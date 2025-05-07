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


    def as_dict(self):
        return {
            "order_item_id": self.order_item_id,
            "order_id": self.order_id,
            "product_id": self.product_id,
            "quantity": self.quantity,
            "unit_price": self.unit_price,
            "total_price": self.total_price,
            "discount_amount": self.discount_amount
        }

