from abc import ABC, abstractmethod
from django.db import OperationalError
from ..utility.ApplicationException import ApplicationException


class BaseService(ABC):

    def __init__(self):
        self.pageSize = 5

    def map_and_throw_exception(self,ex):

        print(">>>>>>>>>>>>>>inside map and throw method")

        if type(ex) == OperationalError:
            raise ApplicationException(
                "Database service is currently unvailable. Please try again later."
            )
        else:
            raise ApplicationException(
            "Unexpected error occurred"

            )



    def save(self, obj):
        try:
            if obj.id == 0:
                obj.id = None
            obj.save()
            return obj

        except Exception as ex:
            self.map_and_throw_exception(ex)


    def delete(self, obj_id):
        try:
            obj = self.get(obj_id)
            if obj:
                obj.delete()
                return True
            return False
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def get(self, obj_id):
        Model = self.get_model()
        try:
            return Model.objects.get(id=obj_id)
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def search(self):
        try:
            return self.get_model().objects.all()
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def preload(self):
        Model = self.get_model()
        try:
            return Model.objects.all()
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def mduplicateFields(self, dict, exclude_id=None):
        error = {}
        try:
            for uniquekey in dict:
                qs = self.get_model().objects.filter(**{uniquekey: dict[uniquekey]})
                if exclude_id and exclude_id > 0:
                    qs = qs.exclude(id=exclude_id)
                if qs.exists():
                    error[uniquekey] = dict[uniquekey] + " is duplicate"
            return error
        except Exception as ex:
            self.map_and_throw_exception(ex)

    @abstractmethod
    def get_model(self):
        pass
