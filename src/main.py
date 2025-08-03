import httpx
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import uvicorn

# Initialize FastAPI app
app = FastAPI(
    title="Geocoding API",
    description="A FastAPI wrapper for the Photon geocoding service",
    version="1.0.0"
)

BASE_URL = "https://photon.komoot.io"

# Pydantic models for request/response
class PlaceSearchRequest(BaseModel):
    query: str
    limit: Optional[int] = None
    lang: Optional[str] = None

class LocationSearchRequest(BaseModel):
    query: str
    lat: float
    lon: float

class ReverseGeocodeRequest(BaseModel):
    lat: float
    lon: float

class PlaceResponse(BaseModel):
    name: Optional[str]
    country: Optional[str]
    coordinates: List[float]
    properties: Dict[str, Any]

# Geocoding functions
def search_place(query: str, limit: Optional[int] = None, lang: Optional[str] = None) -> List[Dict[str, Any]]:
    """Search for places by name"""
    params = {"q": query}
    if limit:
        params["limit"] = limit
    if lang:
        params["lang"] = lang

    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/api/", params=params)
            response.raise_for_status()
            return response.json()["features"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Geocoding service error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

def search_with_location(query: str, lat: float, lon: float) -> List[Dict[str, Any]]:
    """Search with location priority"""
    params = {
        "q": query,
        "lat": lat,
        "lon": lon
    }
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/api/", params=params)
            response.raise_for_status()
            return response.json()["features"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Geocoding service error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

def reverse_geocode(lat: float, lon: float) -> Dict[str, Any]:
    """Reverse geocoding"""
    params = {
        "lat": lat,
        "lon": lon
    }
    try:
        with httpx.Client() as client:
            response = client.get(f"{BASE_URL}/reverse", params=params)
            response.raise_for_status()
            features = response.json()["features"]
            if not features:
                raise HTTPException(status_code=404, detail="No location found for the given coordinates")
            return features[0]["properties"]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=f"Geocoding service error: {e}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")

# API Endpoints
@app.get("/", tags=["Root"])
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Geocoding API",
        "version": "1.0.0",
        "endpoints": {
            "search": "/search",
            "search_with_location": "/search/location",
            "reverse_geocode": "/reverse"
        }
    }

@app.post("/search", response_model=List[PlaceResponse], tags=["Search"])
async def search_places(request: PlaceSearchRequest):
    """
    Search for places by name
    
    - **query**: The search query (place name)
    - **limit**: Maximum number of results (optional)
    - **lang**: Language code (optional)
    """
    features = search_place(request.query, request.limit, request.lang)
    
    results = []
    for feature in features:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        results.append(PlaceResponse(
            name=props.get('name'),
            country=props.get('country'),
            coordinates=coords,
            properties=props
        ))
    
    return results

@app.get("/search", response_model=List[PlaceResponse], tags=["Search"])
async def search_places_get(
    query: str = Query(..., description="The search query (place name)"),
    limit: Optional[int] = Query(None, description="Maximum number of results"),
    lang: Optional[str] = Query(None, description="Language code")
):
    """
    Search for places by name (GET method)
    
    - **query**: The search query (place name)
    - **limit**: Maximum number of results (optional)
    - **lang**: Language code (optional)
    """
    features = search_place(query, limit, lang)
    
    results = []
    for feature in features:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        results.append(PlaceResponse(
            name=props.get('name'),
            country=props.get('country'),
            coordinates=coords,
            properties=props
        ))
    
    return results

@app.post("/search/location", response_model=List[PlaceResponse], tags=["Location Search"])
async def search_with_location_priority(request: LocationSearchRequest):
    """
    Search for places with location priority
    
    - **query**: The search query (place name)
    - **lat**: Latitude for location priority
    - **lon**: Longitude for location priority
    """
    features = search_with_location(request.query, request.lat, request.lon)
    
    results = []
    for feature in features:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        results.append(PlaceResponse(
            name=props.get('name'),
            country=props.get('country'),
            coordinates=coords,
            properties=props
        ))
    
    return results

@app.get("/search/location", response_model=List[PlaceResponse], tags=["Location Search"])
async def search_with_location_priority_get(
    query: str = Query(..., description="The search query (place name)"),
    lat: float = Query(..., description="Latitude for location priority"),
    lon: float = Query(..., description="Longitude for location priority")
):
    """
    Search for places with location priority (GET method)
    
    - **query**: The search query (place name)
    - **lat**: Latitude for location priority
    - **lon**: Longitude for location priority
    """
    features = search_with_location(query, lat, lon)
    
    results = []
    for feature in features:
        props = feature["properties"]
        coords = feature["geometry"]["coordinates"]
        results.append(PlaceResponse(
            name=props.get('name'),
            country=props.get('country'),
            coordinates=coords,
            properties=props
        ))
    
    return results

@app.post("/reverse", response_model=Dict[str, Any], tags=["Reverse Geocoding"])
async def reverse_geocode_endpoint(request: ReverseGeocodeRequest):
    """
    Reverse geocoding - get place information from coordinates
    
    - **lat**: Latitude
    - **lon**: Longitude
    """
    return reverse_geocode(request.lat, request.lon)

@app.get("/reverse", response_model=Dict[str, Any], tags=["Reverse Geocoding"])
async def reverse_geocode_endpoint_get(
    lat: float = Query(..., description="Latitude"),
    lon: float = Query(..., description="Longitude")
):
    """
    Reverse geocoding - get place information from coordinates (GET method)
    
    - **lat**: Latitude
    - **lon**: Longitude
    """
    return reverse_geocode(lat, lon)

# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "geocoding-api"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
