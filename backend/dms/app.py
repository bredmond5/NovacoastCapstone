import os

from flask import Flask

from . import config, domains, groups, lookalikes
from .db import db, migrate
from .groups import scheduler
from .mail import mail


def create_app(*mapping, **kwargs):
    app = Flask(__name__)
    app.secret_key = os.getenv('APP_SECRET_KEY')

    app.config.from_object(config)
    app.config.from_mapping(*mapping, **kwargs)

    db.init_app(app)
    migrate.init_app(app, db)
    mail.init_app(app)

    scheduler.start_scheduler(config.SCHEDULER_DB_URL)

    app.register_blueprint(groups.blueprint, url_prefix='/groups')
    app.register_blueprint(domains.blueprint, url_prefix='/domains')
    app.register_blueprint(lookalikes.blueprint, url_prefix='/lookalikes')

    return app
