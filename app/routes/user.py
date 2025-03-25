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
@user.route('/user/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(login=form.login.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"{form.login.data}: Успешный вход!")
            return redirect(next_page) if next_page else redirect(url_for('post.all'))
        else:
            flash(f"При входе произошла ошибка", "danger")
    return render_template('user/login.html', form=form)

@user.route('/user/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('post.all'))