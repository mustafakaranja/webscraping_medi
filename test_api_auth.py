import requests
import json

def test_medifind_api():
    """Test the Medifind API with authentication"""
    url = "https://www.medifind.com/api/search/doctors/conditionSearch"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMyMzI2LCJlbWFpbCI6Im11c3RhZmFrYXJhbmphd2FsYTcyQGdtYWlsLmNvbSIsImdpdmVuTmFtZSI6Ik11c3RhZmEiLCJmYW1pbHlOYW1lIjoiS2FyYW5qYXdhbGEiLCJoYXNQTUFjY291bnQiOmZhbHNlLCJ2YWxpZEFkbWluRG9tYWluIjpmYWxzZSwicG1UZWFtRGlzYWJsZWRTdGF0dXMiOm51bGwsInByb2ZpbGVNYW5hZ2VtZW50QWNjb3VudERpc2FibGVkIjpudWxsLCJOUEkiOm51bGwsInNvY2lhbExvZ2luIjp0cnVlLCJzb2NpYWxMb2dpblZpYSI6Ikdvb2dsZSIsImlhdCI6MTc1MjQ4MTIxNCwiZXhwIjoxNzUyNTY3NjE0LCJpc3MiOiJNZWRpRmluZCJ9.p0XELt9iX-7D61dcoG5vseYLmZi0G9hC5KyR6L03J5k',
        'Referer': 'https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors',
        'Origin': 'https://www.medifind.com',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin'
    }
    
    payload = {
        "conditionId": 3766,
        "page": 0,
        "limit": 10,  # Small limit for testing
        "sort": "relevance",  # Fixed: use valid sort value
        "filters": {
            "location": {},
            "specialty": [],
            "hospital": [],
            "insurance": [],
            "gender": [],
            "language": []
        }
    }
    
    try:
        print("🔄 Testing Medifind API...")
        response = requests.post(url, json=payload, headers=headers, timeout=30)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📊 Response Headers: {dict(response.headers)}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API Test Successful!")
            print(f"📈 Total doctors found: {data.get('totalCount', 0)}")
            print(f"📋 Doctors in this page: {len(data.get('doctors', []))}")
            
            if data.get('doctors'):
                print("\n👨‍⚕️ Sample physician data:")
                for i, doctor in enumerate(data['doctors'][:3]):  # Show first 3
                    name = f"{doctor.get('firstName', '')} {doctor.get('lastName', '')}"
                    specialty = ', '.join([spec.get('name', '') for spec in doctor.get('specialties', [])])
                    location = f"{doctor.get('city', '')}, {doctor.get('state', '')}"
                    experience = doctor.get('yearsOfExperience', 0)
                    publications = doctor.get('publicationCount', 0)
                    
                    print(f"  {i+1}. {name}")
                    print(f"     Specialty: {specialty}")
                    print(f"     Location: {location}")
                    print(f"     Experience: {experience} years")
                    print(f"     Publications: {publications}")
                    print()
            
            print("🎉 Ready to use API in Streamlit app!")
            return True
        else:
            print(f"❌ API Error: {response.status_code}")
            print(f"📄 Response: {response.text}")
            return False
        
    except Exception as e:
        print(f"💥 Exception: {str(e)}")
        return False

if __name__ == "__main__":
    test_medifind_api()
