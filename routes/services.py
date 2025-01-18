import pandas as pd
from models.model import Data
from sqlalchemy.orm import Session


def get_data() -> pd.DataFrame:
    return pd.read_excel("data/HINDALCO_1D.xlsx")


def insert_data_into_db(data: pd.DataFrame, db: Session):
    for _, row in data.iterrows():
        db_data = Data(
            datetime=row["datetime"],
            close=row["close"],
            high=row["high"],
            low=row["low"],
            open=row["open"],
            volume=row["volume"],
            instrument=row["instrument"],
        )
        db.add(db_data)
    db.commit()
