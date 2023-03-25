
from fastapi import FastAPI
import requests
import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from cachetools import cached, TTLCache
import json

app = FastAPI()
# origins = [
#     "http://localhost",
#     "http://localhost:8000",
# ]
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=origins,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# Define the cache with a TTL of 1 hour
cache = TTLCache(maxsize=1000, ttl=3600)

@cached(cache)
@app.get("/api/v1")
async def hello(dish: str):

    if not dish:
        return {
            'statusCode': 400,
            'body': {'message': 'Missing required query parameter "dish"'},
            'headers': {'Content-Type': 'application/json'}
        }

   # Check cache for existing response
    cached_response = cache.get(dish)
    if cached_response:
        print(cached_response)
        return {
            'statusCode': 200,
            'body': cached_response,
            'headers': {'Content-Type': 'application/json'}
        }
    

    else:
        url = "https://nutrition-by-api-ninjas.p.rapidapi.com/v1/nutrition"
        querystring = {"query":dish}
        headers = {
            "X-RapidAPI-Key": "0dfc9dc047msh61e9dbb1a616803p1aefadjsnd675fdb0aaab",
            "X-RapidAPI-Host": "nutrition-by-api-ninjas.p.rapidapi.com"
        }
        response = requests.request("GET", url, headers=headers, params=querystring)

    cache[dish] = response.json()
    return {
        'statusCode': 200,
        'body': cache[dish],
        'headers': {'Content-Type': 'application/json'}
    }


if __name__ == '__main__':
     uvicorn.run(
         app,
         host="127.0.0.1",
         port=8000,
        #  ssl_keyfile="/path/to/ssl/keyfile",
        # ssl_certfile="/path/to/ssl/certfile",
    )
