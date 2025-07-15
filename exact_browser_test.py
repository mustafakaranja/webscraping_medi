import requests
import json
import pandas as pd

def get_physicians_data(page=1, size=20):
    """Get physicians data from Medifind API"""
    
    url = "https://www.medifind.com/api/search/doctors/conditionSearch"
    
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMyMzI2LCJlbWFpbCI6Im11c3RhZmFrYXJhbmphd2FsYTcyQGdtYWlsLmNvbSIsImdpdmVuTmFtZSI6Ik11c3RhZmEiLCJmYW1pbHlOYW1lIjoiS2FyYW5qYXdhbGEiLCJoYXNQTUFjY291bnQiOmZhbHNlLCJ2YWxpZEFkbWluRG9tYWluIjpmYWxzZSwicG1UZWFtRGlzYWJsZWRTdGF0dXMiOm51bGwsInByb2ZpbGVNYW5hZ2VtZW50QWNjb3VudERpc2FibGVkIjpudWxsLCJOUEkiOm51bGwsImlhdCI6MTc1MjU2NjI1OCwiZXhwIjoxNzUyNjUyNjU4LCJpc3MiOiJNZWRpRmluZCJ9.o4NJJJYNZ1dhKborzW5NgOtysFgDtF9apM9X57-K3nI'
    }
    
    # Main payload - this is what works in Postman
    payload = {
        "specialty": ["oncology"],
        "projectId": 3766,
        "radius": None,
        "lat": None,
        "lon": None,
        "country": None,
        "state": None,
        "fidelity": 6,
        "size": size,
        "page": page,
        "gender": None,
        "doctorYearsExperience": 0,
        "languages": [],
        "doctorTier": [],
        "sort": "relevance",
        "type": "conditionSearch",
        "showFeaturedCards": True,
        "telemedicine": False,
        "acceptsNewPatients": False,
        "appointmentAssistOptIn": False
    }
    
    print(f"🔄 Getting page {page} with {size} results...")
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print(f"✅ SUCCESS! Total available: {data.get('totalResults', 'Unknown')}")
            
            if 'results' in data and data['results']:
                physicians = data['results']
                print(f"📋 Got {len(physicians)} physicians")
                
                # Create clean table
                table_data = []
                for doc in physicians:
                    table_data.append({
                        'Name': doc.get('name', ''),
                        'Specialty': doc.get('specialty', ''),
                        'City': doc.get('city', ''),
                        'State': doc.get('state', ''),
                        'Hospital': doc.get('hospital', ''),
                        'Years Experience': doc.get('yearsExperience', ''),
                        'Rating': doc.get('rating', ''),
                        'Phone': doc.get('phone', '')
                    })
                
                # Display table
                df = pd.DataFrame(table_data)
                print("\n" + "="*80)
                print(f"PHYSICIANS - Page {page}")
                print("="*80)
                print(df.to_string(index=False))
                
                # Save to CSV
                filename = f"physicians_page_{page}.csv"
                df.to_csv(filename, index=False)
                print(f"\n💾 Saved to {filename}")
                
                return data
            else:
                print("❌ No results found")
        else:
            print(f"❌ Error: {response.status_code} - {response.text[:200]}")
            
    except Exception as e:
        print(f"❌ Exception: {e}")
    
    return None

if __name__ == "__main__":
    # Get first page (20 results)
    result = get_physicians_data(page=1, size=20)
    
    if result:
        total_results = result.get('totalResults', 0)
        print(f"\n✅ Success! Total physicians available: {total_results}")
        
        # Ask if user wants more pages
        print(f"\nTo get next page, run: get_physicians_data(page=2, size=20)")
        print(f"To get more results per page: get_physicians_data(page=1, size=50)")
    else:
        print("\n❌ Failed to get data")
