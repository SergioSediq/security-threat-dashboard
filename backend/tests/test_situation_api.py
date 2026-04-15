def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_summary_shape(client):
    r = client.get("/api/v1/situation/summary")
    assert r.status_code == 200
    body = r.json()
    assert set(body.keys()) >= {
        "total_events",
        "critical",
        "mitre_techniques_observed",
        "osint_items",
    }


def test_threats_list(client):
    r = client.get("/api/v1/threats")
    assert r.status_code == 200
    body = r.json()
    items = body["items"]
    assert body["total"] >= 1
    assert body["limit"] == 50
    assert body["offset"] == 0
    assert len(items) >= 1
    assert "cve_ids" in items[0]


def test_threats_severity_filter(client):
    r = client.get("/api/v1/threats?severity=CRITICAL")
    assert r.status_code == 200
    body = r.json()
    for row in body["items"]:
        assert row["severity"] == "CRITICAL"


def test_version_endpoint(client):
    r = client.get("/api/v1/version")
    assert r.status_code == 200
    body = r.json()
    assert body["app"] == "situation-api"
    assert "version" in body


def test_export_jsonl(client):
    r = client.get("/api/v1/export/threats.jsonl")
    assert r.status_code == 200
    assert r.headers.get("content-type", "").startswith("application/x-ndjson")
    assert len(r.content) > 0


def test_osint_list(client):
    r = client.get("/api/v1/osint")
    assert r.status_code == 200
    body = r.json()
    assert "items" in body
    assert isinstance(body["items"], list)


def test_meta(client):
    r = client.get("/api/v1/meta")
    assert r.status_code == 200
    body = r.json()
    assert "fixture_mode" in body
    assert "version" in body


def test_mitre_reference(client):
    r = client.get("/api/v1/mitre/reference")
    assert r.status_code == 200
    ref = r.json()
    assert isinstance(ref, dict)
    assert len(ref) >= 1
