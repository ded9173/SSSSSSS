from flask import Flask
from config import get_config
from extensions import db, migrate, login_manager
from models import User


def create_app():
    app = Flask(__name__)
    app.config.from_object(get_config())

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Blueprints
    from blueprints.auth import auth_bp
    from blueprints.items import items_bp
    from blueprints.countreparties import countreparties_bp
    from blueprints.countreparties_orders import countreparties_orders_bp
    from blueprints.notes import notes_bp
    from blueprints.specification import specification_bp
    from blueprints.admin import admin_bp
    from blueprints.puzzle_captcha import puzzle_captcha_bp

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(items_bp, url_prefix='/api/items')
    app.register_blueprint(countreparties_bp, url_prefix='/api/countreparties')
    app.register_blueprint(countreparties_orders_bp, url_prefix='/api/orders')
    app.register_blueprint(notes_bp, url_prefix='/api/notes')
    app.register_blueprint(specification_bp, url_prefix='/api/specification')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(puzzle_captcha_bp, url_prefix='/api/captcha')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)