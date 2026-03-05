import requests
from bs4 import BeautifulSoup

def fetch_article_text(url: str) -> str:
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Remove noise
    for tag in soup(["script", "style", "nav", "footer", "header"]):
        tag.decompose()
    
    # Extract paragraphs
    paragraphs = soup.find_all("p")
    text = " ".join(p.get_text() for p in paragraphs)
    
    return text.strip()