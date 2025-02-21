# TrustChecker 🛡️

An AI-powered website content verification system that analyzes web pages and determines if they match their expected content description.

## Features 🌟

- URL validation and web scraping
- AI-powered content analysis using GPT-4
- Trust score calculation (0-100%)
- Detailed content analysis and matching

## Prerequisites 📋

- Python 3.8+
- OpenAI API key

## Installation 🚀

1. Clone the repository:
```bash
git clone https://github.com/codewithdark-git/TrustChecker.git
cd TrustChecker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
   - Rename `.env.example` to `.env`
   - Add your OpenAI API key to the `.env` file:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```

## Running the Application 🏃‍♂️

Start the FastAPI server:
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints 🔌

### POST /analyze/
Analyzes a website's content and compares it with the expected description.

#### Request Body:
```json
{
  "url": "https://example.com",
  "expected_description": "An educational website about physics"
}
```

#### Response:
```json
{
  "url": "https://example.com",
  "title": "Example - Learn Physics",
  "match_score": 85,
  "analysis": "The website content largely aligns with the description..."
}
```

## API Documentation 📚

- Interactive API docs (Swagger UI): `http://localhost:8000/docs`
- Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## Error Handling ⚠️

The API includes comprehensive error handling for:
- Invalid URLs
- Unreachable websites
- Scraping failures
- AI analysis errors

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.
