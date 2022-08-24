@app.route('/upload',methods = ['POST'])
def upload():
    if request.method == 'POST':
        form = Allskills()
        if request.form['submit']:    
            uploadfile = request.files.get('resume')
           
            if not uploadfile:
                print('True')
            filename = uploadfile.filename
            # print(filename)

            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    # abort(400)
                    pass
                # uploadfile.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                
                newdata = {
                    "candidate_name":request.form["candidatename"],
                    "c_email_id":request.form["email"],
                    "contact_no":request.form["contact"],
                    "filename":filename,
                    "uploadfile" :base64.b64encode(bytes(uploadfile.read()))

                }
                
                dbResponse = db.allskills_db.insert_one(newdata)
                print(dbResponse.inserted_id)
            return redirect('allskills')
        return render_template('home.html')


def extractall():
    pdfFileObj = open('uploads/MyResume.pdf', 'rb')
    pdfReader = PyPDF2.PdfFileReader(pdfFileObj) 
    with open('uploads/MyResume.pdf','rb') as pdf_file:
        read_pdf = PyPDF2.PdfFileReader(pdf_file)
        number_of_pages = read_pdf.getNumPages()
        page_content_acc = ''
        for page_number in range(number_of_pages):   # use xrange in Py2
            page = read_pdf.getPage(page_number)
            page_content = page.extractText()
            page_content_acc = page_content_acc + page_content
            print(page_content)

    cont1 = re.sub('[^A-Za-z0-9]+', ' ', page_content_acc)
    print(cont1)
    programming_lang = ["Javascript","Python","C","Java","Go", "Perl", "Ruby","swift", "Scala", "PHP", "C++", "R programming","Objective C", "SQL","Structured Query Language"," Arduino","MATLAB","Rust","Typescript","Kotlin","CSS","Groovy","Dart","Powershell","Julia","Scratch","COBOL","Fortron", "Shell","Prolog","VBScript","Haskell","Delphi","Hack","PASCAL","ADA","LUA","Visual Basic","Lisp","Bash","SAS Programming","C#"]
    web_technologies = ["MEAN stack","PHP","Django","Ruby","React.js","HTML","Node.Js", "React", "ASP.NET","Laravel", "Swift", "Go", "Vue","React", "Angular", "Ember", "JQuery","Structured Query Language","Java","AngularJS","Rust","Typescript","Kotlin","CSS","C#"]
    databasesmgmt = ["Oracle Database","IBM DB2","Microsoft Sql server","MySQL","FileMaker Pro","Microsoft Access","SQLite","PostgresSQL", "MongoDB", "Redis","CouchDB", "Neo4j"]
    tools = ["Microsoft Excel","Scalyr","Rudder","Github","Graylog","Docker","UpGuard","Jenkins","Puppet","QuerySurge","Solarwinds DevOps","Vagrant","PagerDuty","Prometheus","Ganglia","Snort","Splunk","Nagios","Chef","Sumo Logic","OverOps","Consul","Stackify Retrace","CFEngine","Artifactory","Capistrano","Monit","Supervisor","Ansible","Code Climate","Icinga","New Relic APM","Juju","ProductionMap","Kubernetes","Git","Gradle","Kibana","Salt","Monit","Terraform","Bitbucket","Microsoft Power BI","Tableau Desktop","R Studio","SAS Studio","R Studio","Infogram","ChartBlocks","Datawrapper","D3.js","Domo","Google Charts","FusionCharts","Chart.js","Sisense","Workday Adaptive Planning","Grafana","Plecto","Whatagraph","Cluvio","RAWGraphs","Visually","looker","Chartist.js","Sigma.js","Qlik","Polymaps","Zoho Analytics","Databox","ChartBlocks","Datawrapper"," Plotly","Visually"," Ember Charts"," NVD3"," Highcharts","Leaflet","Hubspot","Spotfire","Dundas Data Visualization"]
    Script_lang = ["JavaScript","PHP","C#","Python","Ruby","Groovy","Perl","Lua","Bash","PowerShell","R","VBA","Emacs Lisp","GML","ECMAScript","Mscript","Julia","tcsh","Nim","POSIX shell","Tcl"]
    Front_end = [" React", "Javascript", "CSS", "HTML", "AngularJS", "Vue","Vue.js", "SASS", "Swift", "Elm","jQuery"]
    Data_Science = ["Machine Learning","NoSQL","SPSS" ,"Data Mining","Technical","SQL","Statistics","Python","Deep Learning","Big Data","Spark","NLP","AWS","Tabeleau","Natural Language Processing","Google Cloud Platform","GCP","Cloud Computing","NoSQL","Microsoft Azure","Microsoft Power BI","SAP","AI","Artificial Intelligence","Microsoft Excel"]
    Frameworks = ["Angular","ASP.NET","ASP.NET Core","Express","Vue","Spring","Django","Flask","Laravel","Ruby on Rails","Symfony","Gatsby","Sinatra","CakePHP","Horde","Yii","Zend","Zikula","Bootstrap","Grails","Play","Web2py","Lumen","TurboGears","Phalcon","FuelPHP","Spark:","Grok","Mojoloicious","Fat-Free Framework","Wicket","Yesod","Sencha Ext JS","Nuxt.js","Phoenix","CodeIgniter","PHPixie","Javalin","Silex","Caliburn Micro","Ionic","Xamarin","PhoneGap","React Native ","Corona","jQuery Mobile","Flutter","Mobile Angular UI","Appcelerator Titanium","Swiftic","NativeScript","Framework 7","Rachet","PyTorch","Neural Network Libraries","Neural Network Libraries","Apache MXNet","ML.NET","Infer.NET","Accord.NET","Chainer","Horovod","H2O Q","Robot Framework","Gauge","Pytest","Jest","Mocha","Jasmine","Nightwatch","Protractor","Protractor","TestProject","Galen Framework","WebDriverIO","OpenTest","Citrus","Karate","Scrapy","Truffle","Embark","Etherlime","OpenZeppelin Contracts","Brownie","Create Eth App","Exonum","Hyperledger","Corda","MultiChain","Meteor","Onsen UI","SiteWhere","Electron","Svelte","Aurelia","Mithril","Bulma","Microdot","Rapidoid","Ktor","Scalatra","Toolatra"]
    print("--------------------------------------------------------") 
    allskills = programming_lang + web_technologies + databasesmgmt + tools + Script_lang + Front_end + Data_Science + Frameworks
    print(allskills)
    print("--------------------------------------------------------")
    exist_skills = set(filter(lambda x : x in cont1 , allskills))
    print(list(exist_skills))





