from __init__ import app, db
from models import Users, Posts, UserForm, PostForm, PasswordForm
# ...rest of your routes.py code...

from flask import render_template,flash,request,redirect,url_for

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

@app.route("/test_pw",methods = ['GET','POST'])
def test_pw():
    email = None
    password_hash= None# why we did this?
    pw_to_check = None
    passed = None
    form = PasswordForm()
    
    #when the page loads for the first time, there would be no name.
    #THat would be input by the user, but our render template expects a name
    #hence we are adding the variable, which would then get replaced y the user input
    # form = NamerForm() #this is our form class we created above

    #validate stuf
    if form.validate_on_submit():
        email = form.email.data
        password = form.password_hash.data
        form.email.data=''
        form.password_hash.data=''

        pw_to_check = Users.query.filter_by(email=email).first()
        # print(pw_to_check.password_hash)

        passed = check_password_hash(pw_to_check.password_hash,password)
        print(passed)
        flash("Form successfully filled")
        """
        So when somebody fills the form, take info from there and update my name vairable
        """

    return render_template('test_pw.html',
                           email=email,
                           password_hash = password_hash,
                           passed = passed,
                           pw_to_check = pw_to_check,
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
            print("Inside here1")
            print(f"Password for {form.name.data} is {generate_password_hash(form.password_hash.data)}")
            hashed_pw = generate_password_hash(form.password_hash.data)
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
            print("Inside here2")
            flash(f"Email ID {form.email.data} already exists")
        name = form.name.data #we do this to give a confirmation
        form.name.data=''
        form.email.data=''
        form.color.data=''
        form.password_hash.data=''
        form.password_hash2.data=''
    all_users = Users.query.order_by(Users.date_added)
    return render_template("add_user.html", form=form,name=name,all_users=all_users)


@app.route("/posts/<int:id>")
def post(id):
    post = Posts.query.get_or_404(id)
    return render_template("post.html",post=post)


@app.route("/posts")
def posts():
    posts=Posts.query.order_by(Posts.date_posted)
    return render_template('posts.html',posts=posts)


#Add Post Page
@app.route('/add-post',methods = ["GET","POST"])
def add_post():
    form = PostForm() 

    if form.validate_on_submit():
        post = Posts(
            title = form.title.data,
            content = form.content.data,
            author = form.author.data,
            slug = form.slug.data
        )
        
        #Clear the form
        form.title.data = ''
        form.content.data = ''
        form.author.data = ''
        form.slug.data = ''
        
        #add post data to db
        db.session.add(post)
        db.session.commit()
        flash("Blog post submitted successfully")
    return render_template('add_post.html',form=form)


@app.route('/posts/edit/<int:id>',methods=["GET","POST"])
def edit_post(id):
    post = Posts.query.get_or_404(id)
    form = PostForm()
    if form.validate_on_submit(): #This is after they have clicked submit and been validated by flask
        #hence we are assigning values filled in the form to post
        post.title = form.title.data
        post.content = form.content.data
        post.author = form.author.data
        post.slug = form.slug.data

        #updated DATabase
        db.session.add(post)
        db.session.commit()
        flash("POST HAS BEEN UPDATED")
        return redirect(url_for('post',id=post.id)) #after editing be redirected to current post
    else:
        form.title.data = post.title
        form.content.data = post.content
        form.author.data = post.author
        form.slug.data = post.slug
        return render_template('edit_post.html',form=form)

@app.route('/posts/delete/<int:id>',methods=["GET",'POST'])
def delete_post(id):
    post_to_delete = Posts.query.get_or_404(id)

    posts=Posts.query.order_by(Posts.date_posted)#This is called as we need something to display after file has been deleted or error is shown
    try:
        db.session.delete(post_to_delete)
        db.session.commit()
        flash("Post Successfully deleted!")
        return render_template('posts.html',posts=posts)
    except Exception as e:
        flash(e)
        return render_template('posts.html',posts=posts)

@app.errorhandler(404)
def page_not_found(e):
    return "404 NOT FOUND",404

@app.errorhandler(500)
def page_not_found(e):
    return "500 NOT FOUND",500


