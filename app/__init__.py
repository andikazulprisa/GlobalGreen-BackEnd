from flask import Flask
from config import Config
from .extensions import db, migrate
from .models import User, Product, Category, Cart, Wishlist, Review
from .models import Recipe, RecipeIngredient, RecipeTag, Tag
from .models import CartItem, WishlistItem, ProductImage, Nutrition
from .models import Discount, Order, OrderItem, Payment, Address, ShoppingCart
from app.routes.user_routes import user_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_bp, url_prefix='/users')

    # from app.routes.product_routes import product_bp
    # app.register_blueprint(product_bp, url_prefix='/products')


    return app