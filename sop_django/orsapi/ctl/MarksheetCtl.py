import json
from django.http import JsonResponse
from .BaseCtl import BaseCtl
from .ErrorCtl import ErrorCtl
from ..service.StudentService import StudentService
from ..utility.DataValidator import DataValidator
from ..models import Marksheet
from ..service.MarksheetService import MarksheetService

class MarksheetCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['name'] = requestForm.get('name','')
        self.form['rollNumber'] = requestForm.get('rollNumber','')
        self.form['physics'] = requestForm.get('physics','')
        self.form['chemistry'] = requestForm.get('chemistry','')
        self.form['maths'] = requestForm.get('maths','')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.rollNumber = self.form['rollNumber']
        obj.name = self.form['name']
        obj.physics = self.form['physics']
        obj.chemistry = self.form['chemistry']
        obj.maths = self.form['maths']
        return obj

    def model_to_form(self, obj):
        if obj == None:
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['rollNumber'] = obj.rollNumber
        self.form['physics'] = obj.physics
        self.form['chemistry'] = obj.chemistry
        self.form['maths'] = obj.maths

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['rollNumber'])):
            inputError['rollNumber'] = "Roll Number can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeckroll(self.form['rollNumber'])):
                inputError['rollNumber'] = "Roll Number must be alpha numeric"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['physics'])):
            inputError['physics'] = "Physics can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['physics'])):
                inputError['physics'] = "Please Enter Number below 100"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['chemistry'])):
            inputError['chemistry'] = "Chemistry can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['chemistry'])):
                inputError['chemistry'] = "Please Enter Number below 100"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['maths'])):
            inputError['maths'] = "Maths can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.ischeck(self.form['maths'])):
                inputError['maths'] = "Please Enter Number below 100"
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
            #Check unique elements
            pk = int(self.form['id'])
            uniqueAttrib = {"rollNumber" : self.form['rollNumber']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the user
            marksheet = self.form_to_model(Marksheet())
            self.get_service().save(marksheet)
            res["success"] = True
            res["result"]["data"] = marksheet.id
            res["result"]["message"] = "Marksheet added successfully"
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
                res["result"]["lastId"] = Marksheet.objects.last().id
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get(self, request, params={}):
        try:
            marksheet = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (marksheet != None):
                res["success"] = True
                res["result"]["data"] = marksheet.to_json()
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            marksheet = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (marksheet != None):
                self.get_service().delete(params["id"])
                res["success"] = True
                res["result"]["data"] = marksheet.to_json()
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
            student_list = StudentService().preload()
            preloadList = []
            for x in student_list:
                preloadList.append(x.to_json())
            res["result"]["studentList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return MarksheetService()