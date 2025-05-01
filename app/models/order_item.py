from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db


class OrderItem(db.Model):
    __tablename__ = "order_items"

    order_item_id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.order_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))
    quantity = Column(Integer)
    unit_price = Column(Float)
    total_price = Column(Float)
    discount_amount = Column(Float)

    order = relationship("Order", back_populates="order_items")
    product = relationship("Product", back_populates="order_items")