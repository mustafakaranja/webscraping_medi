import requests
import json

def test_api():
    """Test the Medifind API to verify it's working"""
    url = "https://www.medifind.com/api/search/doctors/conditionSearch"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Origin': 'https://www.medifind.com',
        'Referer': 'https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'X-Requested-With': 'XMLHttpRequest'
    }
    
    # Try different payload structures based on what might be expected
    payloads_to_try = [
        # Structure 1: Maybe it expects a different parameter name
        {
            "condition": 3766,
            "page": 0,
            "limit": 5,
            "sort": "relevance"
        },
        
        # Structure 2: Maybe without conditionId
        {
            "page": 0,
            "limit": 5,
            "sort": "relevance",
            "filters": {
                "location": {},
                "specialty": [],
                "hospital": [],
                "insurance": [],
                "gender": [],
                "language": []
            }
        },
        
        # Structure 3: Maybe it uses URL parameters instead
        {
            "input": "&size=200",
            "specialties": "&input=&limit=true",
            "insurance": "&input=&limit=false",
            "language": "&input=&limit=true"
        },
        
        # Structure 4: Try with string values
        {
            "conditionId": "3766",
            "page": "0",
            "limit": "5",
            "sort": "relevance"
        },
        
        # Structure 5: Minimal payload
        {
            "search": "neuroendocrine tumor",
            "limit": 5
        }
    ]
    
    for i, payload in enumerate(payloads_to_try, 1):
        print(f"\n🔄 Trying payload structure {i}:")
        print(f"Payload: {json.dumps(payload, indent=2)}")
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            print(f"Status Code: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                print("✅ API Test Successful!")
                print(f"Response keys: {list(data.keys())}")
                
                if 'totalResults' in data:
                    print(f"Total results: {data.get('totalResults', 0)}")
                elif 'totalCount' in data:
                    print(f"Total count: {data.get('totalCount', 0)}")
                
                if 'results' in data and data['results']:
                    results = data['results']
                    print(f"Results in this page: {len(results)}")
                    first_result = results[0]
                    print(f"First result keys: {list(first_result.keys())}")
                    print(f"Sample data: {json.dumps(first_result, indent=2)[:500]}...")
                elif 'doctors' in data and data['doctors']:
                    doctors = data['doctors']
                    print(f"Doctors in this page: {len(doctors)}")
                    first_doctor = doctors[0]
                    print(f"First doctor keys: {list(first_doctor.keys())}")
                    print(f"Sample doctor: {json.dumps(first_doctor, indent=2)[:500]}...")
                
                return True
            else:
                print(f"❌ Status: {response.status_code}")
                print(f"Response: {response.text}")
                
        except Exception as e:
            print(f"❌ Error with payload {i}: {str(e)}")
            continue
    
    # If all payloads fail, try with GET method and URL parameters
    print(f"\n🔄 Trying GET method with URL parameters:")
    try:
        get_url = f"{url}?conditionId=3766&page=0&limit=5&sort=relevance"
        response = requests.get(get_url, headers=headers, timeout=10)
        print(f"GET Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ GET API Test Successful!")
            print(f"Data: {json.dumps(data, indent=2)[:500]}...")
            return True
        else:
            print(f"GET Response: {response.text}")
    except Exception as e:
        print(f"❌ GET Error: {str(e)}")
    
    print("\n❌ All API attempts failed")
    return False

if __name__ == "__main__":
    test_api()
