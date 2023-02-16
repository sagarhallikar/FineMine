
from csv import reader
from distutils.log import error
import email
import json
import os
from os import environ as env
from secrets import choice
from form import Allskills, Sample,SortAll
from urllib.parse import quote_plus, urlencode
import re
import base64
import gridfs
import streamlit as st
import pymongo
from pymongo import MongoClient
from wand.image import Image
from PyPDF2 import PdfReader,PdfFileWriter
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename
from flask import Flask, redirect, render_template, session, url_for,request,send_file
import PyPDF2
import codecs
import secrets


app = Flask(__name__)
# APP_ROOT = os.path.dirname(os.path.abspath(__file__))

oauth = OAuth(app)

GOOGLE_CLIENT_ID = '500806758570-htr8muhock4srktapvq725cq8n7r1msm.apps.googleusercontent.com'
GOOGLE_CLIENT_SECRET = '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'
REDIRECT_URI = '/authorised'



app.config['UPLOAD_EXTENSIONS'] = ['.pdf', '.docx', '.doc']
app.config['MAX_CONTENT_LENGTH'] = 1024*1024*1024
app.config['UPLOAD_PATH'] = 'uploads'

app.config['SECRET_KEY'] = secrets.token_hex(32)

AUTH0_DOMAIN = "dev-ypbqn1iuzj4k6hib.us.auth0.com"

oauth.register(
    "auth0",
    client_id="LIbriPvpFZO1lJziqumNIS2FHwViQQOe",
    client_secret="Tc4YJgW_KZOnsP928MerxiEkWaDHkTIQvvwjcCqRnnwIGegq7vNO9NR6TUCTB1FT",
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{AUTH0_DOMAIN}/.well-known/openid-configuration'
)

SECRET_KEY = 'development key'
DEBUG = True

try:
    mongo = pymongo.MongoClient("mongodb://localhost:27017/FineMine")
    #     host = "localhost",
    #     port = 27017,
    #     serverSelectionTimeoutMS = 1000
    # )
    db =mongo.get_database()
    collection = db.get_collection('BinaryDatas')
    
    mongo.server_info() #trigger exception if cannot connect to db
except:
    print("ERROR")

fs = gridfs.GridFS(db)

def write_new_pdf(path):
    fs = gridfs.GridFS(db)    
    with open(path, "rb") as f:
        encoded_string = base64.b64encode(f.read())
    return encoded_string

@app.route("/")
def home():    
    return render_template('home.html')

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
    return render_template('home.html')

@app.route('/allskills',methods=['GET','POST']) 
def allskills():
    form = Allskills()
    if session.get("user"):
        return render_template('allskills.html', form = form)               
    else:
        return redirect('login')

@app.route('/sift',methods = ['GET','POST'])
def sift():
    form = Sample()
    if session.get("user"):
        return render_template('samples.html', form = form)    
    else:
        return redirect('login')

@app.route('/getdata',methods= ['POST'])
def getdata():
    if request.method == 'POST': 
        errors = None 
        output = []      
        form = Sample()        
        if request.form['Get_data']:     
            # con = request.form['contact']
            check = db.allskills_db.find_one(filter=dict(contact_no=request.form['contact']))            
        # [('default', '                 '),
        #  ('AS', 'All Skills'), 
        # ('Prg_lang', 'Programming Language'), 
        # ('WT', 'Web Technologies'),
        #  ('db', 'Database Management'), 
        # ('tl', 'Tools'), 
        # ('Scpt_lang', 'Scripting Language'), 
        # ('Frnt_nd', 'Front End Technologies'), 
        # ('DS', 'Data Science'), 
        # ('Frm_wks', 'Frameworks')]

        if check == None:
            errors = "Details are not available , Please check your contact number!"
        elif  request.form.get('sort') == 'AS':            
            output = check["allskills"]
        elif request.form.get('sort') == 'Prg_lang':
            output = check["prglang"]
        elif request.form.get('sort') == 'WT':
            output = check["web"]
        elif request.form.get('sort') == 'db':
            output = check["db"]
        elif request.form.get('sort') == 'tl':
            output = check["tools_only"]
        elif request.form.get('sort') == 'Scpt_lang':
             output = check["script"]
        elif request.form.get('sort') =='Frnt_nd':
            output = check["front"]
        elif request.form.get('sort') == 'DS':
            output = check["ds"]
        elif request.form.get('sort') == 'Frm_wks':
            output = check["framework"]       
        return render_template('samples.html', form = form, data = output, error = errors )
    return render_template('home.html')
    

@app.route('/sortall',methods = ['GET','POST'])
def sortall():
    form = SortAll()
    if session.get("user"):
        return render_template('sortAll.html', form = form)    
    else:
        return redirect('login')

