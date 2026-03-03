from ..models import Marksheet
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class MarksheetService(BaseService):

    def duplicate(self, rollNumber, pk=0):
        """
        Check if a marksheet with the same rollNumber exists.
        pk > 0 indicates update operation; exclude that record.
        """
        try:
            qs = self.get_model().objects.filter(rollNumber=rollNumber)

            if pk > 0:
                qs = qs.exclude(id=pk)

            return qs.exists()

        except Exception as ex:
            # Use BaseService method to map OperationalError or other DB errors
            self.map_and_throw_exception(ex)

    def search(self, params):
        try:
            pageNo = (params["pageNo"]) * self.pageSize
            sql = "select * from sos_marksheet where 1=1"
            val = params.get("name", None)
            if DataValidator.isNotNull(val):
                sql += " and name like '" + val + "%%'"
            sql += " limit %s, %s"
            print('---------^^^^^^',sql)
            cursor = connection.cursor()
            cursor.execute(sql, [pageNo, self.pageSize])
            result = cursor.fetchall()
            columnName = ("id", "rollNumber", "name", "physics", "chemistry", "maths")
            res = {
                "data": [],
            }
            params["index"] = ((params['pageNo'] - 1) * self.pageSize)
            for x in result:
                print({columnName[i]: x[i] for i, _ in enumerate(x)})
                params['maxId'] = x[0]
                res['data'].append({columnName[i]: x[i] for i, _ in enumerate(x)})
            return res
        except Exception as ex:
            self.map_and_throw_exception(ex)

    def get_model(self):
        return Marksheet