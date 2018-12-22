#!/usr/bin/env python2.7
# =============================================================================
# title         : Project 2: Item Catalog
# author        : Faleh Aldham
# date          : Dec 16, 2018
# version       : 0.1
# usage         : python app.py
# notes         : this script uses 3rd party library
# python_version: 2.7
# =============================================================================

# importing Flask framework
from flask import Flask, render_template, request, \
                    redirect, jsonify, url_for, flash

# importing SQLalchemy ==> the database engine that talks Python :)
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MangaCategory, MangaItem, User

# Importing the session library to stor user information
from flask import session as login_session
import random
import string

# importing oauth dependinces for integrating
# with Google Oauth APIs and other needed libraries
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

from functools import wraps

# initiating a flask app
app = Flask(__name__)

CLIENT_ID = json.loads(
    open('client_secrets.json', 'r').read())['web']['client_id']
APPLICATION_NAME = "My Favorite Manga Application"

# Connect to Database and create database session
database_name = 'sqlite:///mangacatelog.db?check_same_thread=False'
engine = create_engine(database_name, pool_pre_ping=True)
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


# all mangas endpoint
# ----------------------------

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in login_session:
            return f(*args, **kwargs)
        else:
            flash("You are not allowed to access there")
            return redirect('/login')
    return decorated_function


# Displays all Manga Categories and recently added Manga
@app.route("/")
@app.route("/manga")
def manga():
    manga_categories = session.query(
        MangaCategory).order_by(asc(MangaCategory.name))
    recent_manag_items = session.query(
        MangaItem).order_by(MangaItem.id.desc()).limit(5)
    return render_template(
                            'itemcatalog.html',
                            manga_categories=manga_categories,
                            recent_manag_items=recent_manag_items,
                            login_session=login_session)


# Displays all Manga in a given category
@app.route("/manga/<string:manga_cat>")
@app.route("/manga/<string:manga_cat>/items")
def manga_category(manga_cat):
    manga_categories = session.query(
        MangaCategory).order_by(asc(MangaCategory.name))
    for cat in manga_categories:
        if cat.name == manga_cat:
            manga_cat_id = cat.id
    manag_items = session.query(MangaItem).filter_by(
        mangaCategory_id=(manga_cat_id)).order_by(MangaItem.id.desc()).all()
    creators = {}
    if login_session:
        for item in manag_items:
            creators[getUserInfo(item.user_id).id] = getUserInfo(item.user_id)
        return render_template(
            'manga_item.html',
            manga_categories=manga_categories,
            manag_items=manag_items,
            selected_manga_category=manga_cat,
            login_session=login_session,
            creators=creators)
    else:
        return render_template(
            'manga_item.html',
            manga_categories=manga_categories,
            manag_items=manag_items,
            selected_manga_category=manga_cat,
            login_session=login_session,
            creators=creators)


# Displays description of a given manga
@app.route("/manga/<string:manga_cat>/<string:manga_item>")
def manga_item_desc(manga_cat, manga_item):
    manga_categories = session.query(
        MangaCategory).order_by(asc(MangaCategory.name))
    manga_item = session.query(
        MangaItem).filter_by(name=manga_item).one()
    creator = ''
    if login_session['user_id']:
        print 'know'
        creator = getUserInfo(login_session['user_id'])
        return render_template(
            'manga_desc.html',
            manga_item=manga_item,
            manga_cat=manga_cat,
            manga_categories=manga_categories,
            login_session=login_session,
            creator=creator)
    else:
        print 'no'
        return render_template(
            'manga_desc.html',
            manga_item=manga_item,
            manga_cat=manga_cat,
            manga_categories=manga_categories,
            login_session=login_session,
            creator='')


# Creates new manga

@app.route("/manga/new", methods=['GET', 'POST'])
@login_required
def new_manga():
    manga_categories = session.query(
        MangaCategory).order_by(asc(MangaCategory.name))
    if request.method == 'POST':
        new_manga_cat = request.form['mangaCategory_id']
        if request.form['submit_button'] == 'add':
            new_name = request.form['name']
            new_desc = request.form['description']

            for cat in manga_categories:
                if cat.name == new_manga_cat:
                    manga_cat = cat
                    manga_cat_id = cat.id

            newMangaItem = MangaItem(
                name=new_name,
                description=new_desc,
                mangaCategory_id=manga_cat_id,
                user_id=login_session['user_id'])
            session.add(newMangaItem)
            session.commit()
            session.close()

            return redirect(
                url_for('manga_category', manga_cat=new_manga_cat))
        elif request.form['submit_button'] == 'cancel':
            return redirect(url_for('manga'))
    else:
        return render_template(
            'newManga.html',
            manga_categories=manga_categories,
            login_session=login_session)