@app.route('/getall',methods = ['POST'])
def getall():
    if request.method == 'POST': 
            errors = None 
            result = []      
            form = SortAll()       
            x = request.form.get('sort_al') 
            y =''
            if  x == 'AS':            
                y = "allskills"
            elif x == 'Prg_lang':
                y = "prglang"
            elif x == 'WT':
                y = "web"
            elif x == 'db':
                y = "db"
            elif x == 'tl':
                y = "tools_only"
            elif x == 'Scpt_lang':
                y = "script"
            elif x =='Frnt_nd':
                y = "front"
            elif x == 'DS':
                y = "ds"
            elif x == 'Frm_wks':
                y = "framework"

            if request.form['Get_all']:               
                result = db.allskills_db.find({},{'_id':0,'candidate_name':1, y:1})
                result1 = []
                # print(result)
                for s in result:
                    print(s) 
                    result1.append(s)                                                                                
            return render_template('sortAll.html', form = form, data = result1, error = errors )
    return render_template('home.html')


@app.route('/download')
def downloadFile ():
    # i =var 
    data = db.allskills_db.find_one(filter=dict(contact_no="07019328368"))
    
    with open('uploads/'+data["filename"], "wb") as f:
        f.write(base64.b64decode(data['uploadfile']))
 
    path = "uploads/"+data["filename"]
    return send_file(path, as_attachment=True)



