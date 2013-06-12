#!/usr/bin/python
# -*- coding: utf-8 -*- 
from __future__ import with_statement
from sqlrequest import *
from sqlite3 import dbapi2 as sqlite3
from flask import Flask,session,g,url_for, abort,render_template,Markup,request,flash,redirect, _app_ctx_stack
from flask.views import MethodView
from werkzeug import url_decode

import time
from sqlite3 import dbapi2 as sqlite3
from hashlib import md5
from datetime import datetime
from contextlib import closing
from flask import Flask, request, session, url_for, redirect, \
     render_template, abort, g, flash
from werkzeug import check_password_hash, generate_password_hash
from werkzeug.contrib.fixers import LighttpdCGIRootFix

###Middleware####
class MethodRewriteMiddleware(object):
 
    def __init__(self, app):
        self.app = app
 
    def __call__(self, environ, start_response):
        if 'METHOD_OVERRIDE' in environ.get('QUERY_STRING', ''):
            args = url_decode(environ['QUERY_STRING'])
            method = args.get('__METHOD_OVERRIDE__')
            if method:
                method = method.encode('ascii', 'replace')
                environ['REQUEST_METHOD'] = method
  
        return self.app(environ, start_response)


#Creation de la base de donnees
DATABASE = '/tmp/enstapp.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'
app = Flask(__name__)
app.config.from_object(__name__)
app.wsgi_app = MethodRewriteMiddleware(app.wsgi_app)


def connect_db():
    """Returns a new connection to the database."""
    return sqlite3.connect(app.config['DATABASE'])

def init_db():
    """Creates the database tables."""
    with closing(connect_db()) as db:
        with app.open_resource('schema.sql') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    """Opens a new database connection if there is none yet for the
current application context.
"""
    top = _app_ctx_stack.top
    if not hasattr(top, 'sqlite_db'):
        sqlite_db = sqlite3.connect(app.config['DATABASE'])
        sqlite_db.row_factory = sqlite3.Row
        top.sqlite_db = sqlite_db
	

    return top.sqlite_db


def query_db(query, args=(), one=False):
    """Queries the database and returns a list of dictionaries."""
    cur = g.db.execute(query, args)
    rv = [dict((cur.description[idx][0], value)
               for idx, value in enumerate(row)) for row in cur.fetchall()]
    return (rv[0] if rv else None) if one else rv



@app.teardown_appcontext
def close_db_connection(exception):
    """Closes the database again at the end of the request."""
    top = _app_ctx_stack.top
    if hasattr(top, 'sqlite_db'):
        top.sqlite_db.close()


######SIMPLE ROUTING########
@app.route('/')
def about():    
    return render_template('about.html')

@app.route('/updateperson', methods=['PUT'])
def updateperson():
	db = get_db()
	param={'name':request.form['nom'],'firstname':request.form['prenom'],'function':request.form['fonction'],'bureau':request.form['bureau'],'phone':request.form['telephone'],'mail':request.form['email']}
	updateFieldRecord('person',param,request.form['person_id'],db)
	db.commit()
  return redirect(url_for('person_api'))

@app.route('/deleteperson/<int:person_id>', methods=['GET','DELETE'])
def deleteperson(person_id):
	db=get_db()
	deleteRecord('person',person_id,db)
	flash('Person deleted !')
	db.commit()
	return redirect(url_for('person_api'))

@app.route('/updateplace', methods=['PUT'])
def updateplace():
	db = get_db()
	param={'name': request.form['nom'],'description_FR':request.form['description_fr'],'description_AN':request.form ['description_ang']}
	updateFieldRecord('place',param,request.form['place_id'],db)
	db.commit()
  return redirect(url_for('place_api'))

@app.route('/deleteplace/<int:place_id>', methods=['GET','DELETE'])
def deleteplace(place_id):
	db=get_db()
	deleteRecord('place',place_id,db)
	flash('Place deleted !')
	db.commit()
	return redirect(url_for('place_api'))

@app.route('/updateservice', methods=['PUT'])
def updateservice():
	db = get_db()
	param={'name': request.form['nom'],'description_FR':request.form['description_fr'],'description_AN':request.form ['description_ang'],'building':request.form['building']}
	updateFieldRecord('service',param,request.form['service_id'],db)
	db.commit()
  return redirect(url_for('service_api'))

@app.route('/deleteservice/<int:service_id>', methods=['GET','DELETE'])
def deleteservice(service_id):
	db=get_db()
	deleteRecord('service',service_id,db)
	flash('Service deleted !')
	db.commit()
	return redirect(url_for('service_api'))

