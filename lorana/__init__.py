from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_mail import Mail
from lorana.config import Config


# => تعريف الادوات خام بدون براميتار  <=
mail = Mail()
db =SQLAlchemy()
bcrypt= Bcrypt()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)   # => بداية تشغبل البرنامج
    # => الاعدادات <=
    app.config.from_object(Config)
    app.config['SQLALCHEMY_ECHO'] = True
    # => ربط الادوات بال app <=
    db.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app,db)

    # => اعدادات ال login manager <=
    from lorana.modules import User
    login_manager.login_view = 'users.login'

    @login_manager.user_loader  #بتشتغل تلقائيا لما فلاسك لوج ان مجتاح يعرف مين اليوزر الحالى (login , built session)
    def load_user(user_id):
        return User.query.get(int(user_id))  # وتقوله مين اليوزر عن طريق انها بتديله ال ip من ال db

    # => تسجيل ال blueprints عشان استدعى الروتس الى فيهم <=
    from lorana.users.routes import users
    from lorana.products.routes import products
    from lorana.main.routes import main
    from lorana.admin.routes import admin
    from lorana.errrors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(products)
    app.register_blueprint(main)
    app.register_blueprint(admin)
    app.register_blueprint(errors)

    return app



