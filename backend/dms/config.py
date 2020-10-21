import os

SQLALCHEMY_DATABASE_URI = os.getenv('DB_URL', 'sqlite:///dms.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

RABBITMQ_HOST = os.getenv('RABBITMQ_HOST', 'rabbitmq')
RABBITMQ_QUEUE = os.getenv('RABBITMQ_QUEUE', 'scans')

SCHEDULER_DB_URL = os.getenv('SCHEDULER_DB_URL', 'sqlite:///scheduler.db')
