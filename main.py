from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def home():
    first_name = "Sehal"
    food = ["Pizza","Burger","Fries"]
    return render_template("index.html", first_name=first_name, food=food)


@app.route('/user/<name>')
def user(name):
    return f"<h1>Hello there  {name} </h1>"



if __name__ == "__main__":
    app.run(debug=True)
