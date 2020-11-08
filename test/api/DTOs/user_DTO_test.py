import unittest

from api.DTOs.user_DTO import UserDTO
from api.models.user_model import UserModel


class TestUserDTO(unittest.TestCase):
    def setUp(self) -> None:

        self.dto = UserDTO

        self.user_model = UserModel
        self.user_model.user_key = "a_user_key"
        self.user_model.name = "name"
        self.user_model.document = "document"
        self.user_model.email = "email"
        self.user_model.balance = 6.66
        self.user_model.created_at = "a_datetime"

    def test_to_dict(self):
        expected_dict = {
            "user_key": "a_user_key",
            "name": "name",
            "document": "document",
            "email": "email",
            "balance": 6.66,
            "created_at": "a_datetime",
        }
        actual_dict = self.dto(user_model=self.user_model).to_dict()

        self.assertDictEqual(expected_dict, actual_dict)
