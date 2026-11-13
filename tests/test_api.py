def test_upload_csv(client, sample_csv_bytes):
    response = client.post(
        "/upload",
        files={
            "file": (
                "sample_movies.csv",
                sample_csv_bytes,
                "text/csv"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()
    assert data["rows"] == 20
    assert data["columns"] == 4
    assert data["column_names"] == ["title", "release_year", "rating", "genre"]
    assert data["filename"] == "sample_movies.csv"


def test_process_and_retrieve(
    client, uploaded_dataset_id, processing_body
):
    response = client.post(
        "/movies/process",
        json=processing_body
    )

    assert response.status_code == 200

    result = response.json()
    assert result["validation_rows_removed"] == 0

    report = result["cleaning_report"]
    assert report["rows_before"] == 20
    assert report["rows_after"] == 18
    assert report["rows_removed"] == 2

    response = client.get(
    "/movies/search",
    params={
        "columns": ["title", "rating"],
        "min_rating": 0,
        "limit": 100
    }
)

    assert response.status_code == 200

    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 18

    for movie in data:
        assert "title" in movie
        assert "rating" in movie



def test_retrieve_missing_dataset(client):
    response = client.get("/datasets/99999")

    assert response.status_code == 404


def test_cache_and_processing(client, uploaded_dataset_id, processing_body):
    response1 = client.get("/movies", params={"limit": 100})
    assert response1.status_code == 200

    response2 = client.get("/movies", params={"limit": 100})
    assert response2.status_code == 200
    assert response1.json() == response2.json()

    process_response = client.post(
        "/movies/process",
        json=processing_body
    )
    assert process_response.status_code == 200

    response3 = client.get("/movies", params={"limit": 100})
    assert response3.status_code == 200
    assert len(response3.json()) == 18


def test_cache_hit_skips_database(client, uploaded_dataset_id, monkeypatch):
    import main

    main.movie_cache.invalidate()

    response1 = client.get("/movies", params={"limit": 100})
    assert response1.status_code == 200

    def fail_if_called(*args, **kwargs):
        raise AssertionError("Database should not be queried on cache HIT")

    monkeypatch.setattr(
        main.storage,
        "query_movies",
        fail_if_called
    )

    response2 = client.get("/movies", params={"limit": 100})

    assert response2.status_code == 200
    assert response2.json() == response1.json()
