from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from utilities.database import get_db
from routes.services import (
    get_data,
    insert_data_into_db,
    visualise_sma,
    generate_signals,
)
import matplotlib

matplotlib.use("Agg")

router = APIRouter()


@router.post("/insert")
def insert_data(db: Session = Depends(get_db)):
    try:
        data = get_data()
        insert_data_into_db(data, db)
        return JSONResponse(status_code=200, content="Data inserted successfully")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/visualise_sma")
def visualise(short_window: int, long_window: int, forecast_steps: int):
    try:
        data = get_data().copy()
        signals = generate_signals(data, short_window, long_window)
        return visualise_sma(signals, short_window, long_window, forecast_steps)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
