from flask import Flask, render_template
from flask_wtf import FlaskForm
from wtforms import StringField,SubmitField #string is input box, submit is the submit button
from wtforms.validators import DataRequired #Validate your inputs, points out when blank

app = Flask(__name__)
app.config['SECRET_KEY'] = "your_random_secret_key_here"



#create a form class
#for this we would also need a secret ket
#with forms, we have a csrf token that synchs up with your secret key to prevent hackers from hijacking your form
#all modern forms have csrf tokens
class NamerForm(FlaskForm):
    name =StringField("Whats your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")




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
        """
        So when somebody fills the form, take info from there and update my name vairable
        """

    return render_template('name.html',
                           name=name,
                           form=form)




@app.errorhandler(404)
def page_not_found(e):
    return "404 NOT FOUND",404

@app.errorhandler(500)
def page_not_found(e):
    return "500 NOT FOUND",500



if __name__ == "__main__":
    app.run(debug=True)
