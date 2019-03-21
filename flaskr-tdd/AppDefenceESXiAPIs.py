from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os
import json

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ESXiProcesses.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

class Process(db.Model):

    __tablename__ = "process"

    WorldFlags = db.Column(db.Integer, primary_key=True)
    WorldGroupId = db.Column(db.Integer, nullable=True)
    ParentCartelId = db.Column(db.Integer, nullable=True)
    CartelId = db.Column(db.Integer, nullable=True)
    Id = db.Column(db.Integer, primary_key=True)
    WorldType = db.Column(db.String, nullable=True)
    SessionId = db.Column(db.Integer, nullable=True)
    CommandLine = db.Column(db.String, primary_key=True)
    SecurityDomain = db.Column(db.String, nullable=True)
    Name = db.Column(db.String, nullable=True)
    CartelGroupId = db.Column(db.Integer, nullable=True)
    WorldState = db.Column(db.String, nullable=True)
    sha256 = db.Column(db.String, nullable=True)
    BinaryPath = db.Column(db.String, nullable=True)

    def __init__(self, WorldFlags, WorldGroupId, ParentCartelId, \
        CartelId, Id, WorldType, SessionId, CommandLine, SecurityDomain,\
            Name, CartelGroupId, WorldState, sha256, BinaryPath):

        self.WorldFlags = WorldFlags
        self.WorldGroupId = WorldGroupId
        self.ParentCartelId = ParentCartelId
        self.CartelId = CartelId
        self.Id = Id
        self.WorldType = WorldType
        self.SessionId = SessionId
        self.CommandLine = CommandLine
        self.SecurityDomain = SecurityDomain
        self.Name = Name
        self.CartelGroupId = CartelGroupId
        self.WorldState = WorldState
        self.sha256 = sha256
        self.BinaryPath = BinaryPath

class SuspeciousProcess(db.Model):

    __tablename__ = "suspecious_process"

    WorldFlags = db.Column(db.Integer, primary_key=True)
    WorldGroupId = db.Column(db.Integer, nullable=True)
    ParentCartelId = db.Column(db.Integer, nullable=True)
    CartelId = db.Column(db.Integer, nullable=True)
    Id = db.Column(db.Integer, primary_key=True)
    WorldType = db.Column(db.String, nullable=True)
    SessionId = db.Column(db.Integer, nullable=True)
    CommandLine = db.Column(db.String, primary_key=True)
    SecurityDomain = db.Column(db.String, nullable=True)
    Name = db.Column(db.String, nullable=True)
    CartelGroupId = db.Column(db.Integer, nullable=True)
    WorldState = db.Column(db.String, nullable=True)
    sha256 = db.Column(db.String, nullable=True)
    BinaryPath = db.Column(db.String, nullable=True)

    def __init__(self, WorldFlags, WorldGroupId, ParentCartelId, \
        CartelId, Id, WorldType, SessionId, CommandLine, SecurityDomain,\
            Name, CartelGroupId, WorldState, sha256, BinaryPath):

        self.WorldFlags = WorldFlags
        self.WorldGroupId = WorldGroupId
        self.ParentCartelId = ParentCartelId
        self.CartelId = CartelId
        self.Id = Id
        self.WorldType = WorldType
        self.SessionId = SessionId
        self.CommandLine = CommandLine
        self.SecurityDomain = SecurityDomain
        self.Name = Name
        self.CartelGroupId = CartelGroupId
        self.WorldState = WorldState
        self.sha256 = sha256
        self.BinaryPath = BinaryPath

class ProcessSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('WorldFlags', 'WorldGroupId', 'ParentCartelId', \
                  'CartelId', 'Id', 'WorldType', 'SessionId', 'CommandLine', \
                  'SecurityDomain', 'Name', 'CartelGroupId', 'WorldState', 'sha256')

class SuspeciousProcessSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('WorldFlags', 'WorldGroupId', 'ParentCartelId', \
                  'CartelId', 'Id', 'WorldType', 'SessionId', 'CommandLine', \
                  'SecurityDomain', 'Name', 'CartelGroupId', 'WorldState', 'sha256')

process_schema = ProcessSchema(many=True)
suspecious_process_schema = SuspeciousProcessSchema(many=True)
# endpoint to register new process
@app.route("/process", methods=["POST"])
def add_process():

    with open('config.json') as config:
        config = config.read()
        PROTECTED = json.loads(config)['protected_mode']

    command = request.json['Command Line']
    table = Process
    if PROTECTED:
        if  not Process.query.filter(Process.CommandLine==command).first():
            table = SuspeciousProcess

    new_process = table(
        request.json['World Flags'],
        request.json['World Group Id'],
        request.json['Parent Cartel Id'],
        request.json['Cartel Id'],
        request.json['Id'],
        request.json['World Type'],
        request.json['Session Id'],
        request.json['Command Line'],
        request.json['Security Domain'],
        request.json['Name'],
        request.json['Cartel Group Id'],
        request.json['World State'],
        request.json['sha256Hash'],
        request.json['Binary Path']
    )

    db.session.add(new_process)
    db.session.commit()
    return jsonify({"Status" : "Successful"})

# endpoint to show all processes
@app.route("/process", methods=["GET"])
def get_all_processes():
    all_processes = Process.query.all()
    result = process_schema.dump(all_processes)
    return jsonify(result.data)

@app.route("/warnings", methods=["GET"])
def get_warnings():
    all_processes = SuspeciousProcess.query.all()
    result = suspecious_process_schema.dump(all_processes)
    return jsonify(result.data)

@app.route("/process/count", methods=["GET"])
def process_count():
    all_processes = db.session.query(Process.CommandLine, db.func.count(Process.CommandLine)).group_by(Process.CommandLine).all()
    return json.dumps(all_processes)

@app.route("/warnings/count", methods=["GET"])
def warning_count():
    all_processes = db.session.query(SuspeciousProcess.CommandLine, db.func.count(SuspeciousProcess.CommandLine)).group_by(SuspeciousProcess.CommandLine).all()
    return json.dumps(all_processes)

@app.route("/process/search", methods=["GET"])
def search_command_entries():
    command = request.args.get("command")
    all_processes = Process.query.filter(Process.CommandLine==command).all()
    result = process_schema.dump(all_processes)
    return jsonify(result.data)

if __name__ == '__main__':
    if not os.path.exists(os.path.join(basedir, 'ESXiProcesses.sqlite')):
        db.create_all()
    app.run(host="0.0.0.0", debug=True)