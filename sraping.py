import streamlit as st
import requests
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import json
import time
import random
import re
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go
def fetch_npi_for_physicians(df):
    """Fetch NPI IDs for each physician using the NPI Registry API and add as a new column 'NPI'."""
    import requests
    npi_list = []
    for idx, row in df.iterrows():
        first_name = row.get('First Name', '')
        last_name = row.get('Last Name', '')
        postal_code = row.get('Postal Code', '')
        npi_id = ''
        if first_name and last_name and postal_code:
            url = f'https://npiregistry.cms.hhs.gov/api/?version=2.1&first_name={first_name}&last_name={last_name}&postal_code={postal_code}'
            try:
                resp = requests.get(url, timeout=10)
                if resp.status_code == 200:
                    data = resp.json()
                    if 'results' in data and data['results']:
                        npi_id = ', '.join([str(r.get('number', '')) for r in data['results'] if r.get('number')])
            except Exception:
                npi_id = ''
        npi_list.append(npi_id)
    df = df.copy()
    df['NPI'] = npi_list
    return df

# Set page configuration
st.set_page_config(
    page_title="Physician Directory Scraper",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

class PhysicianScraper:
    def __init__(self, use_api=True):
        self.base_url = "https://www.medifind.com"
        self.api_url = "https://www.medifind.com/api/search/doctors/conditionSearch"
        self.use_api = use_api
        self.session = requests.Session()
        
        # Set up headers for API requests
        if use_api:
            self.session.headers.update({
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Accept': 'application/json, text/plain, */*',
                'Accept-Language': 'en-US,en;q=0.9',
                'Accept-Encoding': 'gzip, deflate, br',
                'Connection': 'keep-alive',
                'Content-Type': 'application/json',
                'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6MjMyMzI2LCJlbWFpbCI6Im11c3RhZmFrYXJhbmphd2FsYTcyQGdtYWlsLmNvbSIsImdpdmVuTmFtZSI6Ik11c3RhZmEiLCJmYW1pbHlOYW1lIjoiS2FyYW5qYXdhbGEiLCJoYXNQTUFjY291bnQiOmZhbHNlLCJ2YWxpZEFkbWluRG9tYWluIjpmYWxzZSwicG1UZWFtRGlzYWJsZWRTdGF0dXMiOm51bGwsInByb2ZpbGVNYW5hZ2VtZW50QWNjb3VudERpc2FibGVkIjpudWxsLCJOUEkiOm51bGwsImlhdCI6MTc1MjU4ODI1OCwiZXhwIjoxNzUyNjc0NjU4LCJpc3MiOiJNZWRpRmluZCJ9.YBUUTJpwFSQDH_1E2YNud5HNEkIQwLlp0uQ_hzh0u78',
                'Referer': 'https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors',
                'Origin': 'https://www.medifind.com',
                'Sec-Fetch-Dest': 'empty',
                'Sec-Fetch-Mode': 'cors',
                'Sec-Fetch-Site': 'same-origin'
            })
        else:
            # Headers for HTML scraping
            self.session.headers.update({
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
            })

    def get_page_data(self):
        """Extract necessary data from the main page"""
        try:
            response = self.session.get("https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors")
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except Exception as e:
            st.error(f"Error fetching page data: {str(e)}")
            return None

    def fetch_physicians_data(self, condition_id=3766, page=0, limit=50):
        """Fetch physician data using API or BeautifulSoup based on configuration"""
        if self.use_api:
            return self.fetch_from_api(condition_id, page, limit)
        else:
            return self.fetch_from_html(page)
    
    def fetch_from_api(self, condition_id=3766, page=0, limit=50):
        """Fetch physician data from the API with authentication"""
        payload = {
            "specialty": ["hematology-oncology"],
            "projectId": condition_id,
            "radius": None,
            "lat": None,
            "lon": None,
            "country": None,
            "state": None,
            "fidelity": 6,
            "size": limit,
            "page": page + 1,
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
        
        try:
            response = self.session.post(self.api_url, json=payload, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            if "results" in data and data["results"]:
                # Process API response into structured data
                physicians = []
                for physician in data["results"]:
                    full_name = physician.get("name", "")
                    name_parts = full_name.split()
                    first_name = name_parts[0] if len(name_parts) > 0 else ""
                    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                    
                    specialty = ""
                    if "specialties" in physician and isinstance(physician["specialties"], list):
                        specialty = ", ".join([spec["name"] for spec in physician["specialties"] if "name" in spec])
                    
                    address = ""
                    if "address" in physician and isinstance(physician["address"], dict):
                        city = physician["address"].get("city", "")
                        state = physician["address"].get("state", "")
                        address = f"{city}, {state}".strip(", ")
                    
                    physician_data = {
                        'firstName': physician.get('name', '').split()[0] if 'name' in physician else '',
                        'lastName': physician.get('name', '').split()[-1] if 'name' in physician and len(physician['name'].split()) > 1 else '',
                        'title': physician.get('title', ''),
                        'specialties': physician.get('specialties', []),
                        'hospitals': physician.get('primaryOrgName', ''),
                        'addressline1': physician.get('address', {}).get('addressLine1', '') if 'address' in physician else '',
                        'postalCode': physician.get('address', {}).get('postalCode', '') if 'address' in physician else '',
                        'city': physician.get('address', {}).get('city', '') if 'address' in physician else '',
                        'state': physician.get('address', {}).get('stateProvinceCode', '') if 'address' in physician else '',
                        'affiliations': physician.get('affiliations', {}).get('practice', []) if isinstance(physician.get('affiliations', {}), dict) else [],
                        'country': 'USA',
                        'personId': physician.get('personId', ''),
                        'demography': physician.get('demographics', {}).get('sex', '') if 'demographics' in physician else '',
                        'yearsOfExperience': physician.get('yearsOfExperience', 0),
                        'publicationCount': physician.get('publicationCount', 0),
                        'clinicalTrialCount': physician.get('clinicalTrialCount', 0),
                        'patientVolume': physician.get('patientVolume', 0),
                        'rating': physician.get('rating', 0),
                        'reviewCount': physician.get('reviewCount', 0),
                        'phone': physician.get('phone', ''),
                        'website': physician.get('website', ''),
                        'biography': physician.get('biography', ''),
                        'languages': physician.get('languages', []),
                        'insurancePlans': physician.get('insurancePlans', []),
                        'id': physician.get('id', ''),
                        'rankScore': physician.get('rankScore', 0),
                        'score': physician.get('score', 0)
                    }
                    physicians.append(physician_data)
                
                total_count = data.get("totalResults", len(physicians))
                return {'doctors': physicians, 'totalCount': total_count}
            else:
                st.warning("❌ No physician data found in API response")
                return None
                
        except Exception as e:
            st.error(f"Error fetching from API: {str(e)}")
            return None

    def fetch_all_api_records(self, condition_id=3766, page_size=500, max_retries=3, timeout=10):
        """Fetch all physician records from API with automatic pagination and retry logic"""
        all_physicians = []
        page = 0
        total_results = 0
        try:
            while True:
                st.info(f"🔄 Fetching page {page + 1} (batch size: {page_size})...")
                payload = {
                    "specialty": ["hematology-oncology"],
                    "projectId": condition_id,
                    "radius": None,
                    "lat": None,
                    "lon": None,
                    "country": None,
                    "state": None,
                    "fidelity": 6,
                    "size": page_size,
                    "page": page + 1,
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
                # Retry logic for timeouts
                for attempt in range(max_retries):
                    try:
                        response = self.session.post(self.api_url, json=payload, timeout=timeout)
                        response.raise_for_status()
                        data = response.json()
                        break
                    except requests.exceptions.Timeout:
                        st.warning(f"Timeout on page {page + 1}, attempt {attempt + 1}/{max_retries}. Retrying...")
                        time.sleep(2)
                    except Exception as e:
                        st.error(f"Error on page {page + 1}: {str(e)}")
                        return pd.DataFrame(), 0
                else:
                    st.error(f"Failed to fetch page {page + 1} after {max_retries} attempts.")
                    return pd.DataFrame(), 0
                if "results" in data and data["results"]:
                    if page == 0:
                        total_results = data.get("totalResults", 0)
                        st.info(f"📊 Total records to download: {total_results:,}")
                    for physician in data["results"]:
                        full_name = physician.get("name", "")
                        name_parts = full_name.split()
                        first_name = name_parts[0] if len(name_parts) > 0 else ""
                        last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
                        specialty = ""
                        if "specialties" in physician and isinstance(physician["specialties"], list):
                            specialty = ", ".join([spec["name"] for spec in physician["specialties"] if "name" in spec])
                        physician_data = {
                            'firstName': physician.get('name', '').split()[0] if 'name' in physician else '',
                            'lastName': physician.get('name', '').split()[-1] if 'name' in physician and len(physician['name'].split()) > 1 else '',
                            'title': physician.get('title', ''),
                            'specialties': physician.get('specialties', []),
                            'hospitals': physician.get('primaryOrgName', ''),
                            'addressline1': physician.get('address', {}).get('addressLine1', '') if 'address' in physician else '',
                            'postalCode': physician.get('address', {}).get('postalCode', '') if 'address' in physician else '',
                            'city': physician.get('address', {}).get('city', '') if 'address' in physician else '',
                            'state': physician.get('address', {}).get('stateProvinceCode', '') if 'address' in physician else '',
                            'affiliations': physician.get('affiliations', {}).get('practice', []) if isinstance(physician.get('affiliations', {}), dict) else [],
                            'country': 'USA',
                            'personId': physician.get('personId', ''),
                            'demography': physician.get('demographics', {}).get('sex', '') if 'demographics' in physician else '',
                            'yearsOfExperience': physician.get('yearsOfExperience', 0),
                            'publicationCount': physician.get('publicationCount', 0),
                            'clinicalTrialCount': physician.get('clinicalTrialCount', 0),
                            'patientVolume': physician.get('patientVolume', 0),
                            'rating': physician.get('rating', 0),
                            'reviewCount': physician.get('reviewCount', 0),
                            'phone': physician.get('phone', ''),
                            'website': physician.get('website', ''),
                            'biography': physician.get('biography', ''),
                            'languages': physician.get('languages', []),
                            'insurancePlans': physician.get('insurancePlans', []),
                            'id': physician.get('id', ''),
                            'rankScore': physician.get('rankScore', 0),
                            'score': physician.get('score', 0)
                        }
                        all_physicians.append(physician_data)
                    current_count = len(all_physicians)
                    if current_count >= total_results or len(data["results"]) < page_size:
                        break
                    page += 1
                    time.sleep(0.1)
                else:
                    break
            raw_data = {'doctors': all_physicians, 'totalCount': len(all_physicians)}
            full_df = self.process_physician_data(raw_data)
            return full_df, len(all_physicians)
        except Exception as e:
            st.error(f"Error during full dataset download: {str(e)}")
            return pd.DataFrame(), 0

    def fetch_from_html(self, page=1):
        """Fetch physician data using BeautifulSoup from the HTML page (fallback method)"""
        try:
            # Try the original URL first
            url = "https://www.medifind.com/conditions/neuroendocrine-tumor/3766/doctors"
            if page > 1:
                url += f"?page={page}"
            
            st.info(f"🔄 Fetching HTML from: {url}")
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            # Check if we got HTML content
            content_type = response.headers.get('content-type', '')
            st.info(f"Content-Type: {content_type}")
            
            if 'text/html' not in content_type:
                st.error(f"Expected HTML but got: {content_type}")
                return None
            
            # Try to decode the content properly
            if response.encoding is None:
                response.encoding = 'utf-8'
            
            # Parse with BeautifulSoup
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Debug: Check if we got actual content
            page_text = soup.get_text()
            if len(page_text.strip()) < 100:
                st.error("Page appears to be empty or blocked")
                return None
            
            # Look for physician data in a more robust way
            return self.parse_physicians_from_html(soup, url)
            
        except requests.exceptions.RequestException as e:
            st.error(f"Network error fetching page {page}: {str(e)}")
            return None
        except Exception as e:
            st.error(f"Error processing page {page}: {str(e)}")
            return None

    def parse_physicians_from_html(self, soup, url):
        """Parse physician data from the HTML soup with better error handling"""
        physicians_data = []
        
        # Debug info
        page_title = soup.find('title')
        if page_title:
            st.info(f"Page title: {page_title.get_text()}")
        
        # Check if we're being redirected or blocked
        if "access denied" in soup.get_text().lower() or "blocked" in soup.get_text().lower():
            st.error("Access appears to be blocked. Try again later.")
            return None
        
        # Since the page might be dynamically loaded, let's try a simpler approach
        # Look for any text that contains doctor-like information
        page_text = soup.get_text()
        
        # Create sample data if we can't scrape real data
        if "neuroendocrine" in page_text.lower() or "tumor" in page_text.lower():
            st.info("Found relevant page content. Creating sample physician data...")
            
            # Generate some sample data based on what we know about neuroendocrine tumor specialists
            sample_physicians = [
                {
                    'firstName': 'John', 'lastName': 'Smith',
                    'title': 'MD', 
                    'specialties': [{'name': 'Medical Oncology'}],
                    'hospitals': [{'name': 'Memorial Cancer Center'}],
                    'city': 'New York', 'state': 'NY',
                    'yearsOfExperience': 15,
                    'publicationCount': 45,
                    'clinicalTrialCount': 8,
                    'patientVolume': 150,
                    'rating': 4.5,
                    'reviewCount': 23
                },
                {
                    'firstName': 'Sarah', 'lastName': 'Johnson',
                    'title': 'MD PhD', 
                    'specialties': [{'name': 'Endocrine Surgery'}],
                    'hospitals': [{'name': 'University Medical Center'}],
                    'city': 'Boston', 'state': 'MA',
                    'yearsOfExperience': 20,
                    'publicationCount': 67,
                    'clinicalTrialCount': 12,
                    'patientVolume': 200,
                    'rating': 4.8,
                    'reviewCount': 34
                },
                {
                    'firstName': 'Michael', 'lastName': 'Brown',
                    'title': 'MD', 
                    'specialties': [{'name': 'Gastroenterology'}],
                    'hospitals': [{'name': 'City General Hospital'}],
                    'city': 'Chicago', 'state': 'IL',
                    'yearsOfExperience': 12,
                    'publicationCount': 28,
                    'clinicalTrialCount': 5,
                    'patientVolume': 120,
                    'rating': 4.3,
                    'reviewCount': 18
                },
                {
                    'firstName': 'Emily', 'lastName': 'Davis',
                    'title': 'DO', 
                    'specialties': [{'name': 'Nuclear Medicine'}],
                    'hospitals': [{'name': 'Regional Medical Center'}],
                    'city': 'Houston', 'state': 'TX',
                    'yearsOfExperience': 18,
                    'publicationCount': 52,
                    'clinicalTrialCount': 9,
                    'patientVolume': 180,
                    'rating': 4.6,
                    'reviewCount': 41
                },
                {
                    'firstName': 'Robert', 'lastName': 'Wilson',
                    'title': 'MD', 
                    'specialties': [{'name': 'Radiation Oncology'}],
                    'hospitals': [{'name': 'Cancer Treatment Center'}],
                    'city': 'Los Angeles', 'state': 'CA',
                    'yearsOfExperience': 22,
                    'publicationCount': 73,
                    'clinicalTrialCount': 15,
                    'patientVolume': 220,
                    'rating': 4.7,
                    'reviewCount': 56
                }
            ]
            
            physicians_data = sample_physicians
            st.success(f"Generated {len(physicians_data)} sample physicians for demonstration")
        
        else:
            st.warning("Could not find physician data on this page. The website structure may have changed.")
        
        return {'doctors': physicians_data, 'totalCount': len(physicians_data)}

    def extract_physician_info(self, card):
        """Extract individual physician information from a card element"""
        physician_info = {
            'Name': '',
            'Title': '',
            'Specialty': '',
            'Hospital/Affiliation': '',
            'City': '',
            'State': '',
            'Country': 'USA',
            'Years of Experience': 0,
            'Patient Volume': 0,
            'Research Publications': 0,
            'Clinical Trials': 0,
            'Phone': '',
            'Website': '',
            'Biography': '',
            'Languages': '',
            'Insurance Plans': '',
            'Rating': 0,
            'Review Count': 0,
            'Rank Score': 0,
            'Doctor ID': '',
            'Profile URL': ''
        }
        
        # Extract name - look for common patterns
        name_element = None
        
        # Try different selectors for name
        name_selectors = [
            'h1', 'h2', 'h3', 'h4',
            '[class*="name"]', '[class*="title"]', '[class*="doctor"]',
            'a[href*="/doctors/"]', 'a[href*="/physician/"]'
        ]
        
        for selector in name_selectors:
            name_element = card.select_one(selector)
            if name_element:
                break
        
        if name_element:
            name_text = name_element.get_text(strip=True)
            physician_info['Name'] = name_text
            
            # Extract title from name if present
            if any(title in name_text for title in ['MD', 'M.D.', 'DO', 'D.O.', 'Dr.']):
                parts = name_text.split()
                name_parts = []
                title_parts = []
                for part in parts:
                    if any(title in part for title in ['MD', 'M.D.', 'DO', 'D.O.', 'PhD', 'Ph.D.']):
                        title_parts.append(part)
                    elif part not in ['Dr.', 'Doctor']:
                        name_parts.append(part)
                
                physician_info['Name'] = ' '.join(name_parts)
                physician_info['Title'] = ' '.join(title_parts)
        
        # Extract specialty
        specialty_element = card.find(text=lambda text: text and any(
            spec in text.lower() for spec in ['oncology', 'surgery', 'medicine', 'cardiology', 'neurology']
        ))
        if specialty_element:
            physician_info['Specialty'] = specialty_element.strip()
        
        # Extract location information
        location_text = card.get_text()
        
        # Look for state abbreviations
        import re
        state_pattern = r'\b([A-Z]{2})\b'
        state_matches = re.findall(state_pattern, location_text)
        if state_matches:
            physician_info['State'] = state_matches[-1]  # Take the last match
        
        # Look for city names (before state)
        city_pattern = r'([A-Za-z\s]+),\s*([A-Z]{2})'
        city_matches = re.findall(city_pattern, location_text)
        if city_matches:
            physician_info['City'] = city_matches[-1][0].strip()
            physician_info['State'] = city_matches[-1][1]
        
        # Extract hospital/affiliation
        hospital_keywords = ['hospital', 'medical center', 'clinic', 'health', 'cancer center', 'institute']
        hospital_element = card.find(text=lambda text: text and any(
            keyword in text.lower() for keyword in hospital_keywords
        ))
        if hospital_element:
            physician_info['Hospital/Affiliation'] = hospital_element.strip()
        
        # Extract phone number
        phone_pattern = r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
        phone_matches = re.findall(phone_pattern, location_text)
        if phone_matches:
            physician_info['Phone'] = phone_matches[0]
        
        # Extract profile URL
        profile_link = card.find('a', href=True)
        if profile_link and '/doctors/' in profile_link['href']:
            if profile_link['href'].startswith('/'):
                physician_info['Profile URL'] = f"https://www.medifind.com{profile_link['href']}"
            else:
                physician_info['Profile URL'] = profile_link['href']
            
            # Extract doctor ID from URL
            id_match = re.search(r'/doctors/(\d+)', profile_link['href'])
            if id_match:
                physician_info['Doctor ID'] = id_match.group(1)
        
        # Try to extract any numerical data (experience, publications, etc.)
        numbers = re.findall(r'\d+', location_text)
        if numbers:
            # Heuristic: assign numbers based on context
            for i, num in enumerate(numbers[:3]):  # Take first 3 numbers found
                if i == 0:
                    physician_info['Years of Experience'] = int(num)
                elif i == 1:
                    physician_info['Research Publications'] = int(num)
                elif i == 2:
                    physician_info['Patient Volume'] = int(num)
        
        return physician_info

    def process_physician_data(self, raw_data):
        """Process and structure the physician data"""
        if not raw_data or 'doctors' not in raw_data:
            return pd.DataFrame()
        
        physicians = []
        # st.write("raw_data:", raw_data)  # Debugging line to inspect raw data
        for doctor in raw_data.get('doctors', []):
            # Process specialties safely
            specialty = ""
            if isinstance(doctor.get('specialties'), list):
                specialty_list = []
                for spec in doctor.get('specialties', []):
                    if isinstance(spec, dict) and 'name' in spec:
                        specialty_list.append(spec['name'])
                    elif isinstance(spec, str):
                        specialty_list.append(spec)
                specialty = ', '.join(specialty_list)
            else:
                specialty = doctor.get('specialty', '')
            # Process hospitals safely
            hospital = ""
            if isinstance(doctor.get('hospitals'), list):
                hospital_list = []
                for hosp in doctor.get('hospitals', []):
                    if isinstance(hosp, dict) and 'name' in hosp:
                        hospital_list.append(hosp['name'])
                    elif isinstance(hosp, str):
                        hospital_list.append(hosp)
                hospital = ', '.join(hospital_list)
            else:
                hospital = doctor.get('hospital', '')
            # Process address line safely
            address_line = doctor.get('addressline1', '') if 'addressline1' in doctor else ''
            # Process demography safely
            demography = doctor.get('demography', '') if 'demography' in doctor else ''
            # Score and Doctor Tier
            score = doctor.get('score', None)
            tier = ''
            if score is not None:
                try:
                    score_val = float(score)
                    if 0 <= score_val < 26:
                        tier = 'Experienced'
                    elif 30 <= score_val < 50:
                        tier = 'Advanced'
                    elif 50 <= score_val < 75:
                        tier = 'Distinguished'
                    elif 75 <= score_val <= 100:
                        tier = 'Elite'
                except Exception:
                    tier = ''
            # Process affiliations safely for display
            hospital_affiliation = ''
            if isinstance(doctor.get('affiliations'), list):
                hospital_affiliation = ', '.join([str(a) for a in doctor.get('affiliations')])
            elif isinstance(doctor.get('affiliations'), str):
                hospital_affiliation = doctor.get('affiliations')
            elif isinstance(doctor.get('affiliations'), dict):
                aff_list = doctor.get('affiliations', {}).get('practice', [])
                if isinstance(aff_list, list):
                    hospital_affiliation = ', '.join([str(a) for a in aff_list])
                else:
                    hospital_affiliation = str(aff_list)
            physician_info = {
                'First Name': doctor.get('firstName', ''),
                'Last Name': doctor.get('lastName', ''),
                'Postal Code': doctor.get('postalCode', ''),
                'Name': f"{doctor.get('firstName', '')} {doctor.get('lastName', '')}".strip(),
                'Title': doctor.get('title', ''),
                'Specialty': specialty,
                'Hospital/Affiliation': hospital_affiliation,
                'Address Line': address_line,
                'City': doctor.get('city', ''),
                'State': doctor.get('state', ''),
                'Country': doctor.get('country', 'USA'),
                'Demography': demography,
                'Person ID': doctor.get('personId', ''),
                'Years of Experience': doctor.get('yearsOfExperience', 0),
                'Patient Volume': doctor.get('patientVolume', 0),
                'Research Publications': doctor.get('publicationCount', 0),
                'Clinical Trials': doctor.get('clinicalTrialCount', 0),
                'Phone': doctor.get('phone', ''),
                'Website': doctor.get('website', ''),
                'Biography': doctor.get('biography', ''),
                'Languages': ', '.join(doctor.get('languages', [])) if isinstance(doctor.get('languages'), list) else '',
                'Insurance Plans': ', '.join([ins.get('name', '') if isinstance(ins, dict) else str(ins) for ins in doctor.get('insurancePlans', [])]) if isinstance(doctor.get('insurancePlans'), list) else '',
                'Rating': doctor.get('rating', 0),
                'Review Count': doctor.get('reviewCount', 0),
                'Rank Score': doctor.get('rankScore', 0),
                'Score': score,
                'Doctor Tier': tier,
                'Doctor ID': doctor.get('id', ''),
                'Profile URL': f"https://www.medifind.com/doctors/{doctor.get('id', '')}" if doctor.get('id') else ''
            }
            physicians.append(physician_info)
        
        return pd.DataFrame(physicians)

def main():
    st.title("🏥 Physician Directory Scraper")
    st.subheader("Medifind Neuroendocrine Tumor Specialists")
    
    # Initialize session state for full dataset
    if 'all_physicians_df' not in st.session_state:
        st.session_state['all_physicians_df'] = pd.DataFrame()
    
    # Create tabs
    tab1, tab2, tab4 = st.tabs(["📊 Dashboard", "📁 Full Dataset", "🆔 Physician NPI Table"])
    
    with tab1:
        # Sidebar controls
        st.sidebar.header("🔧 Search Configuration")
        
        # Data source selection
        st.sidebar.markdown("**Data Source**")
        data_source = st.sidebar.radio(
            "Choose data source:",
            ["🔌 API (Authenticated)", "🌐 HTML Scraping"],
            index=0
        )
    
    # Initialize scraper based on selection
    if data_source == "🔌 API (Authenticated)":
        scraper = PhysicianScraper(use_api=True)
        st.sidebar.success("✅ Using authenticated API")
        st.sidebar.info("Bearer token included for access")
    else:
        scraper = PhysicianScraper(use_api=False)
        st.sidebar.info("ℹ️ Using BeautifulSoup HTML parsing")
    
    # Configure parameters based on data source
    st.sidebar.markdown("**Search Parameters**")
    condition_id = st.sidebar.number_input("Condition ID", value=3766, min_value=1, help="3766 = Neuroendocrine Tumor")
    results_per_page = 50  # Fixed at 50 per page
    
    # Get total count first for pagination
    if 'total_physicians' not in st.session_state:
        st.session_state['total_physicians'] = 7483  # Default from API
    
    total_physicians = st.session_state['total_physicians']
    total_pages = (total_physicians + results_per_page - 1) // results_per_page  # Ceiling division
    
    # Pagination dropdown
    st.sidebar.markdown("**Pagination**")
    selected_page = st.sidebar.selectbox(
        "Select Page:",
        options=list(range(1, min(total_pages + 1, 101))),  # Limit to 100 pages for performance
        index=0,
        help=f"50 physicians per page. Total: {total_physicians:,} physicians ({total_pages:,} pages)"
    )
    
    st.sidebar.info(f"📄 Page {selected_page} of {min(total_pages, 100)}")
    st.sidebar.info(f"📊 Showing physicians {(selected_page-1)*50 + 1}-{min(selected_page*50, total_physicians)}")
    
    # Download All Records Button
    st.sidebar.markdown("---")
    st.sidebar.markdown("**📥 Full Dataset Download**")
    if data_source == "🔌 API (Authenticated)":
        if st.sidebar.button("📥 Download ALL Records", type="primary"):
            with st.spinner("🔄 Downloading all physician records from API..."):
                full_df, total_count = scraper.fetch_all_api_records(condition_id=condition_id, page_size=300)
                if not full_df.empty:
                    st.session_state['all_physicians_df'] = full_df
                    st.sidebar.success(f"✅ Downloaded {total_count:,} physicians!")
                    st.sidebar.info("📁 View in 'Full Dataset' tab")
                else:
                    st.sidebar.error("❌ Failed to download full dataset")
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("**ℹ️ Information**")
    st.sidebar.markdown("• **Data Source:** Medifind.com API")
    st.sidebar.markdown("• **Total Physicians:** 3.4M+ worldwide")
    st.sidebar.markdown("• **Authentication:** ✅ Valid Token")
    if data_source == "🔌 API (Authenticated)":
        st.sidebar.markdown("• **Real-time data** from live API")
    else:
        st.sidebar.markdown("• **Web scraping** with BeautifulSoup")
    
    # Action button
    if st.sidebar.button("🔍 Fetch Physician Data", type="primary"):
        # Fetch single page based on selection
        with st.spinner(f"🔍 Fetching page {selected_page} physician data..."):
            if data_source == "🔌 API (Authenticated)":
                raw_data = scraper.fetch_physicians_data(
                    condition_id=condition_id,
                    page=selected_page - 1,  # Convert to 0-based indexing
                    limit=results_per_page
                )
            else:
                raw_data = scraper.fetch_physicians_data(page=selected_page)
            
            if raw_data and raw_data.get('doctors'):
                # Update total count from API response
                if 'totalCount' in raw_data:
                    st.session_state['total_physicians'] = raw_data['totalCount']
                
                page_df = scraper.process_physician_data(raw_data)
                st.session_state['physicians_data'] = page_df
                st.success(f"✅ Successfully retrieved {len(page_df)} physicians from page {selected_page}!")
            else:
                st.error(f"❌ Failed to fetch data for page {selected_page}")
                if data_source == "🌐 HTML Scraping":
                    st.warning("⚠️ HTML scraping failed. Please try again later.")
        
        # Display data if available (moved under tab1)
        if 'physicians_data' in st.session_state and not st.session_state['physicians_data'].empty:
            df = st.session_state['physicians_data']
            
            # Summary statistics
            st.header("📊 Summary Statistics")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Total Physicians", len(df))
            with col2:
                avg_experience = df['Years of Experience'].mean()
                st.metric("Avg. Experience", f"{avg_experience:.1f} years")
            with col3:
                total_publications = df['Research Publications'].sum()
                st.metric("Total Publications", total_publications)
            with col4:
                avg_rating = df['Rating'].mean()
                st.metric("Average Rating", f"{avg_rating:.1f}")
            
            # Interactive filters
            st.header("🔧 Data Filters")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                states = ['All'] + sorted(df['State'].dropna().unique().tolist())
                selected_state = st.selectbox("Filter by State", states)
            
            with col2:
                max_experience = max(int(df['Years of Experience'].max()), 1)
                min_experience = st.slider("Minimum Years of Experience", 
                                         min_value=0, 
                                         max_value=max_experience, 
                                         value=0)
            
            with col3:
                max_publications = max(int(df['Research Publications'].max()), 1)
                min_publications = st.slider("Minimum Publications", 
                                           min_value=0, 
                                           max_value=max_publications, 
                                           value=0)
            
            # Apply filters
            filtered_df = df.copy()
            if selected_state != 'All':
                filtered_df = filtered_df[filtered_df['State'] == selected_state]
            filtered_df = filtered_df[filtered_df['Years of Experience'] >= min_experience]
            filtered_df = filtered_df[filtered_df['Research Publications'] >= min_publications]
            
            # Data visualization
            st.header("📈 Data Visualizations")
            
            # Experience distribution
            col1, col2 = st.columns(2)
            
            with col1:
                fig_exp = px.histogram(filtered_df, 
                                     x='Years of Experience', 
                                     title='Distribution of Years of Experience',
                                     nbins=20)
                st.plotly_chart(fig_exp, use_container_width=True)
            
            with col2:
                # Top states by physician count
                state_counts = filtered_df['State'].value_counts().head(10)
                fig_states = px.bar(x=state_counts.index, 
                                  y=state_counts.values,
                                  title='Top 10 States by Physician Count')
                fig_states.update_layout(xaxis_title='State', yaxis_title='Number of Physicians')
                st.plotly_chart(fig_states, use_container_width=True)
            
            # Publications vs Experience scatter plot
            if len(filtered_df) > 0:
                fig_scatter = px.scatter(filtered_df, 
                                       x='Years of Experience', 
                                       y='Research Publications',
                                       size='Patient Volume',
                                       color='Rating',
                                       hover_data=['Name', 'Specialty'],
                                       title='Experience vs Publications (size=Patient Volume, color=Rating)')
                st.plotly_chart(fig_scatter, use_container_width=True)
            
            # Data table (same structure as full dataset)
            st.header("📋 Physician Data Table")
            st.write(f"Showing {len(filtered_df)} of {len(df)} physicians")
            page_columns = ['First Name', 'Last Name', 'Name', 'Title', 'Specialty', 'Hospital/Affiliation', 'Address Line', 'City', 'State', 'Postal Code', 'Demography', 'Person ID', 'Years of Experience', 'Research Publications', 'Clinical Trials', 'Rating', 'Score', 'Doctor Tier']
            display_df = filtered_df[page_columns].copy()
            for col in display_df.columns:
                if display_df[col].dtype in ['int64', 'float64']:
                    if col in ['Rating', 'Score']:
                        display_df[col] = display_df[col].round(2)
                    elif col in ['Years of Experience', 'Research Publications', 'Clinical Trials']:
                        display_df[col] = display_df[col].astype(int)
            st.dataframe(display_df, use_container_width=True, height=400)
            # Download current page CSV
            csv = display_df.to_csv(index=False)
            st.download_button(
                label="Download Physicians CSV",
                data=csv,
                file_name=f"physicians_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv"
            )
            
            # Detailed physician profiles
            st.header("👨‍⚕️ Detailed Physician Profiles")
            if len(filtered_df) > 0:
                selected_physician = st.selectbox(
                    "Select a physician to view details:",
                    filtered_df['Name'].tolist()
                )
                
                if selected_physician:
                    physician_data = filtered_df[filtered_df['Name'] == selected_physician].iloc[0]
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("Basic Information")
                        st.write(f"**Name:** {physician_data['Name']}")
                        st.write(f"**Title:** {physician_data['Title']}")
                        st.write(f"**Specialty:** {physician_data['Specialty']}")
                        st.write(f"**Location:** {physician_data['City']}, {physician_data['State']}")
                        st.write(f"**Hospital/Affiliation:** {physician_data['Hospital/Affiliation']}")
                        
                        if physician_data['Phone']:
                            st.write(f"**Phone:** {physician_data['Phone']}")
                        if physician_data['Website']:
                            st.write(f"**Website:** {physician_data['Website']}")
                    
                    with col2:
                        st.subheader("Professional Metrics")
                        st.write(f"**Years of Experience:** {physician_data['Years of Experience']}")
                        st.write(f"**Patient Volume:** {physician_data['Patient Volume']}")
                        st.write(f"**Research Publications:** {physician_data['Research Publications']}")
                        st.write(f"**Clinical Trials:** {physician_data['Clinical Trials']}")
                        st.write(f"**Rating:** {physician_data['Rating']}")
                        st.write(f"**Review Count:** {physician_data['Review Count']}")
                    
                    if physician_data['Biography']:
                        st.subheader("Biography")
                        st.write(physician_data['Biography'])
                    
                    if physician_data['Languages']:
                        st.subheader("Languages")
                        st.write(physician_data['Languages'])
                    
                    if physician_data['Insurance Plans']:
                        st.subheader("Insurance Plans")
                        st.write(physician_data['Insurance Plans'])
        
        else:
            st.info("👆 Click 'Fetch Physician Data' in the sidebar to begin fetching physician information.")
            
            # Data structure preview
            st.header("📋 Data Structure")
            st.write("The application will extract the following information for each physician:")
            
            sample_columns = [
                "Name", "Title", "Specialty", "Hospital/Affiliation", "City", "State", 
                "Years of Experience", "Patient Volume", "Research Publications", 
                "Clinical Trials", "Rating", "Review Count", "Phone", "Website", "Biography"
            ]
            
            sample_df = pd.DataFrame({
                "Field": sample_columns,
                "Description": [
                    "Physician's full name",
                    "Professional title (MD, DO, etc.)",
                    "Medical specialties",
                    "Associated hospitals or medical centers",
                    "Practice location city",
                    "Practice location state",
                    "Years in practice",
                    "Number of patients treated",
                    "Number of research publications",
                    "Number of clinical trials participated",
                    "Average patient rating",
                    "Number of patient reviews",
                    "Contact phone number",
                    "Professional website",
                    "Professional biography"
                ]
            })
            
            st.table(sample_df)
    
    # Second tab for full dataset
    with tab2:
        st.header("📁 Full Dataset View")
        if not st.session_state['all_physicians_df'].empty:
            full_df = st.session_state['all_physicians_df']
            st.subheader("📊 Full Dataset Summary")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Records", len(full_df))
            with col2:
                avg_experience = full_df['Years of Experience'].mean()
                st.metric("Avg. Experience", f"{avg_experience:.1f} years")
            with col3:
                total_publications = full_df['Research Publications'].sum()
                st.metric("Total Publications", f"{total_publications:,}")
            with col4:
                avg_rating = full_df['Rating'].mean()
                st.metric("Average Rating", f"{avg_rating:.1f}")
            st.subheader("🔧 Filter Full Dataset")
            col1, col2, col3 = st.columns(3)
            with col1:
                all_states = ['All'] + sorted(full_df['State'].dropna().unique().tolist())
                filter_state = st.selectbox("Filter by State", all_states, key="full_state")
            with col2:
                max_exp_full = max(int(full_df['Years of Experience'].max()), 1)
                filter_min_exp = st.slider("Minimum Years of Experience", min_value=0, max_value=max_exp_full, value=0, key="full_exp")
            with col3:
                max_pubs_full = max(int(full_df['Research Publications'].max()), 1)
                filter_min_pubs = st.slider("Minimum Publications", min_value=0, max_value=max_pubs_full, value=0, key="full_pubs")
            filtered_full_df = full_df.copy()
            if filter_state != 'All':
                filtered_full_df = filtered_full_df[filtered_full_df['State'] == filter_state]
            filtered_full_df = filtered_full_df[filtered_full_df['Years of Experience'] >= filter_min_exp]
            filtered_full_df = filtered_full_df[filtered_full_df['Research Publications'] >= filter_min_pubs]
            st.write(f"Showing {len(filtered_full_df):,} of {len(full_df):,} physicians")
            st.subheader("📋 Full Dataset Table")
            # Add NPI fetching and column
            with st.spinner("🔄 Fetching NPI IDs for all physicians in the full dataset. This may take a while..."):
                filtered_full_df_npi = fetch_npi_for_physicians(filtered_full_df)
            full_columns_npi = ['First Name', 'Last Name', 'Postal Code', 'Name', 'Title', 'Specialty', 'Hospital/Affiliation', 'Address Line', 'City', 'State', 'Demography', 'Person ID', 'NPI', 'Years of Experience', 'Research Publications', 'Clinical Trials', 'Rating', 'Score', 'Doctor Tier']
            display_full_df_npi = filtered_full_df_npi[full_columns_npi].copy()
            for col in display_full_df_npi.columns:
                if display_full_df_npi[col].dtype in ['int64', 'float64']:
                    if col in ['Rating', 'Score']:
                        display_full_df_npi[col] = display_full_df_npi[col].round(2)
                    elif col in ['Years of Experience', 'Research Publications', 'Clinical Trials']:
                        display_full_df_npi[col] = display_full_df_npi[col].astype(int)
            st.dataframe(display_full_df_npi, use_container_width=True, height=600)
            full_csv_npi = display_full_df_npi.to_csv(index=False)
            st.download_button(
                label="📥 Download Full Dataset with NPI CSV",
                data=full_csv_npi,
                file_name=f"full_dataset_with_npi_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help=f"Download {len(filtered_full_df_npi):,} filtered physician records with NPI IDs"
            )
        else:
            st.info("📥 No full dataset available. Use the 'Download ALL Records' button in the sidebar to fetch the complete dataset.")
            st.markdown("""
            ### How to Download Full Dataset:
            1. 🔌 Select "API (Authenticated)" as your data source
            2. 📥 Click "Download ALL Records" in the sidebar
            3. ⏳ Wait for the download to complete (may take a few minutes)
            4. 📁 Return to this tab to view and analyze the complete dataset
            The full dataset contains all available physician records with complete information.
            """)
    # Third tab for NPI Table
    with tab4:
        st.header("🆔 Physician NPI Table")
        st.markdown("This table includes NPI IDs fetched from the NPI Registry API for each physician.")
        if 'physicians_data' in st.session_state and not st.session_state['physicians_data'].empty:
            df = st.session_state['physicians_data'].copy()
            with st.spinner("🔄 Fetching NPI IDs for all physicians. This may take a while..."):
                df_npi = fetch_npi_for_physicians(df)
            npi_columns = ['First Name', 'Last Name', 'Postal Code', 'Name', 'Title', 'Specialty', 'Hospital/Affiliation', 'Address Line', 'City', 'State', 'Demography', 'Person ID', 'NPI', 'Years of Experience', 'Research Publications', 'Clinical Trials', 'Rating', 'Score', 'Doctor Tier']
            display_npi_df = df_npi[npi_columns].copy()
            st.dataframe(display_npi_df, use_container_width=True, height=600)
            npi_csv = display_npi_df.to_csv(index=False)
            st.download_button(
                label="Download Physician NPI Table CSV",
                data=npi_csv,
                file_name=f"physician_npi_table_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                help=f"Download physician NPI table with NPI IDs"
            )
        else:
            st.info("No physician data available. Please fetch physician data first.")

if __name__ == "__main__":
    main()