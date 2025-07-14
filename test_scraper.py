import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test the updated scraper
try:
    from sraping import PhysicianScraper
    
    print("🧪 Testing the updated PhysicianScraper...")
    
    # Test API mode
    scraper = PhysicianScraper(use_api=True)
    print("✅ API scraper initialized")
    
    # Test fetching data
    print("🔄 Testing API fetch...")
    data = scraper.fetch_from_api()
    
    if data and 'doctors' in data:
        print(f"✅ API test successful!")
        print(f"📊 Retrieved {len(data['doctors'])} physicians")
        print(f"📈 Total available: {data.get('totalCount', 0):,}")
        
        # Show first doctor
        if data['doctors']:
            first_doc = data['doctors'][0]
            print(f"\n👨‍⚕️ Sample physician:")
            print(f"   Name: {first_doc.get('firstName')} {first_doc.get('lastName')}")
            print(f"   Specialties: {[s.get('name') for s in first_doc.get('specialties', [])]}")
            print(f"   Location: {first_doc.get('city')}, {first_doc.get('state')}")
            print(f"   Experience: {first_doc.get('yearsOfExperience')} years")
            print(f"   Phone: {first_doc.get('phone')}")
        
        # Test data processing
        print(f"\n🔄 Testing data processing...")
        df = scraper.process_physician_data(data)
        print(f"✅ Processed into DataFrame: {len(df)} rows, {len(df.columns)} columns")
        print(f"📋 Columns: {list(df.columns)}")
        
        print("\n🎉 All tests passed! Ready to run Streamlit app!")
        print("👉 Run: streamlit run sraping.py")
        
    else:
        print("❌ API test failed - no data returned")
        
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
