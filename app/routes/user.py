from flask import Blueprint
from ..extensions import db
from ..models.user import User

user = Blueprint('user', __name__)

@user.route('/user/<name>')
def create_user(name):
    new_user = User(username=name)
    db.session.add(new_user)
    db.session.commit()
    return 'User Created Successfully'