import email
import json
import os
from os import environ as env
from form import Allskills
from urllib.parse import quote_plus, urlencode

import base64
import gridfs
import streamlit as st
import pymongo
from pymongo import MongoClient
from wand.image import Image
from PyPDF2 import PdfFileReader,PdfFileWriter
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename
from flask import Flask, redirect, render_template, session, url_for,request,send_file



app = Flask(__name__)
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))

oauth = OAuth(app)

GOOGLE_CLIENT_ID = '306586400383-epc15d8u7679emu9pr0hj3d2hl001nnr.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
REDIRECT_URI = '/authorised'



app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.docx', '.doc']
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*1024
app.config['UPLOAD_PATH'] = 'uploads'

app.config['SECRET_KEY'] = '915ba8d82820d39206ef0733d4387660'

AUTH0_DOMAIN = "dev-lo037ct9.us.auth0.com"

oauth.register(
    "auth0",
    client_id="4V7po4RZpByuYfbstRa4Uu2mygNfznmF",
    client_secret="R44IwXpf7_3ZnfaCHIBFyJPHpOF9UFXeLa1zWpNUJgSI--vnMCTBLPU8XtTpLsrk",
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
)

SECRET_KEY = 'development key'
DEBUG = True

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

fs = gridfs.GridFS(db)
    # Standard query to Mongo


