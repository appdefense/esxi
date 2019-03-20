from app import db


class Flaskr(db.Model):

    __tablename__ = "hosts"

    post_id = db.Column(db.Integer, primary_key=True)
    host_ip = db.Column(db.String, nullable=False)
    alarming = db.Column(db.String, nullable=True)
    remediation = db.Column(db.Integer, nullable=True)

    def __init__(self, host_ip, alarming, remediation):
        self.host_ip = host_ip
        self.alarming = alarming
        self.remediation = remediation

    def __repr__(self):
        return '<title {}>'.format(self.body)
