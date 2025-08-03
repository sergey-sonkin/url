# URL Shortener

A simple URL shortening service built with FastAPI.

## Usage

```bash
# Install dependencies
uv sync

# Run the server
python main.py
```

Visit `http://localhost:8000` for the web interface or use the API endpoints.

## Web Interface

- Navigate to `http://localhost:8000`
- Enter a URL and click "Shorten URL"
- Copy the shortened URL with one click

## API

- `POST /shorten` - Shorten a URL
- `GET /{code}` - Redirect to original URL
- `GET /docs` - API documentation

## Example

```bash
curl -X POST "http://localhost:8000/shorten" \
  -H "Content-Type: application/json" \
  -d '{"url": "https://example.com"}'
```
