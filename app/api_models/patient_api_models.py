from flask_restx import fields, Namespace
from app.models.patient import PATIENT_STATUS


PATIENT_STATUS_VALUES = [value for value in PATIENT_STATUS]

ns = Namespace('patients', description='Patient Namespace')

patient_response_model = ns.model(
    'Patient',
    {
        'id': fields.Integer(readonly=True),
        'name': fields.String(),
        'age': fields.Integer(),
        'notes': fields.String(),
        'check_datetime': fields.DateTime(),
        'status': fields.String(),
        'created_at': fields.DateTime(readOnly=True),
        'updated_at': fields.DateTime(readOnly=True)
    },
)

patient_create_model = ns.model(
    'Patient Create Update',
    {
        'id': fields.Integer(readonly=True),
        'name': fields.String(required=True),
        'age': fields.Integer(required=True),
        'notes': fields.String(),
        'check_datetime': fields.DateTime(required=True),
        'status': fields.String(enum=PATIENT_STATUS_VALUES, required=True)
    },
)


patient_upsert_response = ns.model(
    'Patient Batch Response',
    {
        'success': fields.List(fields.Nested(patient_response_model)),
        'failed': fields.List(fields.Raw()),
    },
)
