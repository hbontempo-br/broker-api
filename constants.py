import os

from utils.environment import get_environment_variable

# ------- GENERAL ------- #
SERVICE_ROOT = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SERVICE_ROOT, os.pardir))
SERVICE_NAME = get_environment_variable("SERVICE_NAME", "broker-api")
COMMIT = get_environment_variable("COMMIT", "COMMIT")

# ------- DB INFO ------- #
DB_USER = get_environment_variable("DB_USER")
DB_PASSWORD = get_environment_variable("DB_PASSWORD")
DB_ADDRESS = get_environment_variable("DB_ADDRESS")
DB_PORT = get_environment_variable("DB_PORT", "3306")
DB_DATABASE = get_environment_variable("DB_DATABASE", "broker")

# ------- SCHEMA ------- #
SCHEMA_FILE = os.path.join(SERVICE_ROOT, "documentation", "schema.yaml")
