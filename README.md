# broker-api
***

## API endpoints

This API's uses the OpenApi 3.0 standard for it's documentation. You can access it through a ~~[Redocs's page]()~~ or, if you prefer, directly through it's ~~yaml [file]()~~. 

## API Install Guide

*This project is meant to run using **python 3.8** in an Unix-like system , other versions and OSs may not work.*

All dependencies are listed on requirements.txt file. Its strongly recommended to run service in a virtual environment.

### Clone project
```sh
$ git clone git@github.com:hbontempo-br/registration-validator-api.git
```

### Setup a Virtual Environmnet
For linux/Debian distros:
```sh
$ sudo apt-get python3-venv
$ python3 -m venv .venv
$ source .venv/bin/activate
```
#### Install dependencies

From inside the project's folder:

```sh
$ pip3 install -r requirements.txt
```

#### Environment Variables

This project requires this environment variables:

| Variable | Definition | Example | Default |
| - | - | - | - |
| DB_ADDRESS | The address of application MongoDB's cluster | cluster0-2ai50.gcp.mongodb.net | |
| DB_DATABASE | Name of the database that the data is registered | - | registration_validator |
| DB_USER | Application's MongoDB user | CoolUser | |
| DB_PASSWORD | Application's MongoDB password | CoolPassword | |
| GUNICORN_WORKER_TIMEOUT | Number of gunicorn workers that you want | 2 | 1 |
| COMMIT | The commit of this you running application (for better debbuging) | ca82a6dff817ec66f44342007202690a93763949 | None |



## Running the API locally

For local run you must set the environment variables manually or with some tool (pycharm has a nice plugin) and run this simple command:
```sh
$ .venv/bin/gunicorn -b "0.0.0.0:3000" -w 1 -t 3000 --reload app
```
If http://localhost:3000 is returning the api name and current version, everything is running fine.

## Contributing

This project has a strict formatting validation, but it's super easy to adhere to. Just use the automatic pre-commit.

### Install the pre commit:

From inside the project's folder:

Make sure the dependencies refereed on requirements-dev.txt are installed:

```sh
$ pip3 install -r requirements-dev.txt
```

Install the pre-commit:

```sh
$ pre-commit install
```

### Using it:

Just make a commit! On every commit now on all the super strict formatting is taken care of automagically.

If you want to run the validation without a commit just run:
```sh
$ pre-commit run --all-files
```

## Deploying API

```
Under construction
```

## Tests

From inside the project's folder:

Make sure the dependencies refereed on requirements-dev.txt are installed:

```sh
$ pip3 install -r requirements-dev.txt
```

Run pytest:

```sh
$ pytest test
```


<br/>
<br/>
<br/>

---

