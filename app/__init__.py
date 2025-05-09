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
from app.routes.auth_routes import auth_bp
from app.routes.checkout_routes import checkout_bp
from flask_cors import CORS
from app.extensions import jwt



def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app)

    jwt.init_app(app)
    app.config['JWT_SECRET_KEY'] = 'yumesekai'

    db.init_app(app)
    migrate.init_app(app, db)

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(product_bp, url_prefix='/products')
    app.register_blueprint(category_bp, url_prefix='/categories')
    app.register_blueprint(cart_bp, url_prefix='/carts')
    app.register_blueprint(wishlist_bp, url_prefix='/wishlists')
    app.register_blueprint(recipe_bp, url_prefix='/recipes')
    app.register_blueprint(order_bp, url_prefix='/orders')
    app.register_blueprint(cart_item_bp, url_prefix='/cart_items')
    app.register_blueprint(wishlist_item_bp, url_prefix='/wishlist_items')
    app.register_blueprint(discount_bp, url_prefix='/discounts')
    app.register_blueprint(order_item_bp, url_prefix='/order_items')
    app.register_blueprint(payment_bp, url_prefix='/payments')
    app.register_blueprint(address_bp, url_prefix='/addresses')
    app.register_blueprint(shopping_cart_bp, url_prefix='/shopping_carts')
    app.register_blueprint(nutrition_bp, url_prefix='/nutritions')
    app.register_blueprint(product_image_bp, url_prefix='/product_images')
    app.register_blueprint(tag_bp, url_prefix='/tags')
    app.register_blueprint(recipe_tag_bp, url_prefix='/recipe_tags')
    app.register_blueprint(recipe_ingredient_bp, url_prefix='/recipe_ingredients')
    app.register_blueprint(review_bp, url_prefix='/reviews')
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(checkout_bp, url_prefix='/checkout')

    @app.route('/')
    def index():
        return "Welcome to GlobalGreen API! 🚀 🚀 "


    return app  