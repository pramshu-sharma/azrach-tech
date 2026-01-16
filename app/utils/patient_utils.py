def patient_to_dict(patient):
    return {
        "id": patient.id,
        "name": patient.name,
        "age": patient.age,
        "notes": patient.notes,
        "check_datetime": patient.check_datetime,
        "status": patient.status,
        "created_at": patient.created_at,
        "updated_at": patient.updated_at
    }