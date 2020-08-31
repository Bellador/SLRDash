from . import app, db
from flask import g
from sqlalchemy import text
from .models import ScopusEntry
from sqlalchemy.orm import sessionmaker
from flask import render_template, request, jsonify, make_response, url_for, redirect, session

def get_article(eid=False):
    data = {}
    '''
    inital db request to get paper pool based on:
    - subtype: peer reviewed articles
    - not yet reviewed (decision is Null, decision true = included, decision false = excluded)
    '''
    if not eid:
        article = db.session.query(ScopusEntry). \
            filter(ScopusEntry.subtype == 'Article'). \
            filter(ScopusEntry.decision.is_(None)). \
            order_by(ScopusEntry.eid.desc()). \
            limit(1). \
            all() # same as list(query)/list(article)
        article = article[0]
    #eid can be supplied to access e.g. previous post. The eid then comes from the cookie value 'previous_eid'
    else:
        article = db.session.query(ScopusEntry). \
            filter(ScopusEntry.eid == eid). \
            all()  # same as list(query)/list(article)
        article = article[0]

    data = article.__dict__

    # remove the InstanceState key from the dict that hinders json serialisation
    del data['_sa_instance_state']
    # data['eid'] = article.eid
    # data['title'] = article.title
    # data['abstract'] = article.abstract
    # data['url'] = article.paperurl
    # data['keywords'] = article.keywords
    return data

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/start', methods=['GET'])
def start():
    # clear all relevant session cookies
    try:
        del session['current_eid']
        del session['previous_eids']
        del session['reviewer']
    except Exception as e:
        print(f'Some session keys were not present: {e}')
    return ('', 204)

@app.route('/history', methods=['POST'])
def old_article():
    data = request.json
    requested_eid = data['requested_eid']
    data = get_article(eid=requested_eid)
    session['current_eid'] = requested_eid
    json = jsonify(data)
    # store eid as previous_eid (for 'previous' button)
    resp = make_response(json)
    return resp

@app.route('/next', methods=['GET'])
def next_article():
    data = get_article()
    session_items = session.items()
    # set old current_eid to previous_eid if present with session variable
    # if its not present, then next has been called the first time; on window load
    if 'current_eid' not in session.keys():
        session['current_eid'] = data['eid']
        session['previous_eids'] = []
    # next endpoint was called min. once
    else:
        # set current eid to previous eid and assing newly fetched eid
        OLD_current_eid = session['current_eid']
        # check if already exsits (e.g. when going back and forth between articles)
        if OLD_current_eid not in session['previous_eids']:
            session['previous_eids'].append(OLD_current_eid)
        session['current_eid'] = data['eid']

    # add previous eids
    data['previous_eids'] = session['previous_eids']
    json = jsonify(data)
    # store eid as previous_eid (for 'previous' button)
    resp = make_response(json)
    return resp

@app.route('/previous', methods=['GET'])
def previous_article():
    session_items = session.items()
    if 'previous_eids' in session.keys():
        # get eid of previous eid of current eid based on the index of the current
        # first check if current eid is already in previous eids (in case multiple times previous article requested)
        if session['current_eid'] in session['previous_eids']:
            # then take one index prior to the index the current eid has
            index = session['previous_eids'].index(session['current_eid'])-1
            eid_to_get = session['previous_eids'][index]
            data = get_article(eid_to_get)
        else:
            # if the current eid is not already in previous eids, than we can just take the last element of the previous eids list
            eid_to_get = session['previous_eids'][-1]
            data = get_article(eid_to_get)
        # set the previous eid to current
        session['current_eid'] = eid_to_get
        json = jsonify(data)
        # store eid as previous_eid (for 'previous' button)
        resp = make_response(json)
        return resp
    else:
        return ('', 204)

@app.route('/decision', methods=["POST"])
def decision_made():
    '''
    This function will be implemented in the Flask SLRtoolGAE of the SLRtool WebApp which will:
    Check if the paper currently in view will be accepted or rejected by the user given the inclusion and exclusion
    criteria for the Systematic Literature Review

    it will also return the next paper if decision was made.

    :return:
    '''
    json = request.json
    decision = json['decision']
    reviewer = session['reviewer']
    db.session.query(ScopusEntry).\
        filter(ScopusEntry.eid == session['current_eid']).\
        update({'decision': decision, 'reviewer': reviewer})

    db.session.commit()
    return ('', 204)

@app.route('/reviewer', methods=["POST"])
def set_reviewer():
    reviewer = request.json
    session['reviewer'] = reviewer
    return ('', 204)