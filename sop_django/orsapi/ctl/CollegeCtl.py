import json
from django.http import JsonResponse
from ..ctl import ErrorCtl
from ..ctl.BaseCtl import BaseCtl
from ..models import College
from ..service.CollegeService import CollegeService
from ..utility.DataValidator import DataValidator


class CollegeCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id')
        self.form['name'] = requestForm.get('name')
        self.form['address'] = requestForm.get('address')
        self.form['state'] = requestForm.get('state')
        self.form['city'] = requestForm.get('city')
        self.form['phoneNumber'] = requestForm.get('phoneNumber')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.address = self.form['address']
        obj.state = self.form['state']
        obj.city = self.form['city']
        obj.phoneNumber = self.form['phoneNumber']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['address'] = obj.address
        self.form['state'] = obj.state
        self.form['city'] = obj.city
        self.form['phoneNumber'] = obj.phoneNumber

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if DataValidator.isNull(self.form['name']):
            inputError['name'] = "College Name can not be null"
            self.form['error'] = True

        else:
            if DataValidator.isalphacehck(self.form['name']):
                inputError['name'] = "College Name considers only letters"
                self.form['error'] = True

        if DataValidator.isNull(self.form['address']):
            inputError['address'] = "College Address can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['state'])):
            inputError['state'] = "College State can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['city'])):
            inputError['city'] = "College City can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['phoneNumber'])):
            inputError['phoneNumber'] = "College Phone Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ismobilecheck(self.form['phoneNumber'])):
                inputError['phoneNumber'] = "Only numbers's allowed which starts with 6,7,8,9"
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
            uniqueAttrib = {"name": self.form['name']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the user
            college = self.form_to_model(College())
            self.get_service().save(college)
            res["success"] = True
            res["result"]["data"] = college.id
            res["result"]["message"] = "College added successfully"
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
                res["result"]["lastId"] = College.objects.last().id
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get(self, request, params={}):
        try:
            college = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (college != None):
                res["success"] = True
                res["result"]["data"] = college.to_json()
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            college = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (college != None):
                self.get_service().delete(params["id"])
                res["success"] = True
                res["result"]["data"] = college.to_json()
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
            college_list = CollegeService().preload()
            preloadList = []
            for x in college_list:
                preloadList.append(x.to_json())
            res["result"]["courseList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return CollegeService()