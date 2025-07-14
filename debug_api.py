import requests
import json

def test_browser_like_request():
    """Try to replicate the exact browser request"""
    
    # The URL from your network tab
    url = "https://www.medifind.com/api/search/doctors/conditionSearch"
    
    # Headers that match exactly what the browser would send
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-encoding': 'gzip, deflate, br, zstd',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.medifind.com',
        'referer': 'https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors',
        'sec-ch-ua': '"Not_A Brand";v="8", "Chromium";v="120", "Google Chrome";v="120"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    # Let's try to see what happens with an empty payload
    print("🔄 Trying empty payload...")
    try:
        response = requests.post(url, json={}, headers=headers, timeout=10)
        print(f"Empty payload status: {response.status_code}")
        if response.status_code != 200:
            print(f"Response: {response.text}")
        else:
            data = response.json()
            print(f"Success! Keys: {list(data.keys())}")
    except Exception as e:
        print(f"Empty payload error: {e}")
    
    # Maybe it's a different endpoint altogether
    print("\n🔄 Trying alternative endpoints...")
    
    alternative_urls = [
        "https://www.medifind.com/api/search/doctors",
        "https://www.medifind.com/api/doctors/search",
        "https://www.medifind.com/api/condition/3766/doctors",
        "https://www.medifind.com/api/conditions/3766/doctors",
    ]
    
    for alt_url in alternative_urls:
        print(f"Trying: {alt_url}")
        try:
            # Try GET first
            response = requests.get(alt_url, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ GET Success at {alt_url}")
                data = response.json()
                print(f"Data structure: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                break
            else:
                print(f"GET {alt_url}: {response.status_code}")
                
            # Try POST with minimal data
            response = requests.post(alt_url, json={}, headers=headers, timeout=10)
            if response.status_code == 200:
                print(f"✅ POST Success at {alt_url}")
                data = response.json()
                print(f"Data structure: {list(data.keys()) if isinstance(data, dict) else type(data)}")
                break
            else:
                print(f"POST {alt_url}: {response.status_code}")
                
        except Exception as e:
            print(f"Error with {alt_url}: {e}")
    
    # Try to get the page HTML and look for the API call pattern
    print("\n🔄 Analyzing page source for API patterns...")
    try:
        page_response = requests.get(
            "https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors",
            headers={'User-Agent': headers['user-agent']},
            timeout=10
        )
        
        if page_response.status_code == 200:
            html_content = page_response.text
            
            # Look for API endpoints in the HTML
            import re
            api_patterns = re.findall(r'(/api/[^"\'>\s]+)', html_content)
            if api_patterns:
                print("Found API endpoints in HTML:")
                for pattern in set(api_patterns):
                    print(f"  {pattern}")
            
            # Look for JavaScript that might show the correct payload
            js_api_calls = re.findall(r'(fetch|axios|XMLHttpRequest)[^;]+api[^;]+', html_content, re.IGNORECASE)
            if js_api_calls:
                print("Found potential API calls:")
                for call in js_api_calls[:3]:  # Show first 3
                    print(f"  {call[:100]}...")
                    
    except Exception as e:
        print(f"Error analyzing page: {e}")

if __name__ == "__main__":
    test_browser_like_request()
