from flask import request
from flask_restx import Resource

from app.api_models.patient_api_models import (
    ns,
    patient_response_model,
    patient_create_model,
    patient_upsert_response
)
from app.services.patient_service import (
    get_patient_by_id,
    get_all_patients,
    create_patient,
    update_patient,
    delete_patient,
    upsert_batch_patient
)


@ns.route('/')
class PatientList(Resource):
    @ns.marshal_list_with(patient_response_model)
    def get(self):
        return get_all_patients()

    @ns.expect(patient_create_model)
    @ns.marshal_with(patient_response_model, code=201)
    def post(self):
        data = request.json
        return create_patient(data), 201


@ns.route('/<int:id>')
class Patient(Resource):
    @ns.marshal_with(patient_response_model)
    def get(self, id):
        return get_patient_by_id(id)

    @ns.expect(patient_create_model)
    @ns.marshal_with(patient_response_model)
    def put(self, id):
        data = request.json
        return update_patient(id, data)

    def delete(self, id):
        return delete_patient(id), 200


@ns.route('/upsert-batch')
class PatientUpsert(Resource):
    @ns.expect([patient_create_model])
    @ns.marshal_with(patient_upsert_response)
    def post(self):
        batch_data = request.json
        return upsert_batch_patient(batch_data)
