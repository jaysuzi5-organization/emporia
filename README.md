# Documentation for emporia
### fastAPI: Exposes Emporia APIs and logs the data to a PostgreSQL database


This application has two generic endpoints:

| Method | URL Pattern           | Description             |
|--------|-----------------------|--------------------|
| GET    | /api/v1/emporia/info         | Basic description of the application and container     |
| GET    | /api/v1/emporia/health    | Health check endpoint     |



## CRUD Endpoints:
| Method | URL Pattern           | Description             | Example             |
|--------|-----------------------|--------------------|---------------------|
| GET    | /api/v1/emporia         | List all emporia     | /api/v1/emporia       |
| GET    | /api/v1/emporia/{id}    | Get emporia by ID     | /api/v1/emporia/42    |
| POST   | /api/v1/emporia         | Create new emporia    | /api/v1/emporia       |
| PUT    | /api/v1/emporia/{id}    | Update emporia (full) | /api/v1/emporia/42    |
| PATCH  | /api/v1/emporia/{id}    | Update emporia (partial) | /api/v1/emporia/42 |
| DELETE | /api/v1/emporia/{id}    | Delete emporia        | /api/v1/emporia/42    |


### Access the info endpoint
http://home.dev.com/api/v1/emporia/info

### View test page
http://home.dev.com/emporia/test/emporia.html

### Swagger:
http://home.dev.com/api/v1/emporia/docs