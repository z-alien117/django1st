# Oowlish Project Setup

## Prerequisites
Ensure you have the following installed:
- Docker

---

## Setup Instructions

### 1. Configure Environment Variables
1. Copy the example environment file:
   ```bash
   cp example.env .env
   ```
2. Open the `.env` file and set the following variables:
   - **`DJANGO_SECRET_KEY`**: Your Django secret key.
   - **`GOOGLE_API_KEY`**: Your Google API key.

---

### 2. Build and Start the Application
Run the following command to build and start the application:
```bash
docker-compose up --build
```

---

## Testing Instructions

### 1. Connect to the MySQL Database
To prepare the database for testing, follow these steps:

1. Access the MySQL database container:
   ```bash
   docker exec -it db mysql -uroot -p${MYSQL_ROOT_PASSWORD}
   ```
   > Use the `MYSQL_ROOT_PASSWORD` from your `.env` file when prompted.

2. Grant permissions to the `django_user` for the test database:
   ```sql
   GRANT ALL PRIVILEGES ON test_oowlish.* TO 'django_user'@'%';
   FLUSH PRIVILEGES;
   ```

### 2. Run the Test Suite
Execute the following command to run the tests:
```bash
docker exec oowlish_project python manage.py test
```

---

## Project Endpoints

### 1. Swagger Documentation
Access the API documentation via Swagger at the following URL (while the application is running):
```
http://localhost:8000/swagger/
```

### 2. UI Endpoints
Below are the endpoints available for the user interface:

| Endpoint                     | View                          | Description                     |
|------------------------------|-------------------------------|---------------------------------|
| `projects/`                          | `ProjectListView`             | Displays a list of all projects. |
| `projects/{id}/`                 | `ProjectDetailView`           | Displays details for a specific project. |
| `projects/create/`                   | `ProjectCreateView`           | Allows creating a new project. |
| `projects/{id}/update/`          | `ProjectUpdateView`           | Allows updating a specific project. |
| `projects/{id}/delete/`          | `ProjectDeleteView`           | Allows deleting a specific project. |
| `projects/distances/`                | `ProjectDistanceListView`     | Displays a list of project distances. |
