from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class ProductImage(db.Model):
    __tablename__ = "product_images"

    image_id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    image_url = Column(String)
    alt_text = Column(String)
    display_order = Column(Integer)

    product = relationship("Product", back_populates="images")

    def as_dict(self):
        return {
            "image_id": self.image_id,
            "product_id": self.product_id,
            "image_url": self.image_url,
            "alt_text": self.alt_text,
            "display_order": self.display_order
        }