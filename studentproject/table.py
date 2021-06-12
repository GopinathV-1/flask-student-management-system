from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from studentproject import db, app, create
from flask_login import UserMixin


class Student(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False, default='Student')
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default_student.jpg')
    password = db.Column(db.String(60), nullable=False)
    standard = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(1), nullable=False)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            print(Exception)
            return None
        return Student.query.get(user_id)

    def __repr__(self):
        return f"Student('{self.username}', '{self.standard}',\
                         '{self.section}', '{self.image_file}',\
                         '{self.role}')"


class Teacher(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    role = db.Column(db.String(10), nullable=False,  default='Teacher')
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default_teacher.jpg')
    password = db.Column(db.String(60), nullable=False)
    standard = db.Column(db.Integer, nullable=False)
    subject = db.Column(db.String(20), nullable=False)
    posts = db.relationship('Assignment', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except Exception:
            return None
        return Teacher.query.get(user_id)

    def __repr__(self):
        return f"Teacher('{self.username}', '{self.subject}',\
                         '{self.standard}', '{self.image_file}',\
                         '{self.role}')"


class Assignment(db.Model):
    __searchable__ = ['topic']

    id = db.Column(db.Integer, primary_key=True)
    topic = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    standard = db.Column(db.Integer, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    due_date = db.Column(db.Date, nullable=False)
    work = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('teacher.id'),
                        nullable=False)

    def __repr__(self):
        return '<Assignment %r>' % self.topic


try:
    create.create()
except Exception as e:
    print(e)
