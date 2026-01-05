import ssl
import socket
import urllib.request
import urllib.error
from datetime import datetime

# CONFIGURATION
# In a real env, these would load from a config.yaml or env variables
TARGETS = [
    "https://www.google.com",
    "https://github.com",
    "https://expired.badssl.com", # Intentionally bad target for demo
]

def check_ssl_expiry(hostname, port=443):
    """Checks the SSL certificate expiry date for a hostname."""
    context = ssl.create_default_context()
    try:
        with socket.create_connection((hostname, port), timeout=3) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                # Parse the date format: 'May 20 12:00:00 2025 GMT'
                not_after = datetime.strptime(cert['notAfter'], r'%b %d %H:%M:%S %Y %Z')
                days_left = (not_after - datetime.utcnow()).days
                return True, days_left
    except Exception as e:
        return False, str(e)

def check_http_status(url):
    """Checks the HTTP status code."""
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'OpsMonitor/1.0'})
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.getcode()
    except urllib.error.HTTPError as e:
        return e.code
    except urllib.error.URLError as e:
        return f"Unreachable: {e.reason}"

def main():
    print(f"{'TARGET':<30} | {'STATUS':<10} | {'SSL DAYS':<10}")
    print("-" * 55)
    
    for url in TARGETS:
        # Extract hostname for SSL check
        hostname = url.replace("https://", "").replace("http://", "").split('/')[0]
        
        # Run Checks
        http_status = check_http_status(url)
        ssl_valid, ssl_info = check_ssl_expiry(hostname)
        
        # Formatting Output
        ssl_display = f"{ssl_info} days" if ssl_valid else "INVALID"
        print(f"{hostname:<30} | {str(http_status):<10} | {ssl_display:<10}")

if __name__ == "__main__":
    main()
