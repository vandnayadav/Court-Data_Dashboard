from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class CaseQuery(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    case_type = db.Column(db.String(50))
    case_number = db.Column(db.String(50))
    case_year = db.Column(db.String(10))
    parties = db.Column(db.Text)
    filing_date = db.Column(db.String(50))
    next_hearing_date = db.Column(db.String(50))
    pdf_link = db.Column(db.Text)
    raw_html = db.Column(db.Text)
