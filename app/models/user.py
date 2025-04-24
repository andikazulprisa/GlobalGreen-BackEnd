from ..extentions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), nullable=False) # 'seller' atau 'customer'

    products = db.relationship('Product', backref='seller', lazy=True)
    carts = db.relationship('Cart', backref='customer', lazy=True)
    reviews = db.relationship('Review', backref='author', lazy=True)
    transactions = db.relationship('Transaction', backref='buyer', lazy=True)
    wishlists = db.relationship('Wishlist', backref='customer', lazy=True)