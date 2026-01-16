# Azrach Tech - Interview Technical Task — Flask Developer
## Patient Management System

### Steps to run the application:

1. Clone the repository.
   
2. Run poetry install to install dependencies
    poetry install
   
3. Set environment variables:
   - DATABASE_URL: Databse connection string.
   - LOG_LEVEL: Logging level.
   - LOG_FILE: Path for the log file.
     [!NOTE]
     The log file will be genrated automatically when the first log instance is created.
     
4. Run database migrations.
    alembic upgrade head
    
5. Run the main.py file.
    python app/main.py
   
6. Swagger docs can accessed via the root URL: ('/').
