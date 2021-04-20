from app import app
from models import db, connect_db


db.drop_all()
db.create_all()
