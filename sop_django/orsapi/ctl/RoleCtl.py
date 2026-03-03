import json
from django.http import JsonResponse
from .ErrorCtl import ErrorCtl
from .BaseCtl import BaseCtl
from ..utility.DataValidator import DataValidator
from ..models import Role
from ..service.RoleService import RoleService


class RoleCtl(BaseCtl):

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id', '')
        self.form['name'] = requestForm.get('name', '')
        self.form['description'] = requestForm.get('description', '')

    def form_to_model(self, obj):
        pk = int(self.form['id'])
        if pk > 0:
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form["id"] = obj.id
        self.form["name"] = obj.name
        self.form["description"] = obj.description

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Role Name is required"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Role Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Description is required"
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
            uniqueAttrib = {"name" : self.form['name']}
            duplicateErrors = self.get_service().mduplicateFields(uniqueAttrib, pk)
            size = len(duplicateErrors)
            if (size > 0):
                res["success"] = False
                res["result"]["inputerror"] = duplicateErrors
                return JsonResponse(res)

            # Add/ Update the user
            role = self.form_to_model(Role())
            self.get_service().save(role)
            res["success"] = True
            res["result"]["data"] = role.id
            res["result"]["message"] = "Role added successfully"
            return JsonResponse(res)

        except Exception as ex:
            return ErrorCtl.handle(ex)


    def search(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            if json_request:
                params["id"] = json_request.get("id", None)
                params["pageNo"] = json_request.get("pageNo", None)

            records = self.get_service().search(params)

            if records and records.get("data"):
                return JsonResponse({
                    "success": True,
                    "result": records
                })
            else:
                return JsonResponse({
                    "success": False,
                    "result": {"message": "No record found"}
                })

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get(self, request, params={}):
        try:
            role = self.get_service().get(params["id"])

            if role:
                return JsonResponse({
                    "success": True,
                    "result": {"data": role.to_json()}
                })
            else:
                return JsonResponse({
                    "success": False,
                    "result": {"message": "No record found"}
                })

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            deleted_data = self.get_service().delete(params["id"])

            if deleted_data:
                return JsonResponse({
                    "success": True,
                    "result": {
                        "data": deleted_data,
                        "message": "Data deleted successfully"
                    }
                })
            else:
                return JsonResponse({
                    "success": False,
                    "result": {"message": "Data not found"}
                })

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def preload(self, request, params={}):
        try:
            role_list = self.get_service().preload()

            data = []
            for role in role_list:
                data.append(role.to_json())

            return JsonResponse({
                "success": True,
                "result": {
                    "roleList": data
                }
            })

        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return RoleService()