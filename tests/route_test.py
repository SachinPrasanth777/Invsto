from fastapi.testclient import TestClient
from utilities.database import SessionLocal
from models.model import Data
from datetime import datetime
from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Server Loaded Successfully"


def test_visualise_sma():
    response = client.post(
        "/data/visualise_sma?short_window=5&long_window=10&forecast_steps=3"
    )
    assert response.status_code == 200


def test_data_types():
    with SessionLocal() as db:
        data = db.query(Data).all()
        assert data, "No data found in the trade_data table."
        for entry in data:
            assert isinstance(entry.open, float), "Open should be a float value"
            assert isinstance(entry.high, float), "High should be a float value"
            assert isinstance(entry.low, float), "Low should be a float value"
            assert isinstance(entry.close, float), "Close should be a float value"
            assert isinstance(entry.volume, int), "Volume should be an integer value"
            assert isinstance(entry.instrument, str), "Instrument should be a string"
            assert isinstance(
                entry.datetime, datetime
            ), "Datetime should be a datetime type"
