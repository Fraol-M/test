# Geocoding API

A FastAPI wrapper for the Photon geocoding service that provides place search, location-based search, and reverse geocoding capabilities.

## Features

- 🔍 **Place Search**: Search for places by name with optional limits and language preferences
- 📍 **Location-based Search**: Search for places with location priority using coordinates
- 🔄 **Reverse Geocoding**: Get place information from coordinates
- 📚 **Interactive Documentation**: Auto-generated API documentation with Swagger UI
- 🏥 **Health Check**: Built-in health monitoring endpoint
- 🛡️ **Error Handling**: Comprehensive error handling with proper HTTP status codes

## Installation

1. **Install dependencies**:

   ```bash
   poetry install
   ```

2. **Run the server**:

   ```bash
   poetry run python src/main.py
   ```

   Or alternatively:

   ```bash
   uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### Base URL

```
http://localhost:8000
```

### 1. Root Endpoint

- **GET** `/`
- Returns API information and available endpoints

### 2. Health Check

- **GET** `/health`
- Returns service health status

### 3. Place Search

- **GET** `/search?query={query}&limit={limit}&lang={lang}`
- **POST** `/search`
- Search for places by name

**Parameters:**

- `query` (required): The search query (place name)
- `limit` (optional): Maximum number of results
- `lang` (optional): Language code

**Example GET request:**

```bash
curl "http://localhost:8000/search?query=Berlin&limit=2"
```

**Example POST request:**

```bash
curl -X POST "http://localhost:8000/search" \
  -H "Content-Type: application/json" \
  -d '{"query": "Paris", "limit": 2, "lang": "en"}'
```

### 4. Location-based Search

- **GET** `/search/location?query={query}&lat={lat}&lon={lon}`
- **POST** `/search/location`
- Search for places with location priority

**Parameters:**

- `query` (required): The search query (place name)
- `lat` (required): Latitude for location priority
- `lon` (required): Longitude for location priority

**Example GET request:**

```bash
curl "http://localhost:8000/search/location?query=Berlin&lat=52.3879&lon=13.0582"
```

**Example POST request:**

```bash
curl -X POST "http://localhost:8000/search/location" \
  -H "Content-Type: application/json" \
  -d '{"query": "Paris", "lat": 48.8566, "lon": 2.3522}'
```

### 5. Reverse Geocoding

- **GET** `/reverse?lat={lat}&lon={lon}`
- **POST** `/reverse`
- Get place information from coordinates

**Parameters:**

- `lat` (required): Latitude
- `lon` (required): Longitude

**Example GET request:**

```bash
curl "http://localhost:8000/reverse?lat=52.519854&lon=13.438596"
```

**Example POST request:**

```bash
curl -X POST "http://localhost:8000/reverse" \
  -H "Content-Type: application/json" \
  -d '{"lat": 48.8566, "lon": 2.3522}'
```

## Response Format

### Place Search Response

```json
[
  {
    "name": "Berlin",
    "country": "Germany",
    "coordinates": [13.38886, 52.51704],
    "properties": {
      "name": "Berlin",
      "country": "Germany",
      "city": "Berlin",
      "state": "Berlin",
      "postcode": "10115",
      "osm_id": 240109189,
      "osm_type": "R",
      "extent": [13.08835, 52.67551, 13.76116, 52.33826],
      "countrycode": "DE"
    }
  }
]
```

### Reverse Geocoding Response

```json
{
  "name": "Berlin",
  "country": "Germany",
  "city": "Berlin",
  "state": "Berlin",
  "postcode": "10115",
  "osm_id": 240109189,
  "osm_type": "R",
  "extent": [13.08835, 52.67551, 13.76116, 52.33826],
  "countrycode": "DE"
}
```

## Testing

Run the test script to verify all endpoints:

```bash
python test_api.py
```

This will test all endpoints with sample data and show the results.

## Documentation

Once the server is running, you can access:

- **Interactive API Documentation**: http://localhost:8000/docs
- **Alternative API Documentation**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid parameters
- **404 Not Found**: No results found for the given query
- **500 Internal Server Error**: Unexpected errors
- **502 Bad Gateway**: Issues with the underlying geocoding service

## Development

### Project Structure

```
test/
├── src/
│   └── main.py          # FastAPI application
├── tests/
│   └── __init__.py
├── test_api.py          # Test script
├── pyproject.toml       # Dependencies
└── README.md           # This file
```

### Dependencies

- **FastAPI**: Modern web framework for building APIs
- **httpx**: HTTP client for making requests to the geocoding service
- **uvicorn**: ASGI server for running FastAPI
- **pydantic**: Data validation using Python type annotations

## Example Usage

### Python Client

```python
import httpx

# Search for places
response = httpx.get("http://localhost:8000/search", params={"query": "Berlin"})
places = response.json()

# Reverse geocoding
response = httpx.get("http://localhost:8000/reverse", params={"lat": 52.519854, "lon": 13.438596})
location = response.json()
```

### JavaScript/Node.js Client

```javascript
// Search for places
const response = await fetch("http://localhost:8000/search?query=Berlin");
const places = await response.json();

// Reverse geocoding
const reverseResponse = await fetch(
  "http://localhost:8000/reverse?lat=52.519854&lon=13.438596"
);
const location = await reverseResponse.json();
```

## License

This project is open source and available under the MIT License.
