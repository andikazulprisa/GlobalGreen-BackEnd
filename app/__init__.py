from flask import Flask
from config import Config
from .extensions import db, migrate
from .models import User, Product, Category, Cart, Wishlist, Review
from .models import Recipe, RecipeIngredient, RecipeTag, Tag
from .models import CartItem, WishlistItem, ProductImage, Nutrition
from .models import Discount, Order, OrderItem, Payment, Address, ShoppingCart
from app.routes.user_routes import user_bp
from app.routes.product_routes import product_bp
from app.routes.category_routes import category_bp
from app.routes.cart_routes import cart_bp
from app.routes.wishlist_routes import wishlist_bp
from app.routes.recipe_routes import recipe_bp
from app.routes.order_routes import order_bp
from app.routes.cart_item_routes import cart_item_bp
from app.routes.wishlist_item_routes import wishlist_item_bp
from app.routes.discount_routes import discount_bp
from app.routes.order_item_routes import order_item_bp
from app.routes.payment_routes import payment_bp
from app.routes.address_routes import address_bp
from app.routes.shopping_cart_routes import shopping_cart_bp
from app.routes.nutrition_routes import nutrition_bp
from app.routes.product_image_routes import product_image_bp
from app.routes.tag_routes import tag_bp
from app.routes.recipe_tag_routes import recipe_tag_bp
from app.routes.recipe_ingredient_routes import recipe_ingredient_bp
from app.routes.review_routes import review_bp
from flask_cors import CORS



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(product_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(cart_bp)
    app.register_blueprint(wishlist_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(order_bp)
    app.register_blueprint(cart_item_bp)
    app.register_blueprint(wishlist_item_bp)
    app.register_blueprint(discount_bp)
    app.register_blueprint(order_item_bp)
    app.register_blueprint(payment_bp)
    app.register_blueprint(address_bp)
    app.register_blueprint(shopping_cart_bp)
    app.register_blueprint(nutrition_bp)
    app.register_blueprint(product_image_bp)
    app.register_blueprint(tag_bp)
    app.register_blueprint(recipe_tag_bp)
    app.register_blueprint(recipe_ingredient_bp)
    app.register_blueprint(review_bp)


    return app  