from flask import Blueprint, render_template, request, redirect, url_for

from app.auth.forms import UserCreationForm
from app.models import User
auth = Blueprint('auth',__name__,template_folder='auth_templates')

@auth.route('/signup', methods=["GET","POST"])
def signMeUp():
    form = UserCreationForm()
    if request.method== "POST":
        if form.validate():
            username = form.username.data
            email = form.email.data
            password = form.password.data

            my_user = User(username, email, password)
            my_user.saveToDB()

            return redirect(url_for('auth.logMein'))
    return render_template('signup.html', form=form )

@auth.route('/login')
def logMein():
    return render_template('login.html')