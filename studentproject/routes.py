import os
import secrets
from studentproject.table import Student, Teacher, Assignment
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, session,\
                  abort
from studentproject import app, db, bcrypt, login_manager, mail
from studentproject.forms import (RegistrationFormStudent, LoginForm, PostForm,
                               RegistrationFormTeacher, ResetPasswordForm,
                               UpdateAccountForm, RequestResetForm)
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message


@app.route("/")
@app.route("/home", methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        page = request.args.get('page', 1, type=int)
        assignment = Assignment.query.filter(Assignment.topic.like(search))\
                               .paginate(page=page, per_page=5)
        return render_template('home.html', posts=assignment,  tag=tag)
    else:
        page = request.args.get('page', 1, type=int)
        posts = db.session.query(Assignment).paginate(page=page, per_page=5)
        return render_template('home.html', posts=posts)


@app.route("/people")
@login_required
def people():
    if current_user.role == 'Teacher':
        people = db.session.query(Student)\
                           .filter(current_user.standard == Student.standard)\
                           .all()
    else:
        people = db.session.query(Teacher)\
                           .filter(current_user.standard == Teacher.standard)\
                           .all()
    return render_template('people.html', people=people)


@app.route("/register_student", methods=['GET', 'POST'])
def register_student():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationFormStudent()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        student = Student(username=form.username.data, email=form.email.data,
                          password=hashed_password,
                          standard=form.standard.data,
                          section=form.section.data,
                          role='Student'
                          )
        db.session.add(student)
        db.session.commit()
        flash('Your account has been created! \
              You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register_student.html', title='Register',
                           form=form)


@app.route("/register_teacher", methods=['GET', 'POST'])
def register_teacher():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationFormTeacher()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        teacher = Teacher(username=form.username.data, email=form.email.data,
                          password=hashed_password,
                          standard=form.standard.data,
                          subject=form.subject.data,
                          role='Teacher'
                          )
        db.session.add(teacher)
        db.session.commit()
        flash('Your account has been created! \
              You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register_teacher.html', title='Register',
                           form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        if form.role.data == 'Student':
            Check = Student.query.filter_by(email=form.email.data).first()
            session['account_type'] = 'Student'
        else:
            Check = Teacher.query.filter_by(email=form.email.data).first()
            session['account_type'] = 'Teacher'
        if Check and bcrypt.check_password_hash(Check.password,
                                                form.password.data):
            login_user(Check, remember=form.remember.data)
            page = request.args.get('page', 1, type=int)
            posts = db.session.query(Assignment)\
                              .paginate(page=page, per_page=5)
            return render_template('home.html', title='Home',
                                   form=form, posts=posts)
        else:
            flash('Login Unsuccessful. \
                  Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    session.pop('account type', None)
    logout_user()
    return redirect(url_for('login'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics',
                                picture_fn)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.standard = form.standard.data
        if current_user.role == 'Student':
            current_user.section = form.section.data
        else:
            current_user.subject = form.subject.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.standard.data = current_user.standard
        if current_user.role == 'Student':
            form.section.data = current_user.section
        else:
            form.subject.data = current_user.subject
    image_file = url_for('static',
                         filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account',
                           image_file=image_file, form=form)


@login_manager.user_loader
def load_user(user_id):
    if 'account_type' in session:
        if session['account_type'] == 'Teacher':
            return Teacher.query.get(int(user_id))
        elif session['account_type'] == 'Student':
            return Student.query.get(int(user_id))
    else:
        return None


@app.route("/assignment/new", methods=['GET', 'POST'])
@login_required
def new_assignment():
    form = PostForm()
    if form.validate_on_submit():
        post = Assignment(topic=form.topic.data, work=form.work.data,
                          author=current_user, subject=current_user.subject,
                          standard=current_user.standard,
                          due_date=form.due_date.data
                          )
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_assignment.html', title='New Assignment',
                           form=form, legend='New Assignment')


@app.route("/assignment/<int:post_id>")
def assignment(post_id):
    post = Assignment.query.get_or_404(post_id)
    return render_template('assignment.html', title=post.topic, post=post)


@app.route("/assignment/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_assignment(post_id):
    post = Assignment.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.topic = form.topic.data
        post.work = form.work.data
        post.due_date = form.due_date.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('home', post_id=Assignment.id))
    elif request.method == 'GET':
        form.topic.data = post.topic
        form.work.data = post.work
        form.due_date.data = post.due_date
    return render_template('create_assignment.html', title='Update Post',
                           form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_assignment(post_id):
    post = Assignment.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def group_assignment(username):
    page = request.args.get('page', 1, type=int)
    user = Teacher.query.filter_by(username=username).first_or_404()
    posts = Assignment.query.filter_by(author=user)\
        .order_by(Assignment.date_posted.desc())\
        .paginate(page=page, per_page=5)
    return render_template('group_assignment.html', posts=posts, user=user)


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request then simply ignore \
this email and no changes will be made.
'''
    mail.send(msg)


@app.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user1 = Student.query.filter_by(email=form.email.data).first()
        user2 = Teacher.query.filter_by(email=form.email.data).first()
        if user1:
            send_reset_email(user1)
        elif user2:
            send_reset_email(user2)
        flash('An email has been sent with instructions to \
               reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title='Reset Password',
                           form=form)


@app.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user1 = Student.verify_reset_token(token)
    user2 = Teacher.verify_reset_token(token)
    if user1 is None and user2 is None:
        flash('That is an invalid or expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)\
                                .decode('utf-8')
        if user1 is None:
            user2.password = hashed_password
        else:
            user1.password = hashed_password
        db.session.commit()
        flash('Your password has been updated! \
              You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title='Reset Password',
                           form=form)


@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404


@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403


@app.errorhandler(500)
def error_500(error):
    return render_template('500.html'), 500
