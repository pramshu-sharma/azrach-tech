from typing import List, Dict, Any, Union
from flask_restx import abort

from app.models.patient import Patient
from app.core.database import SessionLocal
from app.core.exceptions import db_error_handler
from app.validators.patient_validators import (
    validate_patient_age,
    check_required_fields,
    remove_invalid_fields
)
from app.utils.patient_utils import patient_to_dict
from app.core.logger import get_logger

logger = get_logger(__name__)


@db_error_handler
def get_all_patients() -> List[Patient]:
    logger.info('get_all_patients() called')
    with SessionLocal() as session:
        patients: List[Patient] = session.query(Patient).all()
        logger.info(f'Fetched {len(patients)} patients')
        return patients


@db_error_handler
def get_patient_by_id(patient_id: int) -> Patient:
    logger.info(f'get_patient_by_id() called id: {patient_id}')
    with SessionLocal() as session:
        patient = session.get(Patient, patient_id)

        if not patient:
            logger.warning(f'Patient with id {patient_id} not found')
            abort(404, 'Patient not found')

        logger.info(f'Patient with id {patient_id} fetched')
        return patient


@db_error_handler
def create_patient(patient_data: Dict[str, Any]):
    logger.info(f'create_patient() called data: {patient_data}')
    with SessionLocal() as session:
        patient = Patient(**patient_data)

        try:
            validate_patient_age(patient_data['age'])
        except ValueError as e:
            logger.error(f'Patient age validation failed during creation: {e}')
            abort(422, str(e))

        session.add(patient)
        session.commit()
        session.refresh(patient)
        logger.info(f'Patient created id: {patient.id}')
        return patient


@db_error_handler
def update_patient(patient_id: int, patient_data: Dict[str, Any]) -> Patient:
    logger.info(f'update_patient() called id: {patient_id} data: {patient_data}')
    with SessionLocal() as session:
        patient = session.get(Patient, patient_id)

        if not patient:
            logger.warning(f'Patient id: {patient_id} not found during update')
            abort(404, 'Patient not found')

        if 'age' in patient_data:
            try:
                validate_patient_age(patient_data['age'])
            except ValueError as e:
                logger.error(f'Patient age validation failed during update: {e}')
                abort(422, str(e))

        for key, value in patient_data.items():
            if hasattr(patient, key):
                setattr(patient, key, value)

        session.commit()
        session.refresh(patient)
        logger.info(f'Patient with id {patient.id} updated')
        return patient


@db_error_handler
def delete_patient(patient_id: int) -> str:
    logger.info(f'delete_patient() called id: {patient_id}')
    with SessionLocal() as session:
        patient = session.get(Patient, patient_id)

        if not patient:
            logger.warning(f'Patient id: {patient_id} not found during deletion')
            abort(404, 'Patient not found')

        session.delete(patient)
        session.commit()
        logger.info(f'Patient id: {patient.id} deleted')
        return f'Patient w/id: {patient.id} deleted Code:204'


def upsert_batch_patient(patient_items: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
    logger.info(f'upsert_batch_patient() called for {len(patient_items)} items')
    success: List[Dict[str, Any]] = []
    failed: List[Dict[str, Any]] = []

    if not isinstance(patient_items, list):
        logger.error('Batch upsert failed: payload is not a list')
        abort(400, 'The payload must be a list of objects')

    with SessionLocal() as session:
        for item in patient_items:
            try:
                if not isinstance(item, dict):
                    raise ValueError('Item must be an object / dictionary')

                validated_item: Dict[str, Any] = remove_invalid_fields(item)

                if not validated_item:
                    raise ValueError('No valid fields provided')

                patient_id: Union[int, None] = validated_item.get('id')

                if 'age' in validated_item:
                    validate_patient_age(validated_item['age'])

                if patient_id is not None:
                    patient = session.get(Patient, patient_id)

                    if patient:
                        for key, value in validated_item.items():
                            if key != 'id':
                                setattr(patient, key, value)

                    else:
                        check_required_fields(validated_item)
                        new_data: Dict[str, Any] = {k: v for k, v in validated_item.items() if k != 'id'}
                        patient = Patient(**new_data)
                        session.add(patient)

                else:
                    check_required_fields(validated_item)
                    patient = Patient(**validated_item)
                    session.add(patient)

                session.commit()
                session.refresh(patient)

                if patient_id is not None and session.get(Patient, patient_id):
                    logger.info(f'Patient with id {patient.id} updated (Batch Upsert)')
                else:
                    logger.info(f'Created new patient id: {patient.id} (Batch Upsert)')

                success.append(patient_to_dict(patient))

            except Exception as e:
                session.rollback()
                failed.append({
                    'item': item,
                    'error': str(e)
                })

    return {
        'success': success,
        'failed': failed
    }
