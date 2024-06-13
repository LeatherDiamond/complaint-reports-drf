# Navigation
* ***[Project description](#project-description)***
* ***[How to start locally](#how-to-start-locally)***
* ***[How to start with Docker](#how-to-start-with-docker)***
* ***[Using the API](#using-the-api)***
* ***[Code formatting and quality checking tools](#code-formatting-and-quality-checking-tools)***
* ***[Pipeline configuration](#pipeline-configuration)***
* ***[Running tests inside the container](#running-tests-inside-the-container)***
* ***[Runing tests locally](#running-tests-locally)***
* ***[Running tests with pipeline](#running-tests-with-pipeline)***
* ***[Why should you try it](#why-should-you-try-it)***
* ***[Licence](#licence)***

# Project description

The project is a multilingual, scalable RESTful API application designed for creating and processing customer complaints for the company. The web application is also optimized for tablets and mobile devices, ensuring an excellent and intuitive user experience.

The API and business logic are implemented using Django and Django REST Framework (DRF). The frontend is crafted with Django template engine, CSS, and JavaScript. The codebase is thoroughly tested and undergoes linting checks, adhering to a consistent style and architectural design influenced by Django paradigms.

Furthermore, the service is containerized within a Docker image. Both the [Dockerfile](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/Dockerfile) and [docker-compose.yml](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/docker-compose.yml) are developed and maintained, ensuring the project follows the 12-factor app principles. Versioning, environment variable configurations, and health checks for components ensure a robust deployment.

The project also includes configured pipeline files for [GitLab](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/.gitlab-ci.yml) and [GitHub](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/.github/workflows/django.yml), ensuring that each new code push triggers the build and launch of the project container, runs tests within the container, and subsequently stops it, providing continuous quality code delivery.

The functional aspect of the project allows the company's clients to create complaints through a graphical interface, and also enables third-party applications to process created complaints using the [available API](#using-the-api). The web application protects against multiple requests through custom middlewares integrated into the project. To ensure efficient use of the database, all attachments added to a complaint are automatically archived and stored as compressed files. These archives can be retrieved from the database via a specific API endpoint.

# How to start locally

1. Clone current repository to your local machine:
 ```
 https://github.com/LeatherDiamond/complaint-reports-drf.git
 ```
2. Navigate to the root directory of the project;
3. Configure `.env` file by assigning values to the variables defined in `.env.sample`;
4. Make sure that [Gettext](https://www.gnu.org/software/gettext/) is installed on your local machine;
5. Activate virtual environment:
```
poetry shell
```
6. Install all dependencies:
```
poetry install
```
7. Apply all migrations:
```
python manage.py migrate
```
8. Create a table for cache in the database:
```
python manage.py createcachetable
```
9. Compile messages for multilanguages in the application:
```
django-admin compilemessages
```
10. Create a superuser to provide future access to django admin panel:
```
python manage.py createsuperuser
```
11. Run development server:
```
python manage.py runserver
```
After completing all the steps, the project will be launched and available at `http://localhost:8000/`.

> ###### NOTE:
> Please note that template files uses links and images just for example. For your company needs you should configure template files respectively.

# How to start with Docker

1. Install [Docker](https://docs.docker.com/engine/install/) on your local machine, if it wasn't done yet, and launch it;
2. Clone current repository to your local machine:
 ```
 https://github.com/LeatherDiamond/complaint-reports-drf.git
 ```
3. Configure `.env` file by assigning values to the variables defined in `.env.sample`;
4. USe the command to build and start the container:
```
docker compose up --build
```
After completing all the steps, the project will be launched and available at `http://localhost:8000/`. 

# Using the API
> ###### **NOTE:** 
> By an `Authorized` request, we mean a request with a JWT. \
> Conversely, by an `Unauthorized` request, we mean a request without a JWT.
Web service provides the following enpoints:

- **GET** `/admin/`.
> ***Unauthorized*** request to get access to Django admin panel.
- **POST** `/api/token/`.
> Generate `access` and `refresh` tokens.
- **POST** `/api/token/refresh/`.
> Refresh the token.
- **GET**/**POST** `/{language}/claim_report/create/` where `{language}` can be `pl`, `en` or `ru`. 
> ***Unauthorized*** `GET` request to render the complaint report form in acordance with chosen language. \
> ***Unauthorized*** `POST` request with neccessary body credentials to create a complaint report instance.
- **GET**/**PUT** `/claim_report/unprocessed_reports/`.
> ***Authorized*** `GET` request to recieve a JSON with a list of all complaint reports with the `processed=False` field.
> ***Authorized*** `PUT` request to set all complaint report instances with `processed=False` field to `processed=True`.
- **GET** `/claim_report/download_archive/<int:pk>/`.
> ***Authorized*** `GET` request to recieve zipped attachments from a complaint report (*if they where provided during the instance creation*). \
> `<int:pk>` is an ID of a related complaint report.

# Code formatting and quality checking tools
> ###### **NOTE:**
> Note, that autolaunch of code quality checking and formatting tools is already included in [Gitlab](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/.gitlab-ci.yml) and [Github](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/.github/workflows/django.yml) pipelines configuration files.
1. Run `poetry shell` to activate environment if it's not active yet;
2. Run `black . --check` to check if the code needs to be reformatted;
3. Run `black .` to reformat the code;
4. Run `flake8` to identify potential issues, such as syntax errors, code style violations, and other coding inconsistencies during the development process;

# Pipeline configuration
> ###### NOTE: 
> To provide correct work of the pipeline, please configure neccessary `REPOSITORY SECRETS` that are mandatory in configuration files.
> Also note that if you are using a **GitLab** you should configure a [GitLab Runner](https://docs.gitlab.com/runner/install/), and depending on its configuration, you may need
> [Docker](https://docs.docker.com/engine/install/) launched locally. For example, if your Runner is configured for local Docker setup, you will need to launch Docker on your machine for
> the pipeline to work correctly because the GitLab pipeline uses [Docker-in-Docker](https://docs.gitlab.com/ee/ci/docker/using_docker_build.html).

The project includes configured pipeline files for [GitLab](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/.gitlab-ci.yml) and [GitHub](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/.github/workflows/django.yml), ensuring that each new code push triggers the build and launch of the project container, runs tests within the container, and subsequently stops it, providing continuous quality code delivery. No matter where your project is stored: `GitHub` or `GitLab`, thanks to configured files the pipeline will be launched automatically.

# Running tests locally

1. Make sure that points `1 - 9` from ***[How to start locally](#how-to-start-locally)*** section are already completed;
2. Launch tests with the command:
```
pytest
```

# Running tests inside the container

1. Make sure that `all the points` from ***[How to start with Docker](#how-to-start-with-docker)*** section are already completed;
2. Enter the `claim.webapp` container with the command:
```
docker exec -it claim.webapp bash
```
3. After you entered the container, launch tests with te command:
```
pytest
```

# Running tests with pipeline

Pipeline configuration files are already set to launch tests automatically. It means that each new code push triggers the build and launch of the project container, runs tests within the container, and subsequently stops it.
> ###### NOTE:
> Take a look at the ***[Pipeline configuration](#pipeline-configuration)*** section for some important notes.

# Why should you try it

***1. Multilingual Support:***
Easily serve a global customer base with built-in multilingual capabilities.

***2. Scalable and Efficient:***
Handles high volumes of complaints smoothly, scaling with your business needs.

***3. User-Friendly:***
Optimized for both tablets and mobile devices, providing a responsive and intuitive user experience.

***4. Reliable and Tested:***
Thoroughly tested codebase ensures stability and minimizes bugs.

***5. Easy Deployment:***
Containerized with Docker, following 12-factor app principles for streamlined development and deployment.

***6. Continuous Integration:***
Automated build, test, and deployment pipelines with GitLab and GitHub ensure continuous delivery of quality code.

***7. Secure:***
Custom middleware protects against multiple requests, enhancing security.

***8. Efficient Database Use:***
Attachments are archived and compressed automatically, optimizing database performance.

***9. API Integration:***
Allows third-party applications to process complaints seamlessly.

By choosing this project, you are investing in a robust, scalable, and user-friendly solution that enhances customer satisfaction and streamlines complaint management processes. 
Experience the difference with a well-engineered application and take your customer service to the next level.

# Licence

**This project is licensed under the Apache-2.0 license - see the [LICENSE](https://github.com/LeatherDiamond/complaint-reports-drf/blob/main/LICENSE) file for details.**

