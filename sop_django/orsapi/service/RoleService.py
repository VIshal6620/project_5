from .BaseService import BaseService
from ..models import Role


class RoleService(BaseService):
    def is_duplicate(self, name, exclude_id=None):
        try:
            qs = Role.objects.filter(name=name)
            if exclude_id:
                qs = qs.exclude(id=exclude_id)
            return qs.exists()

        except Exception as ex:
            self.map_and_throw_exception(ex)

    def search(self, params=None):
        try:
            qs = Role.objects.all()

            if params and params.get("id"):
                qs = qs.filter(id=params["id"])

            return {
                "data": [x.to_json() for x in qs],
                "lastId": qs.last().id if qs.exists() else None
            }
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def get_model(self):
        return Role