# Edits manga item
@app.route(
            "/manga/<string:manga_cat>/<string:manga_item>/edit",
            methods=['GET', 'POST'])
@login_required
def manga_item_edit(manga_cat, manga_item):
    manga_categories = session.query(
        MangaCategory).order_by(asc(MangaCategory.name))
    mangaitem = session.query(
        MangaItem).filter_by(name=manga_item).one()

    if mangaitem.user_id != login_session['user_id']:
        return redirect('/manga')

    if request.method == 'POST':
        new_manga_cat = request.form['mangaCategory_id']
        if request.form['submit_button'] == 'edit':
            mangaitem.name = request.form['name']
            mangaitem.description = request.form['description']
            mangaitem.mangaCategory_id = request.form['mangaCategory_id']

            for cat in manga_categories:
                if cat.name == new_manga_cat:
                    manga_cat = cat
                    mangaitem.mangaCategory_id = cat.id

            if not mangaitem.name:
                mangaitem.name = manga_item

            session.add(mangaitem)
            session.commit()
            session.close()
            return redirect(
                url_for('manga_category', manga_cat=new_manga_cat))
        elif request.form['submit_button'] == 'cancel':
            return redirect(
                url_for('manga_category', manga_cat=new_manga_cat))
    else:
        return render_template(
            'editManga.html',
            manga_cat=manga_cat,
            manga_item=mangaitem,
            manga_categories=manga_categories,
            login_session=login_session)


# Deletes manga item
@app.route(
            "/manga/<string:manga_cat>/<string:manga_item>/delete",
            methods=['GET', 'POST'])
@login_required
def manga_item_delete(manga_cat, manga_item):
    manga_categories = session.query(
        MangaCategory).order_by(asc(MangaCategory.name))
    manga_item_for_del = session.query(
        MangaItem).filter_by(name=manga_item).one()

    if manga_item_for_del.user_id != login_session['user_id']:
        return redirect('/manga')

    if request.method == 'POST':
        if request.form['submit_button'] == 'delete':
            session.delete(manga_item_for_del)
            session.commit()
            session.close()
            return redirect(
                url_for('manga_category', manga_cat=manga_cat))
        elif request.form['submit_button'] == 'cancel':
            return redirect(
                url_for('manga_category', manga_cat=manga_cat))
    else:
        return render_template(
            'deleteManga.html',
            manga_item=manga_item,
            manga_categories=manga_categories,
            login_session=login_session)


# JSON APIs to view Manga Information
@app.route('/manga/JSON')
@login_required
def mangaJSON():
    manga_categories = session.query(MangaCategory).all()
    jsonf = []
    for cat in manga_categories:
        items = session.query(
            MangaItem).filter_by(mangaCategory_id=cat.id).all()
        for item in items:
            jsonf.append({
                            'id': cat.id,
                            'name': cat.name,
                            'items': [{
                                        'cat_id': item.mangaCategory_id,
                                        'description': item.description,
                                        'id': item.id, 'title': item.name}]})
    return jsonify(Category=jsonf)


# |=================================================
# |==== Code from Here to the end of this block ====
# |==== was taken from Udacity Authentication   ====
# |==== and Authorization Course                ====
# |=================================================

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(
        random.choice(
            string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state
    # return "The current session state is %s" % login_session['state']
    return render_template(
        'login.html', STATE=state, login_session=login_session)


# Google Account integration - connect
@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data

    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(
            json.dumps('Current user is already connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;'
    output += '-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("you are now logged in as %s" % login_session['username'])
    print "done!"

    return output


def createUser(login_session):
    newUser = User(name=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except Exception:
        return None


# Google Account integration - disconnect
@app.route("/gdisconnect")
def gdisconnect():
    access_token = login_session.get('access_token')
    if access_token is None:
        print 'Access Token is None'
        response = make_response(
            json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('manga'))
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    google_url = 'https://accounts.google.com/o/oauth2/revoke?token='
    url = '{}{}'.format(google_url, login_session['access_token'])

    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return redirect(url_for('manga'))
    else:
        response = make_response(
            json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response
    redirect(url_for('manga'))

# =================================================|
# ==== This is the end of the code taken from  ====|
# ==== Udacity Authentication & Authorization  ====|
# ==== Course.                                 ====|
# =================================================|


if __name__ == "__main__":
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host="0.0.0.0", port=8000)
