# DNS Server in Python

This is a Python-based DNS server that resolves DNS queries for `.ks` domains. The `.ks` TLD (Top-Level Domain) is a friendly nod to [*Kush S.*](https://github.com/krshrimali) a good friend, guide, and the kind of person you want to be or look up to. Cheers, Kush! 🎉 (And hey, you can always change `.ks` to anything you like from config if you don’t like him. 😜)

## Features

- **Custom `.ks` Domain Support**: Resolve `.ks` domains with custom records to make your own little corner of the internet.
- **Support for A and CNAME Records**: Currently, the server supports only `A` and `CNAME` record types for `.ks` domains.
- **Upstream Resolution**: For domains other than `.ks` (e.g., `.com`, `.in`), the server gracefully forwards queries to Google's DNS server.
- **JSON-based Database**: The server uses a JSON file (`DB/registry.json`) as a database for `.ks` domain records.

## Prerequisites

- Python 3.12.0 installed on your system.
  - *Note*: This project was developed and tested on Python 3.12.0. It has not been tested on other Python versions, and compatibility cannot be guaranteed.
- Required Python packages (installable via `requirements.txt`).

## Installation & Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/jaythorat/dns_server-python.git
   cd dns_server-python
   ```

2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the DNS server:
   ```bash
   python server.py
   ```

4. Update your system or browser's DNS settings to point to this server.

5. Add `.ks` domain records by updating the `DB/registry.json` file.

## Testing

1. Add `.ks` domain records to the `DB/registry.json` file (e.g., A or CNAME records).
2. Use a DNS query tool (like `dig`) or configure your browser/system to use the DNS server.
3. Examples of DNS queries using `dig`:
   - Query a custom `.ks` domain (e.g., `test.ks`):
     ```bash
     dig @<DNS_SERVER_IP> test.ks A
     ```
     ```bash
     dig @<DNS_SERVER_IP> test.ks CNAME
     ```
   - Query a regular domain (e.g., `google.com`):
     ```bash
     dig @<DNS_SERVER_IP> google.com
     ```
   Replace `<DNS_SERVER_IP>` with the IP address of your DNS server.

4. Verify `.ks` domains for proper resolution.
5. Test non-`.ks` domains (e.g., `.com`, `.in`) to ensure upstream resolution works properly.

## Limitations

- Currently supports only `A` and `CNAME` record types for `.ks` domains.
- Uses a JSON file as a database, which may not scale for large datasets.
- Requires users to manually change their system or browser's DNS server settings to use this custom DNS server.

## Future Enhancements

- Support for additional record types (e.g., `MX`, `TXT`) to expand functionality.
- Integration with a scalable database instead of JSON for better performance.
- Improved logging and error handling for easier debugging.
- Develop a complete registry service similar to services like GoDaddy or Cloudflare, where users can register and manage domains and DNS records.

## License

This project is open-source and available under the [MIT License](LICENSE).

---