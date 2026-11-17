import pytest
from fastapi.testclient import TestClient

from app import db
from app.main import create_app
from app.schemas import Category, Priority

ARABIC = "الفلوس اتخصمت من كارتي مرتين ومحدش رد عليا"


@pytest.fixture
def db_path(tmp_path):
    return str(tmp_path / "test.db")


@pytest.fixture
def client(db_path):
    return TestClient(create_app(db_path))


def test_create_ticket_returns_201_and_id(client):
    r = client.post("/tickets", json={"text": ARABIC, "channel": "app"})
    assert r.status_code == 201
    assert isinstance(r.json()["id"], int)


def test_roundtrip_preserves_arabic_and_metadata(client):
    meta = {"customer_tier": "gold"}
    tid = client.post("/tickets", json={"text": ARABIC, "channel": "chat", "metadata": meta}).json()["id"]
    got = client.get(f"/tickets/{tid}").json()
    assert got["text"] == ARABIC
    assert got["metadata"] == meta
    assert got["category"] is None  # not classified yet


def test_get_missing_ticket_returns_404(client):
    assert client.get("/tickets/9999").status_code == 404


@pytest.mark.parametrize("text", ["", "   ", "\n\t"])
def test_rejects_empty_or_blank_text(client, text):
    r = client.post("/tickets", json={"text": text, "channel": "app"})
    assert r.status_code == 422


def test_rejects_unknown_channel(client):
    r = client.post("/tickets", json={"text": ARABIC, "channel": "carrier_pigeon"})
    assert r.status_code == 422


def test_stats_counts_by_category(client, db_path):
    db.insert_ticket(db_path, "a", "app", category="billing")
    db.insert_ticket(db_path, "b", "app", category="billing")
    db.insert_ticket(db_path, "c", "web", category="outage")
    client.post("/tickets", json={"text": ARABIC, "channel": "app"})  # unclassified
    stats = {row["category"]: row["n"] for row in client.get("/stats/by-category").json()}
    assert stats == {"billing": 2, "outage": 1, "unclassified": 1}


def test_ticket_category_and_priority_serialization(client, db_path):
    tid = db.insert_ticket(
        db_path,
        text=ARABIC,
        channel="app",
        category=Category.billing_charges.value,
        priority=Priority.high.value,
    )
    got = client.get(f"/tickets/{tid}").json()
    assert got["category"] == Category.billing_charges.value
    assert got["priority"] == Priority.high.value


def test_all_taxonomy_categories_are_valid_enums():
    expected_categories = {
        "billing_charges",
        "payment_failure",
        "account_access",
        "service_outage",
        "technical_issue",
        "security_fraud",
        "request_information",
        "other_unclear",
    }
    assert {c.value for c in Category} == expected_categories
    assert {p.value for p in Priority} == {"high", "medium", "low"}


def test_text_5000_char_limit(client):
    r_valid = client.post("/tickets", json={"text": "a" * 5000, "channel": "app"})
    assert r_valid.status_code == 201

    r_invalid = client.post("/tickets", json={"text": "a" * 5001, "channel": "app"})
    assert r_invalid.status_code == 422


