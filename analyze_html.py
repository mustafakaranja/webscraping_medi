import requests
from bs4 import BeautifulSoup
import re

def test_html_structure():
    """Test to see the HTML structure of the Medifind page"""
    url = "https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Connection': 'keep-alive',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        print("HTML Structure Analysis")
        print("=" * 50)
        
        # Look for common physician-related elements
        print("\n1. Looking for doctor/physician related classes:")
        doctor_elements = soup.find_all(class_=re.compile(r'doctor|physician|profile|result|card', re.I))
        print(f"Found {len(doctor_elements)} elements with doctor-related classes")
        
        for i, elem in enumerate(doctor_elements[:3]):
            print(f"Element {i+1}: {elem.name} with class: {elem.get('class')}")
        
        print("\n2. Looking for links to doctor profiles:")
        doctor_links = soup.find_all('a', href=re.compile(r'/doctors?/|/physician'))
        print(f"Found {len(doctor_links)} doctor profile links")
        
        for i, link in enumerate(doctor_links[:5]):
            print(f"Link {i+1}: {link.get('href')} - Text: {link.get_text(strip=True)[:50]}")
        
        print("\n3. Looking for text containing MD, DO, Dr.:")
        doctor_titles = soup.find_all(text=re.compile(r'\b(Dr\.|MD|M\.D\.|DO|D\.O\.)\b'))
        print(f"Found {len(doctor_titles)} elements with doctor titles")
        
        for i, title in enumerate(doctor_titles[:5]):
            print(f"Title {i+1}: {title.strip()}")
        
        print("\n4. Looking for headings (h1-h6):")
        headings = soup.find_all(['h1', 'h2', 'h3', 'h4', 'h5', 'h6'])
        print(f"Found {len(headings)} headings")
        
        for i, heading in enumerate(headings[:5]):
            print(f"Heading {i+1}: {heading.name} - {heading.get_text(strip=True)}")
        
        print("\n5. Looking for main content area:")
        main_content = soup.find('main') or soup.find('div', class_=re.compile(r'main|content|results'))
        if main_content:
            print(f"Found main content area: {main_content.name} with class: {main_content.get('class')}")
            
            # Look for list items or cards within main content
            cards = main_content.find_all(['div', 'article', 'li'], class_=True)
            print(f"Found {len(cards)} potential card elements in main content")
            
            for i, card in enumerate(cards[:3]):
                text_preview = card.get_text(strip=True)[:100]
                print(f"Card {i+1}: {card.name} - {text_preview}...")
        
        print("\n6. Full page text sample (first 500 chars):")
        page_text = soup.get_text()
        print(page_text[:500])
        
        # Save a sample of the HTML for inspection
        with open('sample_page.html', 'w', encoding='utf-8') as f:
            f.write(str(soup.prettify()))
        print("\n✅ Saved sample HTML to 'sample_page.html' for inspection")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_html_structure()
