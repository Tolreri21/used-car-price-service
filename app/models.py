from sqlmodel import Field
from datetime import datetime, timezone

from app.schemas import CarFeaturesBase


class PredictionHistory(CarFeaturesBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    predicted_price: float
