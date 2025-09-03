#!/usr/bin/env python3
"""
Google Drive Configuration
Paste your Google Drive share links here
"""

# STEP 1: Paste your Google Drive share links here
GDRIVE_LINKS = {
    'January 2025': 'https://docs.google.com/spreadsheets/d/18iJOJtBo_haJLsZlFVknuap9xN4HLUa0/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true',
    'February 2025': 'https://docs.google.com/spreadsheets/d/1t6MOUvRrixczqQZu0T_DwhJyhF5XTtnK/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true', 
    'March 2025': 'https://docs.google.com/spreadsheets/d/1te1qlRUqA5QSxu6xBcE0S4mWBuoLTzpI/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true',
    'April 2025': 'https://docs.google.com/spreadsheets/d/1ElaQO46HeNdWLTw0MTeqJl6ecXrujAg2/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true',
    'May 2025': 'https://docs.google.com/spreadsheets/d/1SV8ilwhzRtIpwublxCUQTCuVLeqbwRSi/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true',
    'June 2025': 'https://docs.google.com/spreadsheets/d/1goGzbaFuS_A0OnEsT_EBV5AsXTrQxMeN/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true',
    'July 2025': 'https://docs.google.com/spreadsheets/d/1we0cbjX2UMsgLHLGzxtnAtGHcJXUlZDY/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true',
    'August 2025': 'https://docs.google.com/spreadsheets/d/17XHQw7ZD_dV6-_8wJqHkMvoFgZcv3Mvm/edit?usp=sharing&ouid=107610548173098011871&rtpof=true&sd=true'
}

# STEP 2: Run this script after pasting links above
import re

def extract_file_id(share_link):
    """Extract file ID from Google Sheets/Drive share link"""
    if 'PASTE_YOUR' in share_link:
        return None
    
    # Pattern 1: Google Sheets - /spreadsheets/d/FILE_ID/
    pattern1 = r'/spreadsheets/d/([a-zA-Z0-9_-]+)'
    # Pattern 2: Google Drive - /file/d/FILE_ID/
    pattern2 = r'/file/d/([a-zA-Z0-9_-]+)'
    # Pattern 3: id=FILE_ID
    pattern3 = r'id=([a-zA-Z0-9_-]+)'
    # Pattern 4: /open?id=FILE_ID
    pattern4 = r'/open\?id=([a-zA-Z0-9_-]+)'
    
    for pattern in [pattern1, pattern2, pattern3, pattern4]:
        match = re.search(pattern, share_link)
        if match:
            return match.group(1)
    
    return None

if __name__ == "__main__":
    print("🔗 Google Drive File ID Extractor")
    print("=" * 50)
    
    # Process links
    file_ids = {}
    missing = []
    
    for month, link in GDRIVE_LINKS.items():
        file_id = extract_file_id(link)
        if file_id:
            file_ids[month] = file_id
            print(f"✅ {month}: ID extracted successfully")
        else:
            missing.append(month)
            print(f"❌ {month}: Please add the share link")
    
    print("\n" + "=" * 50)
    
    if missing:
        print(f"\n⚠️ Missing links for: {', '.join(missing)}")
        print("Please edit this file and paste the share links above.")
    else:
        print("\n✅ All file IDs extracted successfully!")
        print("\n📝 Copy this code to replace GDRIVE_FILES in secure_dashboard_gdrive_final.py:")
        print("-" * 50)
        
        print("GDRIVE_FILES = {")
        month_mapping = {
            'January 2025': '2025-01',
            'February 2025': '2025-02',
            'March 2025': '2025-03',
            'April 2025': '2025-04',
            'May 2025': '2025-05',
            'June 2025': '2025-06',
            'July 2025': '2025-07',
            'August 2025': '2025-08'
        }
        
        for month, month_code in month_mapping.items():
            file_id = file_ids.get(month, 'FILE_ID_NOT_FOUND')
            print(f"    '{month_code}': {{")
            print(f"        'id': '{file_id}',")
            print(f"        'name': '{month}'")
            print(f"    }},")
        
        print("}")
        print("-" * 50)
        print("\n✅ Configuration complete! Now:")
        print("1. Copy the code above")
        print("2. Replace GDRIVE_FILES in secure_dashboard_gdrive_final.py")
        print("3. Test with: streamlit run secure_dashboard_gdrive_final.py")