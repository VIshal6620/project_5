from ..models import TimeTable
from ..utility.DataValidator import DataValidator
from .BaseService import BaseService
from django.db import connection


class TimeTableService(BaseService):

    def duplicate(self, courseName, subjectName, examDate, pk=0):
        """
        Check if a timetable entry exists for the same course, subject, and exam date.
        pk > 0 indicates update operation; exclude that record.
        """
        try:
            qs = self.get_model().objects.filter(
                courseName=courseName,
                subjectName=subjectName,
                examDate=examDate
            )

            if pk > 0:
                qs = qs.exclude(id=pk)

            return qs.exists()

        except Exception as ex:
            self.map_and_throw_exception(ex)

    def search(self, params):
        try:
            pageNo = (params['pageNo']) * self.pageSize
            sql = "select * from sos_timetable where 1=1"
            val = params.get("courseName", None)
            if (DataValidator.isNotNull(val)):
                sql += " and courseName like '" + val + "%%'"
            sql += " limit %s, %s"
            cursor = connection.cursor()
            cursor.execute(sql, [pageNo, self.pageSize])
            result = cursor.fetchall()
            columnName = ('id', 'examTime', 'examDate', 'subjectId', 'subjectName', 'courseId', 'courseName', 'semester')
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
        return TimeTable