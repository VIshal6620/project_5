from ..models import Course
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class CourseService(BaseService):

    def duplicate(self, name, pk=0):
        try:
            q = self.get_model().objects.filter(name=name)

            if pk > 0:
                q = q.exclude(id=pk)

            return q.exists()

        except Exception as ex:
            self.map_and_throw_exception(ex)

    def search(self, params):
        try:
            pageNo = (params['pageNo']) * self.pageSize
            sql = "select * from sos_course where 1=1"
            val = params.get("name", None)
            if DataValidator.isNotNull(val):
                sql += " and name like '" + val + "%%'"
            sql += " limit %s, %s"
            cursor = connection.cursor()
            cursor.execute(sql, [pageNo, self.pageSize])
            result = cursor.fetchall()
            columnName = ('id', 'name', 'description', 'duration')
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
        return Course