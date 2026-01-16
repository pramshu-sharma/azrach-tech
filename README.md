# Azrach Tech - Interview Technical Task — Flask Developer
## Patient Management System

### Steps to run the application:

   1. Clone the repository.
      
   2. Run poetry install to install dependencies
      
       `poetry install`
      
   3. Set environment variables:
      - DATABASE_URL: Database connection string.
      - LOG_LEVEL: Logging level.
      - LOG_FILE: Path for the log file.
   
        *NOTE: The log file will be genrated automatically when the first log instance is created.*
        
   4. Run database migrations.
      
       `alembic upgrade head`
       
   5. Run the main.py file.
      
       `python app/main.py`
      
   6. Swagger docs can accessed via the root URL: ('/').
   
## Main Files Overview

### app/
   **main.py** - Main entry point for the application.

### core/
   **config.py** – Holds application configuration, environment variables.
   **database.py** – Sets up the database connection using SQLAlchemy.
   **exceptions.py** – Defines custom exceptions.
   **logger.py** – Configures logging for the app.

### api_models/
   **patient_api_models.py** - Request/Response models for Flask-RESTX.
   
### models/
   **patient.py** - SQLAlchemy models for patients.

### routing/
   **patients.py** - Flask-RESTX end points.

### services/
   **patient_service.py** - Business Logic and Database operations.

### utils/
   **patient_utils.py** - Helper functions for services / routing.

### validators/
   **patient_validators.py** - Validation functions for incoming request data.

## Additional Features Implemented:
   1. Logging
   2. Exception/Error Handling
   3. Type Hinting

## Additional Features Not Implemented:
   1. Docker
   2. Pagination
   3. Unit Tests







