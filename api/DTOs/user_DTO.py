from ..models import UserModel
from .base_DTO import BaseDTO


class UserDTO(BaseDTO):
    def __init__(self, user_model: UserModel):
        BaseDTO.__init__(self=self, model=user_model)

        self.user_key = user_model.user_key
        self.name = user_model.name
        self.document = user_model.document
        self.email = user_model.email
        self.balance = user_model.balance
        self.created_at = user_model.created_at
