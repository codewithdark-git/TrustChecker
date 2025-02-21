from fastapi import HTTPException
import requests
from bs4 import BeautifulSoup
from typing import Tuple

class WebScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }

    def scrape(self, url: str) -> Tuple[str, str]:
        """
        Scrape website content and return title and text.
        
        Args:
            url (str): The URL to scrape
            
        Returns:
            Tuple[str, str]: A tuple containing (title, content)
            
        Raises:
            HTTPException: If there's an error during scraping
        """
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Get title
            title = soup.title.string if soup.title else "No title found"
            
            # Get main content
            for element in soup(['script', 'style', 'meta', 'link', 'header', 'footer', 'nav']):
                element.decompose()
                
            text = ' '.join(soup.stripped_strings)
            return title, text
            
        except requests.RequestException as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error accessing website: {str(e)}"
            )
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error scraping website: {str(e)}"
            ) 