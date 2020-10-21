# DNSTwist Domain Monitoring Service

Web application that provides email alerts when fuzzy domains are registered.

## Getting started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Using a Visual Studio Code Dev Container

The reccomended way to develop for this project is within a [Visual Studio Code Dev Container](https://code.visualstudio.com/docs/remote/containers). A configuration is included with this project.

To run the application within the Dev Container environment, enter in the Visual Studio Code terminal:

```
flask run
```

The REST API will be available at the host at `localhost:5000`.

### Using Docker

A `docker-compose` file is included. Simply run:

```
docker-compose up -d
```

The REST API will be available at the host at `localhost:5000`.

## Running the tests

The tests are run from the project root directory using pytest:

```
pytest
```

## Known issues

- Monthly scans take place on the first day of each month, rather than the day of the month in `startAt`
- Authentication is currently unimplemented