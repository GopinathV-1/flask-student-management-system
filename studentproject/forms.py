from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import (StringField, PasswordField, SubmitField, BooleanField,
                     IntegerField, SelectField, RadioField, TextAreaField,
                     )
from wtforms.fields.html5 import DateField
from wtforms.validators import (DataRequired, Length, Email, NumberRange,
                                EqualTo, ValidationError)
from studentproject.table import Student, Teacher


class RegistrationFormStudent(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    standard = IntegerField('Standard',
                            validators=[DataRequired(),
                                        NumberRange(min=1, max=12)
                                        ]
                            )
    section = StringField('Section',
                          validators=[DataRequired(), Length(min=1, max=1)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Student.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. \
                                   Please choose a different one.')

    def validate_email(self, email):
        user = Student.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. \
                                   Please choose a different one.')


class RegistrationFormTeacher(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    standard = IntegerField('Standard',
                            validators=[DataRequired(),
                                        NumberRange(min=1, max=12)
                                        ]
                            )
    subject = SelectField('Subject: ', validators=[DataRequired()],
                          choices=[('English', 'English'), ('Tamil', 'Tamil'),
                                   ('Maths', 'Maths'), ('Physics', 'Physics'),
                                   ('Chemistry', 'Chemistry'),
                                   ('Biology', 'Biology')],
                          )
    password = PasswordField('Password',
                             validators=[DataRequired(), EqualTo('password')])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = Teacher.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. \
                                  Please choose a different one.')

    def validate_email(self, email):
        user = Teacher.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. \
                                   Please choose a different one.')


class LoginForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    role = RadioField('Role', validators=[DataRequired()],
                      choices=[('Student', 'Student'),
                               ('Teacher', 'Teacher')],
                      default='choice1')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    standard = IntegerField('Standard',
                            validators=[DataRequired(),
                                        NumberRange(min=1, max=12)
                                        ]
                            )
    section = StringField('Section',
                          validators=[Length(min=1, max=1)], default='A')
    subject = SelectField('Subject: ',
                          choices=[('English', 'English'), ('Tamil', 'Tamil'),
                                   ('Maths', 'Maths'), ('Physics', 'Physics'),
                                   ('Chemistry', 'Chemistry'),
                                   ('Biology', 'Biology')],
                          default='English')
    picture = FileField('Update Profile Picture',
                        validators=[FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            if current_user.role == 'Teacher':
                user = Teacher.query.filter_by(username=username.data).first()
            else:
                user = Student.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('That username is taken. \
                                       Please choose a different one.')

    def validate_email(self, email, role='Teacher'):
        if email.data != current_user.email:
            if current_user.role == 'Teacher':
                user = Teacher.query.filter_by(username=email.data).first()
            else:
                user = Student.query.filter_by(username=email.data).first()
            if user:
                raise ValidationError('That email is taken. \
                                       Please choose a different one.')


class PostForm(FlaskForm):
    topic = StringField('Topic', validators=[DataRequired()])
    work = TextAreaField('Work to be done', validators=[DataRequired()])
    due_date = DateField('Due date', format='%Y-%m-%d')
    submit = SubmitField('Post')


class RequestResetForm(FlaskForm):
    email = StringField('Email',
                        validators=[DataRequired(), Email()])
    submit = SubmitField('Request Password Reset')

    def validate_email(self, email):
        user1 = Student.query.filter_by(email=email.data).first()
        user2 = Teacher.query.filter_by(email=email.data).first()
        if user1 is None and user2 is None:
            raise ValidationError('There is no account with that email. \
                                   You must register first.')


class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password')])
    submit = SubmitField('Reset Password')
