import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Loan
from ..service.LoanService import LoanService
from ..utility.DataValidator import DataValidator


class LoanCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id')
        self.form['loanAmount'] = requestForm.get('loanAmount')
        self.form['interestRate'] = requestForm.get('interestRate')
        self.form['issueDate'] = requestForm.get('issueDate')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.loanAmount = self.form['loanAmount']
        obj.interestRate = self.form['interestRate']
        obj.issueDate = self.form['issueDate']
        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form['id'] = obj.id
        self.form['loanAmount'] = obj.loanAmount
        self.form['interestRate'] = obj.interestRate
        self.form['issueDate'] = obj.issueDate

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['loanAmount'])):
            inputError['loanAmount'] = "loanAmount can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isinteger(self.form['loanAmount'])):
                inputError['loanAmount'] = "loanAmount contains only number"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['interestRate'])):
            inputError['interestRate'] = "interestRate Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['issueDate'])):
            inputError['issueDate'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['issueDate'])):
                inputError['issueDate'] = "Incorrect date format, should be YYYY-MM-DD"
                self.form['error'] = True

        return self.form['error']


    def save(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            self.request_to_form(json_request)
            res = {"result": {}, "success": True}

            # perform input validation
            if (self.input_validation()):
                res["success"] = False
                res["result"]["inputerror"] = self.form["inputError"]
                return JsonResponse(res)
            # Check unique elements
            pk = int(self.form['id'])
            uniqueAttrib = {"loanAmount": self.form['loanAmount']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the user
            loan = self.form_to_model(Loan())
            self.get_service().save(loan)
            res["success"] = True
            res["result"]["data"] = loan.id
            res["result"]["message"] = "Loan added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)


    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["name"] = json_request.get("name", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Loan.objects.last().id
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get(self, request, params={}):
        try:
            role = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (role != None):
                res["success"] = True
                res["result"]["data"] = role.to_json()
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            role = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (role != None):
                self.get_service().delete(params["id"])
                res["success"] = True
                res["result"]["data"] = role.to_json()
                res["result"]["message"] = "Data has been deleted successfully"
            else:
                res["success"] = False
                res["result"]["message"] = "Data was not deleted"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def preload(self, request, params={}):
        try:
            res = {"result": {}, "success": True}
            loan_list = LoanService().preload()
            preloadList = []
            for x in loan_list:
                preloadList.append(x.to_json())
            res["result"]["loanList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return LoanService()