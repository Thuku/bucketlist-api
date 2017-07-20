from app import db

class Bucket(db.Model):
    __tablename__ = 'bucket'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    status = db.Column(db.String(100))
    privacy = db.Column(db.String(100))