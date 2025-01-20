from bs4 import BeautifulSoup
import requests

# Base URL
BASE_URL = "https://www.sikayetvar.com"

def get_complaints(brand_name):
    # URL and headers to avoid getting 403 error
    URL = f"https://www.sikayetvar.com/{brand_name}"
    
    # Send the HTTP request
    httpReq = requests.get(URL, headers={'User-agent': 'your bot 0.1'}, verify=False)
    
    # get HTML content
    html = httpReq.text
    soup = BeautifulSoup(html, "html.parser")
    
    complaints = []
    complaint_titles = soup.find_all("h2", class_="complaint-title", limit=30)
    
    for complaint in complaint_titles:
        if complaint:
            # Get the url from the <a> tag
            link_tag = complaint.find("a", class_="complaint-layer")
            if link_tag and "href" in link_tag.attrs:
                relative_url = link_tag["href"]
                full_url = BASE_URL + relative_url  # Concatenate with the base URL
                
                # Send a request to the full page
                full_complaint_req = requests.get(full_url, headers={'User-agent': 'your bot 0.1'}, verify=False)
                full_complaint_html = full_complaint_req.text
                full_complaint_soup = BeautifulSoup(full_complaint_html, "html.parser")
                
                # Get the full text
                complaint_detail = full_complaint_soup.find("div", class_="complaint-detail-description")
                if complaint_detail:
                    full_complaint_text = complaint_detail.text.strip()
                    # Append the full text with its url to the list
                    complaints.append((full_url, full_complaint_text))
    
    return complaints

# Example usage
complaints = get_complaints('vodafone')
for url, text in complaints:
    print(f"\nFull Complaint URL: {url}\n")
    print(f"Full Complaint Text: {text}\n")

print(len(complaints))
