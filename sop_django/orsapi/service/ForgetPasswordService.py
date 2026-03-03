from ..models import User
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService


class ForgetPasswordService(BaseService):

    def find_by_login(self, params):
        try:
            user = self.get_model().objects.get(loginId=params['loginId'])
            return user
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def get_model(self):
        return User