from . import db

class ScopusEntry(db.Model):
    # Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __tablename__ = 'literature'
    __table_args__ = {'extend_existing': True}
    # tell SQLAlchemy the name of column and its attributes:
    eid = db.Column(db.String, primary_key=True, nullable=False)
    doi = db.Column(db.String)
    title = db.Column(db.String)
    abstract = db.Column(db.String)
    keywords = db.Column(db.String)
    subtype = db.Column(db.String)
    date = db.Column(db.Date)
    author = db.Column(db.String)
    openaccess = db.Column(db.Boolean)
    publicationname = db.Column(db.String)
    paperurl = db.Column(db.String)
    abstracturl = db.Column(db.String)
    request = db.Column(db.String)
    source = db.Column(db.String)
    searchfield = db.Column(db.String)
    query = db.Column(db.String)
    sdg = db.Column(db.String)
    decision_r_1 = db.Column(db.String, default='not reviewed')
    decision_r_2 = db.Column(db.String, default='not reviewed')
    decision_r_3 = db.Column(db.String, default='not reviewed')
    remark_r_1 = db.Column(db.String, default=None)
    remark_r_2 = db.Column(db.String, default=None)
    remark_r_3 = db.Column(db.String, default=None)

    def __init__(self, eid, doi, title, subtype, date, author, openaccess, publicationname, paperurl, abstracturl, request, source, searchfield, query, sdg, decision_r_1, decision_r_2, decision_r_3, remark_r_1=None, remark_r_2=None, remark_r_3=None, abstract=None, keywords=None):
        self.eid = eid
        self.doi = doi
        self.title = title
        self.abstract = abstract
        self.keywords = keywords
        self.subtype = subtype
        self.date = date
        self.author = author
        self.openaccess = openaccess
        self.publicationname = publicationname
        self.paperurl = paperurl
        self.abstracturl = abstracturl
        self.request = request
        self.source = source
        self.searchfield = searchfield
        self.query = query
        self.sdg = sdg
        self.decision_r_1 = decision_r_1
        self.decision_r_2 = decision_r_2
        self.decision_r_3 = decision_r_3
        self.remark_r_1 = remark_r_1
        self.remark_r_2 = remark_r_2
        self.remark_r_3 = remark_r_3