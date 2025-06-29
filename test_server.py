import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.routes.user import user_bp
from src.routes.auth import auth_bp
from src.routes.credits import credits_bp
from src.routes.chat import chat_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'src', 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app, supports_credentials=True)

# Register blueprints
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(credits_bp, url_prefix='/api')
app.register_blueprint(chat_bp, url_prefix='/api')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(os.path.dirname(__file__), "src", "database", "app.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Create some sample products if they don't exist
    from src.models.user import Product
    if Product.query.count() == 0:
        sample_products = [
            Product(name='Basic Package', description='Basic product with 2000 credits', price=10.0, credits_awarded=2000),
            Product(name='Premium Package', description='Premium product with 5000 credits', price=25.0, credits_awarded=5000),
            Product(name='Ultimate Package', description='Ultimate product with 10000 credits', price=50.0, credits_awarded=10000)
        ]
        for product in sample_products:
            db.session.add(product)
        db.session.commit()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

