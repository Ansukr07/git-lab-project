"""
Website Uptime Monitor
======================

A simple yet effective tool to check the availability of multiple websites.
It sends HTTP requests and logs the status code and response time.
Can be used as a scheduled task to verify service health.

Dependency:
- requests

Features:
- Configurable timeout.
- JSON logging support (optional).
- User-agent customization.
- Colorized terminal output (simulated).

Author: Ansu Kumar
Version: 1.0.0
Date: 2025-12-17
"""

import argparse
import logging
import sys
import time
import json
try:
    import requests
except ImportError:
    print("❌ Error: 'requests' library is missing. Install via: pip install requests")
    sys.exit(1)

# --- LOGGING ---
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    datefmt="%H:%M:%S",
    handlers=[logging.StreamHandler(sys.stdout)]
)
logger = logging.getLogger("WebMonitor")

# Default list of sites to check
DEFAULT_SITES = [
    "https://www.google.com",
    "https://www.github.com",
    "https://www.python.org",
    "https://www.stackoverflow.com"
]

def check_site(url: str, timeout: int = 5):
    """
    Checks a single URL and returns stats.
    """
    if not url.startswith("http"):
        url = "http://" + url
        
    start_time = time.time()
    try:
        response = requests.get(url, timeout=timeout)
        duration = round((time.time() - start_time) * 1000, 2)
        
        status = response.status_code
        if 200 <= status < 300:
            return {"url": url, "status": status, "time_ms": duration, "result": "UP"}
        else:
            return {"url": url, "status": status, "time_ms": duration, "result": "DOWN"}
            
    except requests.RequestException as e:
        duration = round((time.time() - start_time) * 1000, 2)
        return {"url": url, "status": 0, "time_ms": duration, "result": "ERROR", "error": str(e)}

def main():
    parser = argparse.ArgumentParser(description="Check website uptime.")
    parser.add_argument("urls", nargs="*", help="List of URLs to check")
    parser.add_argument("--file", help="File containing list of URLs (one per line)")
    parser.add_argument("--timeout", type=int, default=5, help="Request timeout in seconds")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")

    args = parser.parse_args()

    # Gather URLs
    urls = args.urls if args.urls else []
    if args.file:
        try:
            with open(args.file, "r") as f:
                file_urls = [line.strip() for line in f if line.strip()]
                urls.extend(file_urls)
        except OSError as e:
            logger.error(f"Could not read file: {e}")
            sys.exit(1)

    if not urls:
        logger.info("No URLs provided. Using defaults.")
        urls = DEFAULT_SITES

    logger.info(f"🚀 Monitoring {len(urls)} websites...")
    logger.info("-" * 60)
    logger.info(f"{'URL':<40} | {'STATUS':<8} | {'TIME (ms)':<10} | {'RESULT'}")
    logger.info("-" * 60)

    results = []
    
    for url in urls:
        data = check_site(url, args.timeout)
        results.append(data)
        
        symbol = "✅" if data["result"] == "UP" else "❌"
        status_display = str(data["status"]) if data["status"] > 0 else "ERR"
        
        if not args.json:
            logger.info(f"{data['url']:<40} | {status_display:<8} | {data['time_ms']:<10} | {symbol} {data['result']}")

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print("-" * 60)
        up_count = sum(1 for r in results if r["result"] == "UP")
        print(f"Summary: {up_count}/{len(urls)} sites are UP.")

if __name__ == "__main__":
    main()
