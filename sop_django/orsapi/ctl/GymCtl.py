import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Gym
from ..service.GymService import GymService
from ..service.LoanService import LoanService
from ..utility.DataValidator import DataValidator


class GymCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id')
        self.form['memberName'] = requestForm.get('memberName')
        self.form['membershipType'] = requestForm.get('membershipType')
        self.form['startDate'] = requestForm.get('startDate')
        self.form['endDate'] = requestForm.get('endDate')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.memberName = self.form['memberName']
        obj.membershipType = self.form['membershipType']
        obj.startDate = self.form['startDate']
        obj.endDate = self.form['endDate']
        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form['id'] = obj.id
        self.form['memberName'] = obj.memberName
        self.form['membershipType'] = obj.membershipType
        self.form['startDate'] = obj.startDate
        self.form['endDate'] = obj.endDate

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['memberName'])):
            inputError['memberName'] = "memberName can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['memberName'])):
                inputError['memberName'] = "memberName contains only number"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['membershipType'])):
            inputError['membershipType'] = "membershipType can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['membershipType'])):
                inputError['membershipType'] = "membershipType contains only number"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['startDate'])):
            inputError['startDate'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['startDate'])):
                inputError['startDate'] = "Incorrect date format, should be YYYY-MM-DD"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['endDate'])):
            inputError['endDate'] = "DOB can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isDate(self.form['endDate'])):
                inputError['endDate'] = "Incorrect date format, should be YYYY-MM-DD"
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
            uniqueAttrib = {"memberName": self.form['memberName']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the user
            gym = self.form_to_model(Gym())
            self.get_service().save(gym)
            res["success"] = True
            res["result"]["data"] = gym.id
            res["result"]["message"] = "Loan added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)


    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["memberName"] = json_request.get("memberName", None)
                params["pageNo"] = json_request.get("pageNo", None)
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = Gym.objects.last().id
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
            gym_list = GymService().preload()
            preloadList = []
            for x in gym_list:
                preloadList.append(x.to_json())
            res["result"]["gymList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return GymService()