def write_new_pdf(path):
    # db = MongoClient('mongodb://localhost:27017/').myDB
    fs = gridfs.GridFS(db)
    # Note, open with the "rb" flag for "read bytes"
    with open(path, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    # with fs.new_file(
    #     chunkSize=800000,
    #     filename='prami') as fp:
    #     fp.write(encoded_string)
    #     print(fp)
    return encoded_string

def read_pdf(filename):
    # Usual setup
    # db = MongoClient('mongodb://localhost:27017/').myDB
    pass


# def prepare_images(pdf_path):
#     # Output dir
#     output_dir = os.path.join(APP_ROOT, 'static/pdf_image/')

#     with(Image(filename=pdf_path, resolution=300, width=600)) as source:
#         images = source.sequence
#         pages = len(images)
#         for i in range(pages):
#             Image(images[i]).save(filename=output_dir + str(i) + '.png')



@app.route("/")
def home():
    # form  = Allskills()
    print("-----------------------------------")
    return render_template('home.html')
    # print("-----------------------------------")
    # return render_template('home.html')

@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("callback", _external=True)
    )


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    # print(token)
    return redirect("/")

@app.route("/logout")
def logout():
    session.clear()
    # return redirect(
    #     "https://" + env.get("AUTH0_DOMAIN") + "/v2/logout?"
    #     + urlencode(
    #         {
    #             "returnTo": url_for("home", _external=True),
    #             "client_id": env.get("AUTH0_CLIENT_ID"),
    #         },
    #         quote_via=quote_plus,
    #     )
    # )
    return render_template('home.html')

@app.route('/allskills',methods=['GET','POST']) 
def allskills():
    form = Allskills()
    if session.get("user"):
        # if request.form['submit']:
        #     newuser = {
        #         "candidate name":request.form["candidatename"],
        #         "emailid":request.form["email"],
        #         "contact":request.form["contact"],
        #         "resume_file":request.form["resume"]
        #      }
        #     print(newuser)
            return render_template('allskills.html', form = form)
            # dbResponse = db.allskills_db.insert_one(newuser)
        # elif request.form['submit']:
        #     pass     
    else:
        return redirect('login')

def sample():
    form = sample()
    if session.get("user"):
            return render_template('sample.html', form = form)    
    else:
        return redirect('login')

@app.route('/download')
def downloadFile ():
    
    # Standard query to Mongo
    data = db.allskills_db.find_one(filter=dict(contact_no="78457956415"))
    
    with open('uploads/'+data["filename"], "wb") as f:
        f.write(base64.b64decode(data['uploadfile']))
 
    path = "uploads/"+data["filename"]
    return send_file(path, as_attachment=True)



@app.route('/upload',methods = ['POST'])
def upload():
    if request.method == 'POST':
        # print('C1')
        form = Allskills()
        # print('C2')
        if request.form['submit']:
            # print('C3')
      
            uploadfile = request.files.get('resume')
            print("---------------------------------------------")
            # print(type(bytes(uploadfile)))
            print("---------------------------------------------")
            if not uploadfile:
                print('True')
            filename = uploadfile.filename
            # print(filename)

            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                    # abort(400)
                    pass
                # uploadfile.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                
                newdata = {
                    "candidate_name":request.form["candidatename"],
                    "c_email_id":request.form["email"],
                    "contact_no":request.form["contact"],
                    "filename":filename,
                    "uploadfile" :base64.b64encode(bytes(uploadfile.read()))

                }
                
                # print(newdata)
                dbResponse = db.allskills_db.insert_one(newdata)
                print(dbResponse.inserted_id)
            return redirect('allskills')
        return render_template('home.html')




# @app.route('/display/<filename>')
# def display_pdf(filename):
# 	#print('display_image filename: ' + filename)
# 	return redirect(url_for('static', filename='uploads/' + filename), code=301)


# def show_pdf(file_path):
#     with open(file_path, "rb") as f:
#         base64_pdf = base64.b64encode(f.read()).decode('utf-8')
#     # pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
#     pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf"></iframe>'
#     st.markdown(pdf_display, unsafe_allow_html=True)


if __name__ == '__main__':
       app.run(debug=True, port = 8008)
 
