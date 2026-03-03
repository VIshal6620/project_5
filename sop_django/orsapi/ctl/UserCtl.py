import json
from django.http import JsonResponse
from .BaseCtl import BaseCtl
from .ErrorCtl import ErrorCtl
from ..models import User
from ..service.RoleService import RoleService
from ..service.UserService import UserService
from ..utility.DataValidator import DataValidator


class UserCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form["id"] = requestForm.get("id", '')
        self.form["firstName"] = requestForm.get("firstName", '')
        self.form["lastName"] = requestForm.get("lastName", '')
        self.form["loginId"] = requestForm.get("loginId", '')
        self.form["password"] = requestForm.get("password", '')
        self.form["confirmPassword"] = requestForm.get("confirmPassword", '')
        self.form["dob"] = requestForm.get("dob", '')
        self.form["address"] = requestForm.get("address", '')
        self.form["gender"] = requestForm.get("gender", '')
        self.form["mobileNumber"] = requestForm.get("mobileNumber", '')
        self.form["roleId"] = requestForm.get("roleId", '')
        if self.form['roleId'] != '':
            try:
                role = RoleService().get(self.form['roleId'])
                self.form["roleName"] = role.name
            except Exception as ex:
                return ErrorCtl.handle(ex)

    def form_to_model(self, obj):
        try:
            role = RoleService().get(self.form['roleId'])
        except Exception as ex:
            return ErrorCtl.handle(ex)
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.firstName = self.form["firstName"]
        obj.lastName = self.form["lastName"]
        obj.loginId = self.form["loginId"]
        obj.password = self.form["password"]
        obj.confirmPassword = self.form["confirmPassword"]
        obj.dob = self.form["dob"]
        obj.address = self.form["address"]
        obj.gender = self.form["gender"]
        obj.mobileNumber = self.form["mobileNumber"]
        obj.roleId = self.form["roleId"]
        obj.roleName = role.name
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["firstName"] = obj.firstName
        self.form["lastName"] = obj.lastName
        self.form["loginId"] = obj.loginId
        self.form["password"] = obj.password
        self.form["confirmPassword"] = obj.confirmPassword
        self.form["dob"] = obj.dob.strftime("%Y-%m-%d")
        self.form["address"] = obj.address
        self.form["gender"] = obj.gender
        self.form["mobileNumber"] = obj.mobileNumber
        self.form["roleId"] = obj.roleId
        self.form["roleName"] = obj.roleName

    def input_validation(self):
        super().input_validation()
        inputError = self.form["inputError"]

        if (DataValidator.isNull(self.form["firstName"])):
            inputError["firstName"] = "First Name is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["lastName"])):
            inputError["lastName"] = "Last Name is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["loginId"])):
            inputError["loginId"] = "Login ID is required"
            self.form["error"] = True
        else:
            if (DataValidator.isemail(self.form['loginId'])):
                inputError['loginId'] = "Login ID must be like student@gmail.com"
                self.form['error'] = True

        if (DataValidator.isNull(self.form["password"])):
            inputError["password"] = "Password is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["confirmPassword"])):
            inputError["confirmPassword"] = "Confirm Password is required"
            self.form["error"] = True

        if (DataValidator.isNotNull(self.form['confirmPassword'])):
            if (self.form['password'] != self.form['confirmPassword']):
                inputError['confirmPassword'] = "Password & Confirm Password are not same"
                self.form["error"] = True

        if (DataValidator.isNull(self.form["dob"])):
            inputError["dob"] = "DOB is required"
            self.form["error"] = True
        else:
            if (DataValidator.isDate(self.form['dob'])):
                inputError['dob'] = "Incorrect Date of birth"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['gender'])):
            inputError['gender'] = "Gender is required"
            self.form['error'] = True

        if (DataValidator.isNull(self.form["address"])):
            inputError["address"] = "Address is required"
            self.form["error"] = True

        if (DataValidator.isNull(self.form["mobileNumber"])):
            inputError["mobileNumber"] = "Mobile Number is required"
            self.form["error"] = True
        else:
            if (DataValidator.ismobilecheck(self.form['mobileNumber'])):
                inputError['mobileNumber'] = "Mobile No. should start with 6,7,8,9"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['roleId'])):
            inputError['roleId'] = "Role Name is required"
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
            uniqueAttrib = {"loginId" : self.form['loginId']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the user
            user = self.form_to_model(User())
            self.get_service().save(user)
            res["success"] = True
            res["result"]["data"] = user.id
            res["result"]["message"] = "User added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def search(self, request, params={}):
        print('--------------this is search')
        try:
            json_request = json.loads(request.body)
            res = {"result": {}, "success": True}
            if (json_request):
                params["firstName"] = json_request.get("firstName", None)
                params["loginId"] = json_request.get("loginId", None)
                params["roleId"] = json_request.get("roleId", None)
                params["pageNo"] = json_request.get("pageNo", None)
                print('--------------^^^', params["pageNo"])
            records = self.get_service().search(params)
            if records and records.get("data"):
                res["success"] = True
                res["result"]["data"] = records["data"]
                res["result"]["lastId"] = User.objects.last().id
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get(self, request, params={}):
        try:
            user = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (user != None):
                res["success"] = True
                res["result"]["data"] = user.to_json()
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            user = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (user != None):
                self.get_service().delete(params["id"])
                records = self.get_service().search(params)
                if records and records.get("data"):
                    res["result"]["data"] = records["data"]
                    res["result"]["lastId"] = User.objects.last().id
                res["success"] = True
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
            role_list = RoleService().preload()
            preloadList = []
            for x in role_list:
                preloadList.append(x.to_json())
            res["result"]["roleList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return UserService()