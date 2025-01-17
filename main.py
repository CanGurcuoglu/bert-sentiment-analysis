from bs4 import BeautifulSoup
import requests

# Base URL
BASE_URL = "https://www.sikayetvar.com"

# URL and headers to avoid getting 403 error
URL = "https://www.sikayetvar.com/turkcell"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Send the HTTP request
httpReq = requests.get(URL, headers=headers)

# get HTML content
html = httpReq.text
soup = BeautifulSoup(html, "html.parser")

# Get the first complaint title with its url 
complaint = soup.find("h2", class_="complaint-title")

if complaint:
    # Get the url from the <a> tag
    link_tag = complaint.find("a", class_="complaint-layer")
    if link_tag and "href" in link_tag.attrs:
        relative_url = link_tag["href"]
        full_url = BASE_URL + relative_url  # Concatenate with the base URL ( "https://www.sikayetvar.com" + relative_url )

        # Send a request to the full page
        full_complaint_req = requests.get(full_url, headers=headers)
        full_complaint_html = full_complaint_req.text
        full_complaint_soup = BeautifulSoup(full_complaint_html, "html.parser")

        # Get the full text
        full_complaint_text = full_complaint_soup.find("div", class_="complaint-detail-description").text.strip()

        # Print the full text with its url
        print(f"\nFull Complaint URL: {full_url}\n")
        print(f"Full Complaint Text: {full_complaint_text}\n")
