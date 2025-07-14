import requests
from bs4 import BeautifulSoup
import json
import re

def extract_from_browser_html():
    """Extract physician data directly from the HTML page like the browser does"""
    
    url = "https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'Sec-Fetch-Dest': 'document',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-Site': 'none',
        'Cache-Control': 'max-age=0'
    }
    
    try:
        print("🔄 Fetching HTML page...")
        response = requests.get(url, headers=headers, timeout=30)
        response.raise_for_status()
        
        print(f"✅ Page loaded successfully (Status: {response.status_code})")
        print(f"Content-Type: {response.headers.get('content-type', 'Unknown')}")
        print(f"Content-Length: {len(response.content)} bytes")
        
        # Parse the HTML
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Look for JSON data embedded in the page
        print("\n🔍 Looking for embedded JSON data...")
        
        # Method 1: Look for script tags with JSON data
        script_tags = soup.find_all('script')
        for i, script in enumerate(script_tags):
            if script.string:
                # Look for data that might contain physician information
                if any(keyword in script.string.lower() for keyword in ['doctor', 'physician', 'condition', 'search']):
                    print(f"Found potential data in script tag {i}")
                    script_content = script.string
                    
                    # Try to extract JSON objects
                    json_matches = re.findall(r'\{[^{}]*(?:"(?:doctor|physician|condition|totalResults|totalCount)"[^{}]*)*\}', script_content)
                    for j, match in enumerate(json_matches[:3]):  # Show first 3 matches
                        try:
                            data = json.loads(match)
                            print(f"  JSON object {j}: {json.dumps(data, indent=2)[:200]}...")
                        except:
                            print(f"  Potential JSON {j}: {match[:100]}...")
        
        # Method 2: Look for specific data attributes
        print("\n🔍 Looking for data attributes...")
        elements_with_data = soup.find_all(attrs=lambda x: x and any(key.startswith('data-') for key in x.keys()))
        for elem in elements_with_data[:5]:  # Show first 5
            data_attrs = {k: v for k, v in elem.attrs.items() if k.startswith('data-')}
            if data_attrs:
                print(f"Element {elem.name}: {data_attrs}")
        
        # Method 3: Look for physician names and extract surrounding structure
        print("\n🔍 Looking for physician names...")
        
        # Look for links that might be physician profiles
        doctor_links = soup.find_all('a', href=re.compile(r'/doctors?/'))
        print(f"Found {len(doctor_links)} potential doctor links")
        
        physicians = []
        for link in doctor_links[:5]:  # Process first 5
            physician_data = {}
            
            # Extract name from link text or href
            physician_data['name'] = link.get_text(strip=True)
            physician_data['profile_url'] = link.get('href', '')
            
            # Look for parent container that might have more info
            parent = link.parent
            for _ in range(3):  # Go up 3 levels
                if parent and parent.name in ['div', 'article', 'section']:
                    parent_text = parent.get_text()
                    
                    # Look for location patterns
                    location_match = re.search(r'([A-Za-z\s]+),\s*([A-Z]{2})', parent_text)
                    if location_match:
                        physician_data['city'] = location_match.group(1).strip()
                        physician_data['state'] = location_match.group(2)
                    
                    # Look for experience level
                    if 'experienced' in parent_text.lower():
                        physician_data['experience_level'] = 'Experienced'
                    elif 'advanced' in parent_text.lower():
                        physician_data['experience_level'] = 'Advanced'
                    elif 'elite' in parent_text.lower():
                        physician_data['experience_level'] = 'Elite'
                    
                    break
                parent = parent.parent if parent else None
            
            if physician_data['name']:  # Only add if we found a name
                physicians.append(physician_data)
        
        if physicians:
            print(f"\n✅ Extracted {len(physicians)} physicians from HTML:")
            for i, doc in enumerate(physicians, 1):
                print(f"{i}. {doc.get('name', 'Unknown')}")
                if doc.get('city') and doc.get('state'):
                    print(f"   Location: {doc['city']}, {doc['state']}")
                if doc.get('experience_level'):
                    print(f"   Level: {doc['experience_level']}")
                if doc.get('profile_url'):
                    print(f"   URL: https://www.medifind.com{doc['profile_url']}")
                print()
            
            return physicians
        else:
            print("❌ No physician data found in HTML")
            
            # Debug: Show page structure
            print("\n🔍 Page structure analysis:")
            title = soup.find('title')
            if title:
                print(f"Page title: {title.get_text()}")
            
            # Look for any text that mentions doctors or results
            page_text = soup.get_text()
            if 'doctor' in page_text.lower():
                # Find lines with "doctor" in them
                lines_with_doctor = [line.strip() for line in page_text.split('\n') 
                                   if 'doctor' in line.lower() and len(line.strip()) > 5]
                print("Lines mentioning 'doctor':")
                for line in lines_with_doctor[:5]:
                    print(f"  {line[:100]}...")
            
            return []
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return []

if __name__ == "__main__":
    physicians = extract_from_browser_html()
    print(f"\n📊 Final result: {len(physicians)} physicians extracted")
