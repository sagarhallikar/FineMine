from flask import Flask, redirect, render_template,request, url_for, session
from form import  Allskills
from werkzeug.utils import secure_filename
import os
import json
import logging
import pymongo
from pymongo import MongoClient
# from flask_oauth import OAuth

from authlib.integrations.flask_client import OAuth

GOOGLE_CLIENT_ID = '306586400383-epc15d8u7679emu9pr0hj3d2hl001nnr.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
REDIRECT_URI = '/authorised'


SECRET_KEY = 'development key'
DEBUG = True


app = Flask(__name__)

oauth = OAuth(app)
app.config['UPLOAD_PATH'] = 'resume uploads'
# app.config['MAX_CONTENT_PATH'] 
app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.docx', '.doc']
app.config['MAX_CONTENT_LENGTH'] = 5120
app.config['SECRET_KEY'] = '915ba8d82820d39206ef0733d4387660'
app.config['GOOGLE_CLIENT_ID'] = "306586400383-t9chtte8h729gbksfms64e97720tsjgv.apps.googleusercontent.com"
app.config['GOOGLE_CLIENT_SECRET'] = "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"

google = oauth.register(
    name = 'google',
    client_id = app.config["GOOGLE_CLIENT_ID"],
    client_secret = app.config["GOOGLE_CLIENT_SECRET"],
    access_token_url = 'https://accounts.google.com/o/oauth2/token',
    access_token_params = None,
    authorize_url = 'https://accounts.google.com/o/oauth2/auth',
    authorize_params = None,
    api_base_url = 'https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint = 'https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs = {'scope': 'openid email profile'},
    server_metadata_url=f'http://127.0.0.1:8008/authorised'
)


# Connecting Database
try:
    mongo = pymongo.MongoClient(
        host = "localhost",
        port = 27017,
        serverSelectionTimeoutMS = 1000
    )
    db = mongo.finewebapp
    
    mongo.server_info() #trigger exception if cannot connect to db
except:
    print("ERROR")

logging.basicConfig(level=logging.INFO)

@app.route('/venky')
def venky():
    return "venky returned something"

@app.route(REDIRECT_URI)
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('index'))


@app.route('/')
def index():
    # access_token = session.get('access_token')
    # if access_token is None:
    #     return redirect(url_for('login'))

    return render_template('home.html')


# @app.route('/login')
# def login():
#     callback=url_for('authorized', _external=True)
#     return google.authorize(callback=callback)

@app.route('/login')
def login():
    google = oauth.create_client('google')
    redirect_uri = url_for('google_authorize', _external=True)
    print(redirect_uri)
    return google.authorize_redirect(redirect_uri)


# Google authorize route
@app.route('/login/google/authorize')
def google_authorize():
    google = oauth.create_client('google')
    try:
        token = google.authorize_access_token()
        session["user"] = token
        resp = google.get('userinfo').json()
        print(f"\n{resp}\n")
        return "You are successfully signed in using google"
    except Exception as ex:
        print(ex)
        return 'HEllo'

@app.route("/logout")
def logout():
    session.clear()
    return redirect("home", _external=True)

def get_access_token():
    return session.get('access_token')


@app.route('/home',methods=['GET','POST'])
def home():
    if request.method == 'POST':
        return render_template('home.html')
    else:
        return render_template('home.html')

  
@app.route('/test', methods = ['POST'])
def test():
    return render_template('home.html')

# @app.route('/login', methods=['GET','POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         if form.email.data =='rose@gmail.com' and form.password.data =='Rose@123':
#             flash('Account logged In Successfully!','success')
#             return redirect(url_for('home'))
#         else:
#             flash('Login Unsuccessfully. Please check the email and password!','danger')
#     return render_template('signin.html',title = 'Login', form =form)
     
@app.route('/allskills',methods=['GET','POST']) 
def allskills():
    form = Allskills()
            
    if form.validate_on_submit():
        newuser = {
            "candidate name":request.form["candidatename"],
            "emailid":request.form["email"],
            "contact":request.form["contact"],
            "resume_file":request.form["resume"]
            }
        print(newuser)
        dbResponse = db.allskills_db.insert_one(newuser)
        print(dbResponse.inserted_id)
        return render_template('home.html')

    # if request.method == 'POST':
    #     uploaded_file = request.files['resume']
    #     filename = secure_filename(uploaded_file.filename)
    #     if filename != '':
    #         file_ext = os.path.splitext(filename)[1]
    #         if file_ext not in app.config['UPLOAD_EXTENSIONS']:
    #             abort(400)
    #         uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
    #     return render_template('allskills.html',form = form)
    # else:
    #     flash("Please Sign In!!",'success')
    #     return redirect('home')
    
# @app.route('/sift',methods="['GET','POST']") 
# def sift():
#     form = Sift()
#     return render_template('sift.html')

# @app.route('/collate',methods="['GET','POST']") 
# def collate():
#     form = Collate()
#     return render_template('collate.html')

if __name__ == '__main__':
   app.run(debug=True, port = 8008)
 
