from app import db


class Hosts(db.Model):

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


class Process(db.Model):

    __tablename__ = "process"

    post_id = db.Column(db.Integer, primary_key=True)
    cli = db.Column(db.String, nullable=True)
    inbound = db.Column(db.String, nullable=True)
    outbound = db.Column(db.Integer, nullable=True)
    counter = db.Column(db.Integer, nullable=True)

    def __init__(self, cli, inbound, outbound):
        self.cli = cli
        self.inbound = inbound
        self.outbound = outbound
        self.counter = counter

    def __repr__(self):
        return '<title {}>'.format(self.body)