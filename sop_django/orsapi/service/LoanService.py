from django.db import connection
from ..models import Loan
from ..service.BaseService import BaseService
from ..utility.DataValidator import DataValidator


class LoanService(BaseService):

    def search(self, params):
        try:
            pageNo = (params['pageNo']) * self.pageSize
            sql = "select * from sos_loan where 1=1"
            val = params.get("loanAmount", None)
            if DataValidator.isNotNull(val):
                sql += " and loanAmount like '" + val + "%%'"
            sql += " limit %s, %s"
            cursor = connection.cursor()
            cursor.execute(sql, [pageNo, self.pageSize])
            result = cursor.fetchall()
            columnName = ('id', 'loanAmount', 'interestRate', 'issueDate')
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
        return Loan

