from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.extensions import db

class Order(db.Model):
    __tablename__ = "orders"

    order_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id", name="fk_orders_user_id"))
    order_date = Column(DateTime, default=datetime.now)
    total_amount = Column(Float)
    status = Column(String)

    shipping_address_id = Column(Integer, ForeignKey("addresses.address_id", name="fk_orders_shipping_address_id"))
    billing_address_id = Column(Integer, ForeignKey("addresses.address_id", name="fk_orders_billing_address_id"))
    delivery_date = Column(DateTime)

    user = relationship("User", back_populates="orders")
    payment = relationship("Payment", back_populates="order", uselist=False)
    order_items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")


    def as_dict(self):
        return {
            "order_id": self.order_id,
            "user_id": self.user_id,
            "order_date": self.order_date,
            "total_amount": self.total_amount,
            "status": self.status,
            "shipping_address_id": self.shipping_address_id,
            "billing_address_id": self.billing_address_id,
            "delivery_date": self.delivery_date
        }
