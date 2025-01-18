import uuid
from sqlalchemy import Column, String, BigInteger, Float, DateTime
from sqlalchemy.dialects.postgresql import UUID
from utilities.database import Base


class Data(Base):
    __tablename__ = "xlsx_data"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    datetime = Column(DateTime, nullable=False)
    close = Column(Float, nullable=False)
    high = Column(Float, nullable=False)
    low = Column(Float, nullable=False)
    volume = Column(BigInteger, nullable=False)
    instrument = Column(String, nullable=False)
