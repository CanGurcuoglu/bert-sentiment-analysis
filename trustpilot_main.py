import time
from bs4 import BeautifulSoup
import requests

BASE_URL = "https://www.trustpilot.com/review/www.vodafone.co.uk?stars=5"                                          
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

for page in range(1, 3):

    if page == 1:
        url = BASE_URL
    else:
        url = f"{BASE_URL}&page={page}"
        
    try:
        
        # Sending the HTTP request
        response = requests.get(url, headers=HEADERS)
            
        # Parsing HTML content
        soup = BeautifulSoup(response.text, "html.parser")
            
        complaints = soup.find_all("div", class_="styles_reviewContent__44s_M")
            
        if complaints:
            for i, complaint in enumerate(complaints, start=1):
                # Find <p> tags
                p = complaint.find("p", class_="typography_body-l__v5JLj typography_appearance-default__t8iAq typography_color-black__wpn7m")

                if p:
                    complaint_text = p.get_text(strip=True)
                    print(f"Page {page} - Complaint {i}: {complaint_text}\n")
                else:
                    print(f"Page {page} - Complaint {i}: ERROR - No <p> tag found")
        else:
            print(f"No complaints found on page {page}.")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page {page}: {e}")
        
    # Sleep for 5 seconds 
    time.sleep(5)
