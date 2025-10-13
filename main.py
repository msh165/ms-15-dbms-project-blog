from flask import Flask, render_template,flash,request #flash is for flashing messages on top, success, rejects
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField,PasswordField,BooleanField,ValidationError #string is input box, submit is the submit button
from wtforms.validators import DataRequired,EqualTo,Length #Validate your inputs, points out when blank

from flask_sqlalchemy import SQLAlchemy

from datetime import datetime 

from flask_migrate import Migrate

from werkzeug.security import check_password_hash,generate_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_random_secret_key_here"

#Old SQLITE DB
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'#Points to where our database is stored

#New MYSQL DB FORMAT OF URI is username/password@host/name of db
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost/users'


db = SQLAlchemy(app)
migrate= Migrate(app,db)
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



#Creating our model
class Users(db.Model):
    id = db.Column(db.Integer,primary_key = True, )
    name = db.Column(db.String(200), nullable = False)
    email = db.Column(db.String(120), nullable= False, unique=True)
    color = db.Column(db.String(120))
    date_added = db.Column(db.DateTime, default = datetime.now())
    
    password_hash = db.Column(db.String(120))


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




#UPDATE DATABASE RECORD
@app.route("/update/<int:id>",methods=["GET",'POST'])
def update(id):
    form = UserForm()
    user_to_update = Users.query.get_or_404(id)
    #search by what the user input into url
    print("HERE")
    if request.method=="POST":
        user_to_update.name = request.form['name']
        user_to_update.email= request.form['email']
        user_to_update.color= request.form['color']
        try:
            db.session.commit()
            flash(f"User with Name {user_to_update.name} updated Successfully!")
            all_users = Users.query.order_by(Users.date_added)
            return render_template("add_user.html", form=form,all_users=all_users)
        
        except Exception as e:
            flash(e)
            return render_template("update.html", form=form,user_to_update=user_to_update.name)
    else:
        return render_template("update.html", form=form,user_to_update=user_to_update)




@app.route("/delete_user/<int:id>")
def delete_user(id):
    user_to_delete = Users.query.get_or_404(id)
    form = UserForm()
    all_users = Users.query.order_by(Users.date_added)
    
    try:
        db.session.delete(user_to_delete)
        db.session.commit()
        flash("User successfully deleted!")
        return render_template("add_user.html",form=form,all_users = all_users)

    except Exception as e:
        flash(e)
        return render_template("add_user.html",form=form,all_users = all_users)






@app.route("/")
def home():
    return render_template('index.html')
    # return "Hey"

@app.route("/name",methods = ['GET','POST'])
def name():
    name= None# why we did this?
    #when the page loads for the first time, there would be no name.
    #THat would be input by the user, but our render template expects a name
    #hence we are adding the variable, which would then get replaced y the user input
    form = NamerForm() #this is our form class we created above

    #validate stuf
    if form.validate_on_submit():
        name = form.name.data
        form.name.data=''
        flash("Form successfully filled")
        """
        So when somebody fills the form, take info from there and update my name vairable
        """

    return render_template('name.html',
                           name=name,
                           form=form)


@app.route("/user/add", methods = ["POST","GET"])
def add_user():
    name = None
    email = None
    color = None
    form = UserForm()
    if form.validate_on_submit():
        #we need to check the other users dont have the same email
        user = Users.query.filter_by(email=form.email.data).first()
        #it is filtering the users table to get rows matching iwth email input
        #if we get null output, then email DNE and user can be created

        if user is None:
            print(f"Password for {form.name.data} is {generate_password_hash(form.password_hash.data)}")
            hashed_pw = generate_password_hash(form.password_hash.data,"asd123")
            user = Users(
                name = form.name.data,
                email = form.email.data,
                color = form.color.data,
                password_hash = hashed_pw 
            )
            db.session.add(user)
            db.session.commit()
            flash("User Added successfuly")
        else:
            flash(f"Email ID {form.email.data} already exists")
        name = form.name.data #we do this to give a confirmation
        form.name.data=''
        form.email.data=''
        form.color.data=''
        form.password_hash.data=''
        form.password_hash2.data=''
    all_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form,name=name,all_users=all_users)



@app.errorhandler(404)
def page_not_found(e):
    return "404 NOT FOUND",404

@app.errorhandler(500)
def page_not_found(e):
    return "500 NOT FOUND",500



if __name__ == "__main__":
    with app.app_context():
        db.create_all()


    app.run(debug=True)
