from datetime import datetime
from sqlalchemy import String, Float, DateTime
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class FuelPrice(Base):
    __tablename__ = "fuel_prices"

    # Identifiant unique obligatoire pour la base de données
    id: Mapped[int] = mapped_column(primary_key=True)
    
    station_name: Mapped[str] = mapped_column(String(255))

    # SP95
    sp95_name: Mapped[str] = mapped_column(String(50))
    sp95_price: Mapped[float] = mapped_column(Float)
    sp95_updated_at: Mapped[datetime] = mapped_column(DateTime)

    # Diesel
    diesel_name: Mapped[str] = mapped_column(String(50))
    diesel_price: Mapped[float] = mapped_column(Float)
    diesel_updated_at: Mapped[datetime] = mapped_column(DateTime)

    def __repr__(self) -> str:
        return f"FuelPrice(station={self.station_name!r}, diesel={self.diesel_price}, sp95={self.sp95_price})"
    


