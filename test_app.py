import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Test import
try:
    import streamlit as st
    import requests
    import pandas as pd
    import numpy as np
    from bs4 import BeautifulSoup
    print("✅ All imports successful!")
    
    # Test the scraper class
    from sraping import PhysicianScraper
    scraper = PhysicianScraper()
    
    # Test sample data generation
    sample_data = scraper.generate_sample_data(5)
    print(f"✅ Sample data generated: {len(sample_data['doctors'])} physicians")
    
    # Test data processing
    df = scraper.process_physician_data(sample_data)
    print(f"✅ Data processing successful: {len(df)} rows, {len(df.columns)} columns")
    print("Columns:", list(df.columns))
    
    print("\n🎉 Application is ready to run!")
    print("Run: streamlit run sraping.py")
    
except Exception as e:
    print(f"❌ Error: {str(e)}")
    import traceback
    traceback.print_exc()
