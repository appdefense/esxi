from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'ESXiProcesses.sqlite')
db = SQLAlchemy(app)
ma = Marshmallow(app)

process_counter = {}

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

    def __init__(self, WorldFlags, WorldGroupId, ParentCartelId, \
        CartelId, Id, WorldType, SessionId, CommandLine, \
            SecurityDomain, Name, CartelGroupId, WorldState, sha256):

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

class ProcessSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ('WorldFlags', 'WorldGroupId', 'ParentCartelId', \
                  'CartelId', 'Id', 'WorldType', 'SessionId', 'CommandLine', \
                  'SecurityDomain', 'Name', 'CartelGroupId', 'WorldState', 'sha256')

process_schema = ProcessSchema(many=True)
# endpoint to register new process
@app.route("/process", methods=["POST"])
def add_process():

    new_process = Process(
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
        request.json['sha256Hash']
    )

    command = request.json['Command Line']
    
    if process_counter.get(command):
        process_counter[command] += 1
    else:
        process_counter[command] = 1

    db.session.add(new_process)
    db.session.commit()
    return jsonify({"Status" : "Successful"})

# endpoint to show all processes
@app.route("/process", methods=["GET"])
def get_all_processes():
    all_processes = Process.query.all()
    result = process_schema.dump(all_processes)
    return jsonify(result.data)

@app.route("/process/count", methods=["GET"])
def process_count():
    return jsonify(process_counter)

@app.route("/process/search", methods=["GET"])
def search_command_entries():
    command = request.args.get("command")
    all_processes = Process.query.filter(Process.CommandLine==command).all()
    result = process_schema.dump(all_processes)
    return jsonify(result.data)

if __name__ == '__main__':
    if not os.path.exists(os.path.join(basedir, 'ESXiProcesses.sqlite')):
        db.create_all()
    app.run(debug=True)