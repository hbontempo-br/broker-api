import os
import unittest
from uuid import uuid4

from utils.environment import get_environment_variable


class TestEnvironment(unittest.TestCase):
    def setUp(self):
        self.test_value = str(uuid4())
        self.valid_env_var = str(uuid4())
        os.environ[self.valid_env_var] = self.test_value
        self.invalid_env_var = str(uuid4())
        if os.environ.get(self.invalid_env_var):
            del os.environ[self.invalid_env_var]

    def tearDown(self):
        if os.environ.get(self.valid_env_var):
            del os.environ[self.valid_env_var]
        if os.environ.get(self.invalid_env_var):
            del os.environ[self.invalid_env_var]

    def test_valid_env_var(self):
        retrieved_value = get_environment_variable(variable_name=self.valid_env_var)
        self.assertEqual(self.test_value, retrieved_value)

    def test_valid_env_var_with_default(self):
        default_value = str(uuid4())
        retrieved_value = get_environment_variable(
            variable_name=self.valid_env_var, default_value=default_value
        )
        self.assertEqual(self.test_value, retrieved_value)

    def test_invalid_env_var(self):
        with self.assertRaises(expected_exception=AttributeError):
            get_environment_variable(variable_name=self.invalid_env_var)

    def test_invalid_env_var_with_default(self):
        default_value = str(uuid4())
        retrieved_value = get_environment_variable(
            variable_name=self.invalid_env_var, default_value=default_value
        )
        self.assertEqual(default_value, retrieved_value)
