import pandas as pd
from models.model import Data
from sqlalchemy.orm import Session
import matplotlib.pyplot as plt
from fastapi.responses import StreamingResponse
import statsmodels.api as sm
import io


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


def calculate_sma(data: pd.DataFrame, column: str, window: int) -> pd.Series:
    return data[column].rolling(window=window).mean()


def generate_signals(
    data: pd.DataFrame, short_window: int, long_window: int
) -> pd.DataFrame:
    data["short_sma"] = calculate_sma(data, "close", short_window)
    data["long_sma"] = calculate_sma(data, "close", long_window)
    data["signal"] = 0
    data.loc[data["short_sma"] > data["long_sma"], "signal"] = 1
    data.loc[data["short_sma"] < data["long_sma"], "signal"] = -1
    return data[["datetime", "close", "short_sma", "long_sma", "signal"]]


def forecast_value(data: pd.DataFrame, forecast_steps: int) -> pd.Series:
    model = sm.tsa.ARIMA(data["close"], order=(5, 1, 0))
    results = model.fit()
    forecast = results.forecast(steps=forecast_steps)
    return forecast


def visualise_sma(
    data: pd.DataFrame, short_window: int, long_window: int, forecast_steps: int
) -> StreamingResponse:
    plt.figure(figsize=(10, 6))
    plt.plot(data["datetime"], data["close"], label="Original Stock Price", marker="o")
    plt.plot(
        data["datetime"],
        data["short_sma"],
        label=f"Short SMA ({short_window} days)",
        marker="o",
        color="blue",
    )
    plt.plot(
        data["datetime"],
        data["long_sma"],
        label=f"Long SMA ({long_window} days)",
        marker="o",
        color="orange",
    )

    forecast = forecast_value(data, forecast_steps)
    forecast_index = pd.date_range(
        start=data["datetime"].iloc[-1] + pd.Timedelta(days=1),
        periods=forecast_steps,
        freq="D",
    )
    plt.plot(forecast_index, forecast, color="red", label="Forecast")

    plt.title("Simple Moving Average (SMA) Crossover with Forecast")
    plt.ylabel("Stock Price")
    plt.xlabel("Date")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    plt.close()
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")
