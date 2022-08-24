from enum import unique
from msilib.schema import File
from sys import maxsize
from flask_wtf import FlaskForm
from flask import Flask,request
from wtforms import StringField,SubmitField,PasswordField,SelectField,BooleanField,IntegerField,FileField
from wtforms.validators import DataRequired, Email,EqualTo,Length




class Allskills(FlaskForm):
    candidatename = StringField(' Candidate Name ',validators= [DataRequired(),Length(min=3,max = 40)])
    email = StringField('Email Id',validators = [DataRequired(),Email()])
    contact = IntegerField('Contact Number',validators= [DataRequired()])
    resume  = FileField('file')
    submit= SubmitField('Submit')
 
class Sample(FlaskForm):
    candidatename = StringField(' Candidate Name ',validators= [DataRequired(),Length(min=3,max = 40)])
    contact = IntegerField('Contact Number',validators= [DataRequired()])
    sort = SelectField(u'Search for any Skill Set',choices = [('default','                 '),('AS','All Skills'),('Prg_lang','Programming Language'),('WT','Web Technologies'),('db','Database Management'),('tl','Tools'),('Scpt_lang','Scripting Language'),('Frnt_nd','Front End Technologies'),('DS','Data Science'),('Frm_wks','Frameworks')])
    resume  = FileField('file')
    Get_data = SubmitField('Get Data')
 
class SortAll(FlaskForm):
    sort_al = SelectField(u'Search for any Skill Set',choices = [('default','                 '),('AS','All Skills'),('Prg_lang','Programming Language'),('WT','Web Technologies'),('db','Database Management'),('tl','Tools'),('Scpt_lang','Scripting Language'),('Frnt_nd','Front End Technologies'),('DS','Data Science'),('Frm_wks','Frameworks')])
    Get_all = SubmitField('All Data')