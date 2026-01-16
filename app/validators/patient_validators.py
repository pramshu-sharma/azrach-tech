from app.models.patient import Patient


def validate_patient_age(age):
    if not isinstance(age, int):
        raise ValueError('Age must be an integer.')

    if age < 0 or age > 120:
        raise ValueError('Age must be realistic (0 - 120).')


def check_required_fields(item):
    required_fields = ['name', 'age', 'check_datetime', 'status']
    for field in required_fields:
        if field not in item:
            raise ValueError(f'Missing required field: {field}')


def remove_invalid_fields(item):
    return {k: v for k, v in item.items() if hasattr(Patient, k)}
