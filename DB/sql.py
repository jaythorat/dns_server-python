from queue import Empty, Queue
from threading import Lock

import mysql.connector

from config.config import Config


class MysqlConnectionPool:
    def __init__(self):
        self.dConfig = Config()
        self.sqlHost = self.dConfig.getSqlHost()
        self.sqlPort = self.dConfig.getSqlPort()
        self.sqlUser = self.dConfig.getSqlUser()
        self.sqlPassword = self.dConfig.getSqlPassword()
        self.sqlDatabase = self.dConfig.getSqlDatabase()
        self.pool_size = self.dConfig.getConnectionPoolSize()
        self.pool = Queue(maxsize=self.pool_size)
        self.lock = Lock()
        self._initialize_pool()
    

    def _initialize_pool(self):
        """Initialize the pool with connections."""
        for _ in range(self.pool_size):
            conn = self._create_new_connection()
            self.pool.put(conn)

    def _create_new_connection(self):
        """Create a new database connection."""
        return mysql.connector.connect(
            host=self.sqlHost,
            port=self.sqlPort,
            user=self.sqlUser,
            password=self.sqlPassword,
            database=self.sqlDatabase,
            
        )

    # NOT IN USE TEMPORARILY - USED AUTOCOMMIT INSTEAD : Added by JAY 
    def refresh_connection(self, connection):
        """ Ensures the connection sees the latest DB changes. """
        connection.commit()  # Flush any pending changes
        with connection.cursor() as cursor:
            cursor.execute("SET SESSION TRANSACTION ISOLATION LEVEL READ COMMITTED")

    def get_connection(self, timeout=None):
        """ Borrow a connection from the pool and ensure it is valid. """
        try:
            conn = self.pool.get(timeout=timeout)
            conn.autocommit = True  
            if conn.is_connected():
                try:
                    conn.ping(reconnect=True, attempts=3, delay=2)  # Ensures connection is active
                    return conn
                except mysql.connector.Error:
                    print("Connection lost, recreating...")
                    conn = self._create_new_connection()
                    return conn
            else:
                return self._create_new_connection()
        except Empty:
            raise Exception("No available connections in the pool.")

    def return_connection(self, conn):
        """Return a valid connection back to the pool."""
        with self.lock:
            try:
                conn.ping(reconnect=True)  # Ensure it's alive before putting it back
                self.pool.put(conn)
            except mysql.connector.Error:
                print("Dropping bad connection, creating new one...")
                self.pool.put(self._create_new_connection())  # Replace bad connection

    def commitData(self, procedureCall, data, max_retries=3):
        for attempt in range(max_retries):
            connection = self.get_connection()
            cursor = None
            try:
                if not connection:
                    raise Exception("Unable to connect to SQL Server")
                cursor = connection.cursor()
                cursor.callproc(procedureCall, data)
                values = []
                for result in cursor.stored_results():
                    values = list(result.fetchone())
                connection.commit()
                return {"status": "SUCCESS", "data": values}
            except Exception as e:
                return {"status": "FAILURE", "data": None, "message": str(e)}
            finally:
                try:
                    if cursor:
                        cursor.close()
                    if connection:
                        self.return_connection(connection)
                except Exception as e:
                    print(f"Error closing cursor or retuning connection: {str(e)}")
        return {"status": "FAILURE", "data": None, "message": "Unable to connect to SQL Server"}

    def getData(self, procedureCall, data, max_retries=3):
        for attempt in range(max_retries):
            connection = None
            try:
                connection = self.get_connection()
                with connection.cursor(dictionary=True) as cursor:
                    cursor.callproc(procedureCall, data)
                    for result in cursor.stored_results():
                        rows = result.fetchall()
                return {"status": "SUCCESS", "data": rows}
            except Exception as e:
                return {"status": "FAILURE", "data": None, "message": str(e)}
            finally:
                if connection:
                    try:
                        self.return_connection(connection)
                    except Exception as e:
                        print(f"Error closing connection: {str(e)}")

        return {"status": "FAILURE", "data": None, "message": "Unable to connect to SQL Server"}

    def close_all_connections(self):
        """Close all connections in the pool."""
        while not self.pool.empty():
            conn = self.pool.get()
            conn.close()