@app.route('/personmobile/<string:entry>')	
def personmobile(self,entry):
	db = get_db()
	c=db.cursor()
	person_id=getIdperson(person,entry,c)
	if person_id !=0:
    cur=db.cursor()
		getRecord('person',person_id,db)
		cur=getAllRecord('person',db)
		PERSON=cur.fetchall()
    return render_template('person.xml',person=PERSON, reussite='succes')
	else:
		return render_template('person.xml',person=None, reussite='echec')

@app.route('/servicemobile/<string:entry>')	
def servicemobile(self,entry):
	db = get_db()
	c=db.cursor()
	service_id=getId(service,entry,c)
	if service_id !=0:
    cur=db.cursor()
		getRecord('service',service_id,db)
		cur=getAllRecord('service',db)
		SERVICE=cur.fetchall()
    return render_template('service.xml',service=SERVICE,reussite='succes')
	else:
		return render_template('service.xml',service=None,reussite='echec')	
	
@app.route('/placemobile/<string:entry>')	
def placemobile(self,entry):
	db = get_db()
	c=db.cursor()
	place_id=getId(place,entry,c)
	if place_id !=0:
    cur=db.cursor()
		getRecord('place',place_id,db)
		cur=getAllRecord('place',db)
		PLACE=cur.fetchall()
    return render_template('place.xml',place=PLACE,reussite='succes')
	else:
		return render_template('place.xml',place=None,reussite='echec')


############
# REST API #
############

class PersonAPI(MethodView):
   
   def get(self,person_id):
	    db = get_db()
	    c=db.cursor()
      cur=db.cursor()
	    cur=getAllRecord('person',db)
      people = cur.fetchall()
      if person_id:
           c=getRecord('person',person_id,db)
           PERSON=c.fetchall()
           return render_template('person.html',PEOPLE=people,person=PERSON)
      else:
           return render_template('person.html',PEOPLE=people,person=None)
	
   def post(self):
    	db = get_db()
	    param={'name': request.form['nom'],'firstname':request.form['prenom'],'function':request.form ['fonction'],'mail':request.form     ['email'],'phone':request.form['telephone'],'bureau':request.form ['bureau'] }
    	createNewRecord('person',param,db)
    	db.commit()
	    flash('Nouvelle personne ajoutee')
	    return redirect(url_for('person_api'))	
 
	
class PlaceAPI(MethodView):

    def get(self,place_id):
	    db = get_db()
	    c=db.cursor()
      cur=db.cursor()
	    cur=getAllRecord('place',db)
      places = cur.fetchall()
      if place_id:
        c=getRecord('place',place_id,db)
        PLACE=c.fetchall()
        return render_template('place.html',PLACES=places,place=PLACE)
      else:
        return render_template('place.html',PLACES=places,person=None)
	
    def post(self):
	    db = get_db()
	    param={'name': request.form['nom'],'description_FR':request.form['description_fr'],'description_AN':request.form ['description_ang']}
    	createNewRecord('place',param,db)
	    db.commit()
	    flash('Nouveau lieu ajoute')
	    return redirect(url_for('place_api'))		
	
class ServiceAPI(MethodView):

    def get(self,service_id):
	    db = get_db()
	    c=db.cursor()
      cur=db.cursor()
	    cur=getAllRecord('service',db)
      services = cur.fetchall()
      if service_id:
         c=getRecord('service',service_id,db)
         SERVICE=c.fetchall()
         return render_template('service.html',SERVICES=services,service=SERVICE)
      else:
         return render_template('service.html',SERVICES=services,person=None)
	

    def post(self):
	    db = get_db()
	    param={'name': request.form['nom'],'description_FR':request.form['description_fr'],'description_AN':request.form ['description_ang'],'building':request.form['building']}
    	createNewRecord('service',param,db)
	    db.commit()
	    flash('Nouveau service ajoute')
	    return redirect(url_for('service_api'))	  

    
def register_api(view, endpoint, url, pk='id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(url, defaults={pk: None},view_func=view_func, methods=['GET',])
    app.add_url_rule(url, view_func=view_func, methods=['POST',])
    app.add_url_rule('%s<%s:%s>' % (url, pk_type, pk), view_func=view_func,methods=['GET','POST', 'PUT', 'DELETE'])

register_api(PersonAPI, 'person_api', '/person/', pk='person_id')
register_api(PlaceAPI, 'place_api', '/place/', pk='place_id')
register_api(ServiceAPI, 'service_api', '/service/', pk='service_id')



if __name__ == '__main__':
    init_db()
    app.run()







