def test_health_status(client):
    result = client.get("/health-status")

    assert result.json == {"service": "API Star Wars HealthCheck", "version": "1.0"}
    assert result.status_code == 200
