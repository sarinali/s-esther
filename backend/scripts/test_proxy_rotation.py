#!/usr/bin/env python3

import requests
import time
import random
from typing import List, Dict

def get_free_proxies() -> List[Dict[str, str]]:
    """Get a list of free proxies for testing (use with caution in production)"""

    free_proxies = [
        "8.210.83.33:80",
        "47.74.152.29:8888",
        "43.134.68.153:3128",
        "185.199.84.161:53281"
    ]

    proxy_list = []
    for proxy in free_proxies:
        proxy_dict = {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
        proxy_list.append(proxy_dict)

    return proxy_list

def test_proxy(proxy: Dict[str, str]) -> bool:
    """Test if a proxy is working"""
    try:
        print(f"Testing proxy: {proxy['http']}")

        response = requests.get(
            "http://httpbin.org/ip",
            proxies=proxy,
            timeout=10
        )

        if response.status_code == 200:
            ip_info = response.json()
            print(f"✅ Proxy working! Your IP appears as: {ip_info.get('origin')}")
            return True
        else:
            print(f"❌ Proxy failed with status: {response.status_code}")
            return False

    except Exception as e:
        print(f"❌ Proxy failed with error: {e}")
        return False

def test_ip_rotation():
    """Test IP rotation with different methods"""

    print("=== Testing IP Rotation Methods ===\n")

    # Method 1: Check current IP without proxy
    print("--- Method 1: Current IP (no proxy) ---")
    try:
        response = requests.get("http://httpbin.org/ip", timeout=10)
        current_ip = response.json().get('origin')
        print(f"Your current IP: {current_ip}")
    except Exception as e:
        print(f"Failed to get current IP: {e}")

    print()

    # Method 2: Test with VPN (manual)
    print("--- Method 2: VPN Rotation (Manual) ---")
    print("💡 To test VPN rotation:")
    print("   1. Connect to a VPN service (NordVPN, ExpressVPN, etc.)")
    print("   2. Run this script again")
    print("   3. Disconnect and reconnect to different VPN servers")
    print("   4. Each connection should show a different IP")
    print()

    # Method 3: Test free proxies
    print("--- Method 3: Free Proxy Rotation ---")
    print("⚠️  Note: Free proxies are unreliable and slow. Use paid proxies for production.")

    free_proxies = get_free_proxies()
    working_proxies = []

    for i, proxy in enumerate(free_proxies):
        print(f"\nTesting proxy {i+1}/{len(free_proxies)}:")
        if test_proxy(proxy):
            working_proxies.append(proxy)

        # Add delay between tests
        time.sleep(2)

    print(f"\n✅ Found {len(working_proxies)} working proxies out of {len(free_proxies)} tested")

    # Method 4: Paid proxy services (examples)
    print("\n--- Method 4: Paid Proxy Services (Recommended) ---")
    print("For production use, consider these paid proxy services:")
    print("📍 Residential Proxies:")
    print("   • Bright Data (brightdata.com)")
    print("   • Smartproxy (smartproxy.com)")
    print("   • ProxyMesh (proxymesh.com)")
    print("   • Storm Proxies (stormproxies.com)")
    print("\n📍 Datacenter Proxies:")
    print("   • HighProxies (highproxies.com)")
    print("   • MyPrivateProxy (myprivateproxy.net)")
    print("   • ProxyRack (proxyrack.com)")
    print("\n📍 Rotating Proxy Services:")
    print("   • Oxylabs (oxylabs.io)")
    print("   • NetNut (netnut.io)")
    print("   • GeoSurf (geosurf.com)")

    # Method 5: AWS/Cloud rotation
    print("\n--- Method 5: Cloud Instance Rotation ---")
    print("💡 Advanced method for large-scale operations:")
    print("   1. Spin up multiple cloud instances (AWS EC2, Google Cloud, etc.)")
    print("   2. Use different regions for different IPs")
    print("   3. Rotate between instances for requests")
    print("   4. Automatically terminate and recreate instances")

def setup_proxy_instructions():
    """Provide setup instructions for proxy rotation"""

    print("\n=== How to Set Up Proxy Rotation ===")
    print("1. Choose a proxy service:")
    print("   • For testing: Use the free proxies in this script")
    print("   • For production: Use paid residential proxies")

    print("\n2. Set up environment variables:")
    print("   export PROXY_LIST='http://user:pass@proxy1.com:8080,http://user:pass@proxy2.com:8080'")

    print("\n3. Alternative: Use VPN with rotation:")
    print("   • Install a VPN client (NordVPN, ExpressVPN)")
    print("   • Use their API to programmatically switch servers")
    print("   • Each server change gives you a new IP")

    print("\n4. Update your LinkedIn credentials:")
    print("   export LINKEDIN_EMAIL='your_email@example.com'")
    print("   export LINKEDIN_PASSWORD='your_password'")

    print("\n5. Test the enhanced LinkedIn service:")
    print("   python scripts/linkedin_profile_scraper.py")

if __name__ == "__main__":
    test_ip_rotation()
    setup_proxy_instructions()