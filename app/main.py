from fastapi import FastAPI, HTTPException
import validators
from dotenv import load_dotenv

from app.models import WebsiteRequest, WebsiteResponse
from app.scraper import WebScraper
from app.analyzer import ContentAnalyzer

# Load environment variables
load_dotenv()

app = FastAPI(
    title="TrustChecker",
    description="AI-powered website content verification system",
    version="1.0.0"
)

# Initialize components
scraper = WebScraper()
analyzer = ContentAnalyzer()

@app.post("/analyze/", response_model=WebsiteResponse)
async def analyze_website(request: WebsiteRequest):
    """Analyze a website's content and compare it with the expected description."""
    
    # Validate URL
    if not validators.url(request.url):
        raise HTTPException(status_code=400, detail="Invalid URL provided")
    
    # Scrape website content
    title, content = scraper.scrape(request.url)
    
    # Analyze content
    match_score, analysis = analyzer.analyze(content, request.expected_description)
    
    return WebsiteResponse(
        url=request.url,
        title=title,
        match_score=match_score,
        analysis=analysis
    )

@app.get("/")
async def root():
    """Root endpoint returning API information."""
    return {
        "name": "TrustChecker",
        "version": "1.0.0",
        "description": "AI-powered website content verification system"
    } 