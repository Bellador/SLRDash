from . import app, db
from functools import wraps
from .models import ScopusEntry
from settings import LOGIN_PASSWORD
from flask import render_template, request, jsonify, make_response, url_for, redirect, session

def password_checked(a_func):
    @wraps(a_func)
    def inner():
        if 'passwd_verified' in session.keys():
            if session['passwd_verified'] == True:
                return a_func()
            else:
                return ('not verified', 401)
        else:
            return ('not verified', 401)
    return inner

def get_article(eid=False):
    '''
    inital db request to get paper pool based on:
    - subtype: peer reviewed articles
    - not yet reviewed (decision is Null, decision true = included, decision false = excluded)
    '''
    session_items = session.items()
    if not eid:
        previous_eids = session.get('previous_eids')
        if previous_eids is None:
            previous_eids = ()
        else:
            previous_eids = tuple(previous_eids)
        # get article filter settings from session token that were passed by the user at application start
        filters = tuple(session['filters'])
        reviewer = int(session['reviewer'])
        if reviewer == 1:
            article = db.session.query(ScopusEntry). \
                filter(ScopusEntry.subtype == 'Article'). \
                filter(~ScopusEntry.eid.in_(previous_eids)). \
                filter(ScopusEntry.eid != session.get('current_eid')). \
                filter(ScopusEntry.decision_r_1.in_(filters)). \
                order_by(ScopusEntry.eid.desc()). \
                limit(1). \
                all() # same as list(query)/list(article)
        elif reviewer == 2:
            article = db.session.query(ScopusEntry). \
                filter(ScopusEntry.subtype == 'Article'). \
                filter(~ScopusEntry.eid.in_(previous_eids)). \
                filter(ScopusEntry.eid != session.get('current_eid')). \
                filter(ScopusEntry.decision_r_2.in_(filters)). \
                order_by(ScopusEntry.eid.desc()). \
                limit(1). \
                all() # same as list(query)/list(article)
        elif reviewer == 3:
            article = db.session.query(ScopusEntry). \
                filter(ScopusEntry.subtype == 'Article'). \
                filter(~ScopusEntry.eid.in_(previous_eids)). \
                filter(ScopusEntry.eid != session.get('current_eid')). \
                filter(ScopusEntry.decision_r_3.in_(filters)). \
                order_by(ScopusEntry.eid.desc()). \
                limit(1). \
                all() # same as list(query)/list(article)

    else:
        article = db.session.query(ScopusEntry). \
            filter(ScopusEntry.eid == eid). \
            all()  # same as list(query)/list(article)
    # check if empty return
    try:
        article = article[0]
        data = article.__dict__
        # remove the InstanceState key from the dict that hinders json serialisation
        del data['_sa_instance_state']
    except:
        data = None

    return data

@app.route('/')
def home():
    return render_template('app.html')

@app.route('/start', methods=['GET'])
def start():
    # clear all relevant session cookies
    session_items = session.items()
    keys = session.keys()
    to_del = []
    not_to_del = ['csrf_token', 'filters', 'reviewer', 'passwd_verified']
    for key in keys:
        if key not in not_to_del:
            to_del.append(key)
    # actual delete
    for key in to_del:
        del session[key]
    return ('', 204)

@app.route('/history', methods=['POST'])
@password_checked
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
@password_checked
def next_article():
    data = get_article()
    if data is not None:
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
    else:
        return ('no data', 204)

@app.route('/previous', methods=['GET'])
@password_checked
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
@password_checked
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
    remark = json['remark']
    reviewer = int(session['reviewer'])
    if reviewer == 1:
        db.session.query(ScopusEntry).\
            filter(ScopusEntry.eid == session['current_eid']).\
            update({'decision_r_1': decision,
                    'remark_r_1': remark})
    elif reviewer == 2:
        db.session.query(ScopusEntry).\
            filter(ScopusEntry.eid == session['current_eid']).\
            update({'decision_r_2': decision,
                    'remark_r_2': remark})
    elif reviewer == 3:
        db.session.query(ScopusEntry).\
            filter(ScopusEntry.eid == session['current_eid']).\
            update({'decision_r_3': decision,
                    'remark_r_3': remark})

    db.session.commit()
    return ('', 204)

@app.route('/settings', methods=["POST"])
def set_settings():
    session['passwd_verified'] = False
    settings = request.json
    input_password = settings['password']
    # check password
    if input_password != LOGIN_PASSWORD:
        return ('false password', 401)
    session['passwd_verified'] = True
    session['reviewer'] = settings['reviewer']
    # create new decision column for this reviewer if not existant
    filters = settings['article_filter_list']
    try:
        filters[filters.index('notreviewed_checkbox')] = 'not reviewed'
    except:
        pass
    try:
        filters[filters.index('unsure_checkbox')] = '0'
    except:
        pass
    try:
        filters[filters.index('included_checkbox')] = '1'
    except:
        pass
    try:
        filters[filters.index('excluded_checkbox')] = '-1'
    except:
        pass

    session['filters'] = filters
    return ('', 204)