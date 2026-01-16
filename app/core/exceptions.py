from functools import wraps
from sqlalchemy.exc import SQLAlchemyError
from flask_restx import abort


def db_error_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except SQLAlchemyError as e:
            abort(500, f'A Database error occurred: {str(e)}')

    return wrapper
