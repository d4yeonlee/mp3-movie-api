# MP3 Movie API

## Project Overview

This project is a movie data processing API built using FastAPI, Python, pandas, SQLite, and Fakeredis.

The API allows users to upload movie datasets, process and clean movie data, retrieve movies from SQLite, and use caching to improve retrieval performance.

## Features

- Upload movie datasets in CSV format
- Validate required and numeric columns
- Remove duplicate rows and handle missing values
- Support optional outlier removal
- Store and retrieve movie data using SQLite
- Cache movie search results using Fakeredis
- Automatically invalidate cached results when data changes
- Log API requests and cache activity

## Installation

1. Create a virtual environment:

   python3 -m venv venv

2. Activate the environment:

   source venv/bin/activate

3. Install dependencies:

   python -m pip install -r requirements.txt

## Running the API

Start the FastAPI server:

    uvicorn main:app --reload

Open the interactive API documentation:

http://127.0.0.1:8000/docs

## API Endpoints

### GET /health
Checks whether the API is running.

### POST /upload
Uploads a CSV movie dataset and stores movie data in SQLite.

### GET /movies
Retrieves movies with a configurable limit. Results are cached to avoid repeated database queries.

### GET /movies/search
Searches stored movies using selected columns, minimum rating, and result limit. Results are cached.

### POST /movies/process
Validates and processes movie data using a JSON configuration. Processed data is saved to SQLite.

### GET /datasets/{dataset_id}
Retrieves information about a dataset by its ID.

## SQLite Persistence

Movie data is stored in SQLite so it can persist beyond individual API requests.

## Caching

The API uses Fakeredis to cache movie retrieval results.

- Cache MISS: Queries SQLite and stores the result in the cache.
- Cache HIT: Returns cached data without querying SQLite.
- Cache invalidation: Clears cached results after uploading or processing movie data.
- Cache TTL: 90 seconds.

## Testing

Run the automated tests using:

    python -m pytest tests/ -v

The test suite covers:

- CSV upload
- Movie processing and retrieval
- Missing dataset handling
- Movie retrieval before and after processing
- Cache HIT skipping database queries

## Project Structure

    mp3-movie-api/
    ├── main.py
    ├── requirements.txt
    ├── README.md
    ├── src/
    │   ├── cache.py
    │   ├── storage.py
    │   └── ...
    └── tests/
        ├── conftest.py
        └── test_api.py
