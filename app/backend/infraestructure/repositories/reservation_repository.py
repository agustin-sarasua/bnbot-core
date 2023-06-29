from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.backend.domain.entities import Reservation
from app.utils import logger
from sqlalchemy import Column, Date, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship


Base = declarative_base()

class ReservationDB(Base):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    check_in: Mapped[str] = mapped_column(Date())
    check_out: Mapped[str] = mapped_column(Date())
    num_guests: Mapped[int] = mapped_column(Integer())
    property_id: Mapped[int] = mapped_column(String(255))

    price_per_night: Mapped[float] = mapped_column(Float())
    total_price: Mapped[float] = mapped_column(Float())

    currency: Mapped[str] = mapped_column(String(16))
    chat_id: Mapped[str] = mapped_column(String(255))

    customer_number: Mapped[str] = mapped_column(String(255))
    customer_name: Mapped[str] = mapped_column(String(255))
    customer_email: Mapped[str] = mapped_column(String(255))

    timestamp: Mapped[str] = mapped_column(String(255))

    def __repr__(self) -> str:
        return f"Reservation(id={self.id!r}, check_in={self.check_in!r}, check_out={self.check_out!r})"


class ReservationRepository:

    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(db_url)
        self.sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        # logger.info("Creating the table")
        session = self.sessionLocal()
        Base.metadata.create_all(self.engine)
        session.close()

    def save(self, reservation: Reservation):
        logger.info(f"Saving reservation {reservation.check_in}")
        db = self.sessionLocal()
        db_reservations = ReservationDB(check_in=reservation.check_in,
                                        check_out=reservation.check_out,
                                        num_guests=reservation.num_guests,
                                        property_id=reservation.property_id,
                                        price_per_night=reservation.price_per_night,
                                        total_price=reservation.total_price,
                                        currency=reservation.currency,
                                        chat_id=reservation.chat_id,
                                        customer_number=reservation.customer_number,
                                        customer_name=reservation.customer_name,
                                        customer_email=reservation.customer_email,
                                        timestamp=reservation.timestamp)
        db.add(db_reservations)
        db.commit()
        db.refresh(db_reservations)
        return db_reservations
