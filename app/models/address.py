from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.extensions import db

class Address(db.Model):
    __tablename__ = "addresses"

    address_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    address_type = Column(String)
    street_address = Column(String)

    user = relationship("User", back_populates="addresses")