@app.route('/upload',methods = ['POST'])
def upload():
    if request.method == 'POST':        
        form = Allskills()        
        if request.form['submit']:        
            uploadfile = request.files.get('resume')
            
            if not uploadfile:
                print('True')
            filename = uploadfile.filename         

            if filename != '':
                file_ext = os.path.splitext(filename)[1]
                
                if file_ext not in app.config['UPLOAD_EXTENSIONS']:            
                    pass
                # uploadfile.save(os.path.join(app.config['UPLOAD_PATH'], filename))
                
                # with codecs.open(bytes(uploadfile.read()), 'rb', encoding='utf-8',errors='ignore') as fdata:
                      
                read_pdf = PyPDF2.PdfReader(uploadfile)
                number_of_pages = len(read_pdf.pages)
                page_content_acc = ''
                for page_number in range(number_of_pages):   # use xrange in Py2
                    page = read_pdf.pages[page_number]
                    page_content = page.extract_text()
                    page_content_acc = page_content_acc + page_content
                    # print(page_content)

                cont1 = re.sub('[^A-Za-z0-9]+', ' ', page_content_acc)
                # print(cont1)
                programming_lang = ["Javascript","Python","C","Java","Go", "Perl", "Ruby","swift", "Scala", "PHP", "C++", "R programming","Objective C", "SQL","Structured Query Language"," Arduino","MATLAB","Rust","Typescript","Kotlin","CSS","Groovy","Dart","Powershell","Julia","Scratch","COBOL","Fortron", "Shell","Prolog","VBScript","Haskell","Delphi","Hack","PASCAL","ADA","LUA","Visual Basic","Lisp","Bash","SAS Programming","C#"]
                web_technologies = ["MEAN stack","PHP","Django","Ruby","React.js","HTML","Node.Js", "React", "ASP.NET","Laravel", "Swift", "Go", "Vue","React", "Angular", "Ember", "JQuery","Structured Query Language","Java","AngularJS","Rust","Typescript","Kotlin","CSS","C#"]
                databasesmgmt = ["Oracle Database","IBM DB2","Microsoft Sql server","MySQL","SQL","FileMaker Pro","Microsoft Access","SQLite","PostgresSQL", "MongoDB", "Redis","CouchDB", "Neo4j"]
                tools = ["Microsoft Excel","Scalyr","Rudder","Github","Graylog","Docker","UpGuard","Jenkins","Puppet","QuerySurge","Solarwinds DevOps","Vagrant","PagerDuty","Prometheus","Ganglia","Snort","Splunk","Nagios","Chef","Sumo Logic","OverOps","Consul","Stackify Retrace","CFEngine","Artifactory","Capistrano","Monit","Supervisor","Ansible","Code Climate","Icinga","New Relic APM","Juju","ProductionMap","Kubernetes","Git","Gradle","Kibana","Salt","Monit","Terraform","Bitbucket","Microsoft Power BI","Tableau Desktop","R Studio","SAS Studio","R Studio","Infogram","ChartBlocks","Datawrapper","D3.js","Domo","Google Charts","FusionCharts","Chart.js","Sisense","Workday Adaptive Planning","Grafana","Plecto","Whatagraph","Cluvio","RAWGraphs","Visually","looker","Chartist.js","Sigma.js","Qlik","Polymaps","Zoho Analytics","Databox","ChartBlocks","Datawrapper"," Plotly","Visually"," Ember Charts"," NVD3"," Highcharts","Leaflet","Hubspot","Spotfire","Dundas Data Visualization"]
                Script_lang = ["JavaScript","PHP","C#","Python","Ruby","Groovy","Perl","Lua","Bash","PowerShell","R","VBA","Emacs Lisp","GML","ECMAScript","Mscript","Julia","tcsh","Nim","POSIX shell","Tcl"]
                Front_end = [" React", "Javascript", "CSS", "HTML", "AngularJS", "Vue","Vue.js", "SASS", "Swift", "Elm","jQuery"]
                Data_Science = ["Machine Learning","NoSQL","SPSS" ,"Data Mining","Technical","SQL","Statistics","Python","Deep Learning","Big Data","Spark","NLP","AWS","Tabeleau","Natural Language Processing","Google Cloud Platform","GCP","Cloud Computing","NoSQL","Microsoft Azure","Microsoft Power BI","SAP","AI","Artificial Intelligence","Microsoft Excel"]
                Frameworks = ["Angular","ASP.NET","ASP.NET Core","Express","Vue","Spring","Django","Flask","Laravel","Ruby on Rails","Symfony","Gatsby","Sinatra","CakePHP","Horde","Yii","Zend","Zikula","Bootstrap","Grails","Play","Web2py","Lumen","TurboGears","Phalcon","FuelPHP","Spark:","Grok","Mojoloicious","Fat-Free Framework","Wicket","Yesod","Sencha Ext JS","Nuxt.js","Phoenix","CodeIgniter","PHPixie","Javalin","Silex","Caliburn Micro","Ionic","Xamarin","PhoneGap","React Native ","Corona","jQuery Mobile","Flutter","Mobile Angular UI","Appcelerator Titanium","Swiftic","NativeScript","Framework 7","Rachet","PyTorch","Neural Network Libraries","Neural Network Libraries","Apache MXNet","ML.NET","Infer.NET","Accord.NET","Chainer","Horovod","H2O Q","Robot Framework","Gauge","Pytest","Jest","Mocha","Jasmine","Nightwatch","Protractor","Protractor","TestProject","Galen Framework","WebDriverIO","OpenTest","Citrus","Karate","Scrapy","Truffle","Embark","Etherlime","OpenZeppelin Contracts","Brownie","Create Eth App","Exonum","Hyperledger","Corda","MultiChain","Meteor","Onsen UI","SiteWhere","Electron","Svelte","Aurelia","Mithril","Bulma","Microdot","Rapidoid","Ktor","Scalatra","Toolatra"]
                # print("--------------------------------------------------------") 
                allskills = programming_lang + web_technologies + databasesmgmt + tools + Script_lang + Front_end + Data_Science + Frameworks
                # print(allskills)
                # print("--------------------------------------------------------")
                candi_all_skills = list(set(filter(lambda x : x in cont1 , allskills)))
                print("--------------------------------------------------------")
                candi_prg_skills = list(set(filter(lambda x : x in cont1 , programming_lang)))
                # print(candi_prg_skills)
                print("--------------------------------------------------------")
                candi_web_skills = list(set(filter(lambda x : x in cont1 , web_technologies)))
                print("--------------------------------------------------------")
                candi_db_skills = list(set(filter(lambda x : x in cont1 , databasesmgmt)))
                print("--------------------------------------------------------")
                candi_tool_skills = list(set(filter(lambda x : x in cont1 , tools)))
                print("--------------------------------------------------------")
                candi_script_skills = list(set(filter(lambda x : x in cont1 , Script_lang)))
                print("--------------------------------------------------------")
                candi_front_skills = list(set(filter(lambda x : x in cont1 , Front_end)))
                print("--------------------------------------------------------")
                candi_ds_skills = list(set(filter(lambda x : x in cont1 , Data_Science)))
                print("--------------------------------------------------------")
                candi_framework_skills = list(set(filter(lambda x : x in cont1 , Frameworks)))
                
                newdata = {
                    "candidate_name":request.form["candidatename"],
                    "c_email_id":request.form["email"],
                    "contact_no":request.form["contact"],
                    "filename":filename,
                    "uploadfile" :base64.b64encode(bytes(uploadfile.read())),
                    "allskills": candi_all_skills,
                    "prglang":candi_prg_skills,
                    "web":candi_web_skills,
                    "db":candi_db_skills,
                    "tools_only":candi_tool_skills,
                    "script":candi_script_skills,
                    "front":candi_front_skills,
                    "ds":candi_ds_skills,
                    "framework":candi_framework_skills
                }

                check = db.allskills_db.find_one(filter=dict(contact_no=request.form['contact']))

                # print(check)
                if check == None:
                    dbResponse = db.allskills_db.insert_one(newdata)
                    print(dbResponse.inserted_id)
                else:
                    return "Details already exist!"
            return render_template('allskills.html', form = form, allskills =  candi_all_skills) 
        return render_template('home.html')

if __name__ == '__main__':
       app.run(debug=True, port = 8008)
 
