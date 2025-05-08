from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class Payment(db.Model):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id", name="fk_payments_order_id"), unique=True)

    payment_method = Column(String)
    payment_status = Column(String)
    amount = Column(Float)
    payment_date = Column(DateTime, default=datetime.now)

    # Relasi ke Order
    order = relationship("Order", back_populates="payment")

    def as_dict(self):
        return {
            "payment_id": self.payment_id,
            "order_id": self.order_id,
            "payment_method": self.payment_method,
            "payment_status": self.payment_status,
            "amount": self.amount,
            "payment_date": self.payment_date
        }
