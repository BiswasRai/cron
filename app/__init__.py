from flask import Flask
from app.routes import user_bp, student_bp
from app.models.db import db
import os
from flask_migrate import Migrate
from .config import make_celery

def create_app():
    app = Flask(__name__)
    print('Starting app')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY')
    app.config['CELERY_BROKER_URL'] = os.getenv('RABBIT_MQ')
    app.config['CELERY_CONFIG'] = {"broker_url": os.getenv('RABBIT_MQ'), "result_backend": "rpc://"}
    app.config['CELERY_BROKER_TRANSPORT']= 'amqp'
    app.config['CELERY_IMPORTS'] = ('app.tasks')
    celery = make_celery(app)
    celery.set_default()


    app.register_blueprint(user_bp)
    app.register_blueprint(student_bp)

    app.app_context().push()
    db.init_app(app)
    migrate = Migrate(app, db)

    return app, celery
