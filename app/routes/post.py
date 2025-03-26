from flask import Blueprint, render_template, request, redirect, abort
from flask_login import login_required, current_user

from ..models.user import User
from ..forms import StudentForm, TeacherForm
from ..extensions import db
from ..models.post import Post

post = Blueprint('post', __name__)


@post.route('/', methods=['GET', 'POST'])
def all():
    form = TeacherForm()
    form.teacher.choices = [t.username for s in User.query.filter_by(status=True)]

    if request.method == 'POST':
        teacher = request.form.get('teacher')
        teacher_id = User.query.filter_by(username=teacher).first().id
        teacher_id = Post.query.filter_by(username=teacher.id).order_by(Post.data.desc()).limit(20).all()

    else:
        posts = Post.query.order_by(Post.date.desc()).all()
    return render_template('post/all.html', posts=posts, user=User, form=form)


@post.route('/post/create', methods=['GET', 'POST'])
@login_required
def create():
    form = StudentForm()
    form.student.choices = [s.username for s in User.query.filter_by(status=False)] #   Фильтр учеников "все кто False в бд"
    if request.method == 'POST':
        subject = request.form.get('subject')
        student = request.form.get('student')
        student_id = User.query.filter_by(username=student).first().id

        post = Post(teacher=current_user.id, subject=subject, student=student_id)
        try:
            db.session.add(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
    else:
        return render_template('post/create.html', form=form)


@post.route('/post/<int:id>/update', methods=['GET', 'POST'])
@login_required
def update(id):
    post = Post.query.get(id)

    if post.author.id == current_user.id:

        form = StudentForm()
        form.student.data = User.query.filter_by(id=post.student).first().username
        form.student.choices = [s.username for s in User.query.filter_by(status=False)]
        if request.method == 'POST':
            post.subject = request.form.get('subject')
            student = request.form.get('student')

            post.student = User.query.filter_by(username=student).first().id

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
    if post.author.id == current_user.id:
        try:
            db.session.delete(post)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            print(str(e))
            return str(e)
    else:
        abort(403)