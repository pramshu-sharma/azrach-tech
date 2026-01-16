from flask import Flask
from flask_restx import Api

from app.api_models.patient_api_models import ns as patients_namespace
from app.routing import patients as patients_routing

flask_app = Flask(__name__)
api = Api(flask_app, title='Patient Management System', doc='/')
api.add_namespace(patients_namespace, path='/patients')

if __name__ == '__main__':
    flask_app.run(debug=True)
