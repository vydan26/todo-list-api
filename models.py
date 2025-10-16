from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Zadatak(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    naziv = db.Column(db.String(200),nullable=False)
    opis = db.Column(db.String(500))
    uradjeno = db.Column(db.Boolean, default=False)
    datum = db.Column(db.DateTime)

