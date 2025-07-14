#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sraping import PhysicianScraper

def test_updated_api():
    """Test the updated API integration with the new JSON payload"""
    print("🧪 Testing Updated Physician Scraper with New JSON Payload")
    print("=" * 60)
    
    # Initialize scraper with API mode
    scraper = PhysicianScraper(use_api=True)
    
    try:
        # Test API call with the new payload structure
        print("\n📡 Testing API with updated JSON payload...")
        result = scraper.fetch_from_api(condition_id=3766, page=0, limit=10)
        
        if result and 'doctors' in result:
            doctors = result['doctors']
            total_count = result.get('totalCount', 0)
            
            print(f"✅ SUCCESS! Retrieved {len(doctors)} doctors")
            print(f"📊 Total available: {total_count:,}")
            
            if doctors:
                print(f"\n👨‍⚕️ Sample Doctor:")
                doctor = doctors[0]
                print(f"   Name: {doctor.get('firstName', '')} {doctor.get('lastName', '')}")
                print(f"   Specialties: {[s.get('name', '') for s in doctor.get('specialties', [])]}")
                print(f"   Experience: {doctor.get('yearsOfExperience', 0)} years")
                print(f"   Location: {doctor.get('city', '')}, {doctor.get('state', '')}")
                print(f"   Rating: {doctor.get('rating', 0):.1f}/5.0")
                print(f"   Hospital: {[h.get('name', '') for h in doctor.get('hospitals', [])]}")
                
                print(f"\n📋 Available Fields:")
                print(f"   {list(doctor.keys())}")
                
                return True
        else:
            print("❌ No doctor data returned")
            print(f"Result: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_updated_api()
    if success:
        print(f"\n🎉 Test completed successfully!")
        print(f"🚀 Ready to run: streamlit run sraping.py")
    else:
        print(f"\n❌ Test failed - check the implementation")
