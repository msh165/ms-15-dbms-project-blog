
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError,TextAreaField #string is input box, submit is the submit button
from wtforms.validators import DataRequired,EqualTo,Length #Validate your inputs, points out when blank
from flask_wtf import FlaskForm
from werkzeug.security import check_password_hash,generate_password_hash
from datetime import datetime 

from main import *
from __init__ import db
# ...rest of your models.py code...

class UserForm(FlaskForm):
    name =  StringField("Name", validators=[DataRequired()])
    email = StringField("Email", validators=[DataRequired()])
    color = StringField("Color", validators=[DataRequired()])
    password_hash = PasswordField('Password',
                                  validators=[DataRequired(),
                                              EqualTo('password_hash2',
                                                      message='Passwords must match')])
    password_hash2 = PasswordField('Confirm Password',validators=[DataRequired()])
    submit = SubmitField("Submit")

#create a form class
#for this we would also need a secret ket
#with forms, we have a csrf token that synchs up with your secret key to prevent hackers from hijacking your form
#all modern forms have csrf tokens
class NamerForm(FlaskForm):
    name =StringField("Whats your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PasswordForm(FlaskForm):
    email =StringField("Email", validators=[DataRequired()])
    password_hash =PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


class PostForm(FlaskForm):
    title = StringField("Title",validators=[DataRequired()])
    content = TextAreaField("content",validators=[DataRequired()])
    author = StringField("author",validators=[DataRequired()])
    slug = StringField("slug",validators=[DataRequired()])
    submit = SubmitField("Submit")




#Creating our model
class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True, )
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable= False, unique=True)
    color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default = datetime.now())
    
    password_hash = db.Column(db.String(512))


    # This is a "getter" method. 
    # It PREVENTS you from reading the password attribute directly.
    # If you try to do `user.password`, it will raise an error.
    # This is a security measure so you don't accidentally expose the password.
    @property
    def password(self):
        raise AttributeError('Password is not a readable attribute')

    # This is a "setter" method.
    # When you set a password (e.g., `user.password = 'my_secret_password'`), 
    # this function is automatically called.
    # It takes the plain text password ('my_secret_password'), hashes it,
    # and saves the resulting hash into the `password_hash` column.
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # This is a regular method to check if a submitted password is correct.
    # It takes a plain text password from a login form,
    # hashes it, and compares it to the `password_hash` stored in the database.
    # It returns True if they match, and False if they don't.
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)

    def  __repr__(self):#this tells the name of the table that can be called
        return super().__repr__()





#Creating a blog post model
class Posts(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text)
    author = db.Column(db.String(255))
    date_posted = db.Column(db.DateTime,default = datetime.now())

    slug = db.Column(db.String(255))#Slug appears in the URL bar, looks better than just the post_id


