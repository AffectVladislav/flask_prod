from flask import Blueprint
from ..extensions import db
from ..models.user import User

user = Blueprint('user', __name__)


@user.route('/user/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        avatar_filename = save_picture(form.avatar.data)
        user = User(username=form.username.data, login=form.login.data, password=hash_password, avatar=avatar_filename)
        try:
            db.session.add(user)
            db.session.commit()
            flash(f"{form.login.data}: Успешно зарегистрирован!")
            return redirect(url_for('user.login'))
        except Exception as e:
            print(str(e))
            flash(f"При регистрации произошла ошибка", "danger")
    else:
        return render_template('user/register.html', form=form)


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