from flask import Blueprint, render_template, request, redirect
from flask_login import login_required, current_user

from ..models.user import User
from ..forms import StudentForm
from ..extensions import db
from ..models.post import Post

post = Blueprint('post', __name__)


@post.route('/', methods=['GET', 'POST'])
def all():
    posts = Post.query.all()
    return render_template('post/all.html', posts=posts)


@post.route('/post/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        teacher = request.form.get('teacher')
        subject = request.form.get('subject')
        student = request.form.get('student')

        post = Post(teacher=teacher, subject=subject, student=student)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))


@post.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)
    if request.method == 'POST':
        post.teacher = request.form.get('teacher')
        post.subject = request.form.get('subject')
        post.student = request.form.get('student')

        try:
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        return render_template('post/update.html', post=post)


@post.route('/post/<int:id>/delete', methods=['GET', 'POST'])
@login_required
def delete(id):
    post = Post.query.get(id)
    try:
        db.session.delete(post)
        db.session.commit()
        return redirect('/')
    except Exception as e:
        print(str(e))
        return str(e)
