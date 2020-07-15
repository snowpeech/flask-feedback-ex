from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import UserForm, FeedbackForm, LoginForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgres:///flask_fdbk"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()

toolbar = DebugToolbarExtension(app)


@app.route("/")
def homepage():
    """Redirect to register page"""

    return redirect("/register")

@app.route("/register", methods=["GET", "POST"])
def register_user():
    """Register user: produce form & handle form submission."""
    form = UserForm()

    if form.validate_on_submit():
        username = form.username.data
        pwd = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, pwd=pwd,email=email, first_name=first_name, last_name=last_name)
        db.session.add(new_user)
        
        # add error handling needed for username already exists
        try:
            db.session.commit()
        except IntegrityError:
            #you can except other types of errors and generate custom actions
            form.username.errors.append('Username/Email taken. Please pick another one')
            return render_template('register.html', form=form)


        session["username"] = new_user.username

        # on successful login, redirect to secret page
        return redirect(f"/users/{username}")

    else:
        return render_template("register.html", form=form)
    

@app.route("/login", methods=["GET", "POST"])
def login():
    """Produce login form or handle login."""

    form = LoginForm()

    if form.validate_on_submit():
        name = form.username.data
        pwd = form.password.data

        # authenticate will return a user or False
        user = User.authenticate(name, pwd)

        if user:
            flash(f"Welcome back {user.username}", 'success')
            session["username"] = user.username  # keep logged in
            return redirect(f"/users/{user.username}")

        else:
            form.username.errors = ["Invalid username/password"]

    return render_template("login.html", form=form)
# end-login    


@app.route("/users/<username>", methods=["GET","POST"])
def show_tweets(username):
    """Example hidden page for logged-in users only."""
    if "username" not in session:
        flash("You must be logged in to view!", 'danger')
        return redirect("/")
    user = User.query.get_or_404(username)

    posts = Feedback.query.filter_by(username=username)

    return render_template("profile.html", user=user, posts = posts)
    
#     form = TweetForm()
#     all_tweets = Tweet.query.all()
#         #every time we're printing out each tweet, it's a separate query? It would be better to just do one query using a JOIN

#     if form.validate_on_submit():
#         text=form.text.data 
#         new_tweet = Tweet(text=text, Username=session['username'])
#         db.session.add(new_tweet)
#         db.session.commit()
#         flash(f"Tweet Created!", 'success')
#         return redirect('/tweets')
#     #     # alternatively, can return HTTP Unauthorized status:
#     #     #
#     #     # from werkzeug.exceptions import Unauthorized
#     #     # raise Unauthorized()

#     # else:
#     return render_template("tweets.html", form=form, tweets=all_tweets)

# GET 
# Display a form to add feedback Make sure that only the user who is logged in can see this form
# POST /users/<username>/feedback/add
# Add a new piece of feedback and redirect to /users/<username> — Make sure that only the user who is logged in can successfully add feedback
@app.route("/users/<username>/feedback/add", methods=["GET", "POST"])
def add_feedback(username):
    if session['username'] != username:
        flash("You don't have permission to do this")
        return redirect('/login')
    
    form = FeedbackForm()

    return render_template("add_feedback.html", form=form)


@app.route("/users/<username>/delete", methods=["POST"])
def delete_user(username):
    if session['username'] != username:
        flash("You don't have permission to do that", 'danger')
        return redirect('/login')
    
    user = User.query.get_or_404(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username", None)
    flash("User and associated feedback deleted", 'info')
    return redirect('/')



@app.route("/tweets/<int:id>", methods=["POST"])
def delete_feedback(id):
    if 'username' not in session:
        flash("Please log in first", 'danger')
        return redirect('/login')

    tweet = Tweet.query.get_or_404(id)
    if tweet.username == session['username']:
        db.session.delete(tweet)
        db.session.commit()
        flash("Tweet deleted", 'info')
        return redirect('/tweets')
    
    flash("You don't have permission to do that", 'danger')
    return redirect('/tweets')



@app.route("/logout")
def logout_user():
    """Logs user out and redirects to homepage."""
    # Should be a post request... empty form with submitting post request. style as btn-link
    flash("Good bye!", 'primary')
    session.pop("username", None)

    return redirect("/")
# NTS:: IN BASE.HTML, set a default class for flash messages (if no category, category = x) look this up

#keep view logic clean!