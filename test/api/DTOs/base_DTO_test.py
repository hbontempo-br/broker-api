import unittest

from api.DTOs.base_DTO import BaseDTO


class TestBaseDTO(unittest.TestCase):
    def test_to_dict(self):
        class MockDTOChild(BaseDTO):
            def __init__(self, model):
                BaseDTO.__init__(self=self, model=model)

            def to_dict(self):
                return "ok"

        class MockDTO(BaseDTO):
            def __init__(self, model):
                BaseDTO.__init__(self=self, model=model)

                self.root = "ok"
                self.dict = {"o": "k"}
                self.list = ["o", "k"]
                self.child = MockDTOChild(model=model)

        mock_dto = MockDTO(model=object)

        expected_dict = {
            "root": "ok",
            "dict": {"o": "k"},
            "list": [
                "o",
                "k",
            ],
            "child": "ok",
        }

        actual_dict = mock_dto.to_dict()

        self.assertDictEqual(expected_dict, actual_dict)
