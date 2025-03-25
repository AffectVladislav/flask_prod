from ..extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    posts = db.relationship(Post, backref='author', lazy='dynamic')
    status = db.Column(db.Boolean, nullable=False, default=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    login = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    avatar = db.Column(db.String(150), nullable=False)
