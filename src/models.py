from flask_sqlalchemy import SQLAlchemy
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from app import app
from sqlalchemy import text
from sqlalchemy.sql import func
from flask_login import UserMixin

db = SQLAlchemy()

#users table
class users(db.Model, UserMixin):  
    user_id = db.Column(db.Integer, primary_key = True)

    first_name = db.Column(db.String(255), nullable = False)

    last_name = db.Column(db.String(255), nullable = False)

    username = db.Column(db.String(255), nullable = False)

    email = db.Column(db.String(255), nullable = False)

    password = db.Column(db.String(255), nullable = False)

    role = db.Column(db.String(255), nullable = True)

    registration_date = db.Column(db.DateTime, nullable=True, default=func.now())

    profile_picture = db.Column(db.String(255), nullable = True)


    def __init__(self, first_name: str, last_name: str, username: str, email:str , password: str):
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.email = email
        self.password = password

    def get_reset_token(self, expires_sec=900):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id' : self.user_id}).decode('utf-8')
    
    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return users.query.get(user_id)

    def __repr__(self) -> str:
        return f'users({self.first_name}, {self.last_name})'
    
    def get_id(self):
        return str(self.user_id)


#live posts table
class live_posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime(timezone=True), nullable = True, default = func.now())
    
    # Foreign key referencing the users table
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    
    # Establish the relationship with the User model
    user = db.relationship('users', backref=db.backref('live_posts', lazy=True))

    def __init__(self, content: str, user_id:int):
        self.content = content
        self.user_id = user_id

    def __repr__(self) -> str:
        return f'live_posts({self.post_id}, {self.content}, {self.user_id})'


#post
class Post(db.Model):
    # PRIMARY KEY post_id SERIAL,
    post_id = db.Column(db.Integer, primary_key = True)

    # title VARCHAR(255) NOT NULL,
    title = db.Column(db.String(255), nullable = False)

    # content TEXT,
    content = db.Column(db.Text, nullable = True)

    # date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_posted = db.Column(db.DateTime, nullable = False, server_default=text('NOW()'))

    # likes INT NOT NULL DEFAULT 0,
    likes = db.Column(db.Integer, nullable = True, default = 0)

    # image BLOB,
    file_upload = db.Column(db.String(255), nullable = True, default = 'default.jpg')

    # user_id INT,
    # FOREIGN KEY (user_id) references users(user_id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    # each user's posts
    posts = db.relationship('users', backref='posts')

    def __init__(self, title: str, content: str):
        self.title = title
        self.content = content

    # def __init__(self, user_id: int, title: str, content: str):
    #     self.user_id = user_id
    #     self.title = title
    #     self.content = content

    def __repr__(self) -> str:
        return f'Post #{self.post_id} by {self.user_id})'

#post comments
class Comment(db.Model):
    # PRIMARY KEY comment_id SERIAL,
    comment_id = db.Column(db.Integer, primary_key = True)

    # content TEXT,
    content = db.Column(db.Text, nullable = True)

    # date_posted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    date_posted = db.Column(db.DateTime, nullable = False, server_default=text('NOW()'))

    # likes INT NOT NULL DEFAULT 0,
    likes = db.Column(db.Integer, nullable = True, default = 0)

    # user_id INT,
    # FOREIGN KEY (user_id) references users(user_id)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable = False)

    # post_id INT,
    # FOREIGN KEY (post_id) references posts(post_id)
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable = False)

    # each user's comments
    user_comments = db.relationship('users', backref='user_comments', foreign_keys=[user_id])

    # each post's comments
    post_comments = db.relationship('Post', backref='post_comments', foreign_keys=[post_id])

    def __init__(self, user_id: int, post_id: int, content: str):
        self.user_id = user_id
        self.post_id = post_id
        self.content = content

    def __repr__(self) -> str:
        return f'{self.content}'