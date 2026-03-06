import json
from django.http import JsonResponse
from ..ctl.BaseCtl import BaseCtl
from ..ctl.ErrorCtl import ErrorCtl
from ..models import Subject
from ..service.CourseService import CourseService
from ..service.SubjectService import SubjectService
from ..utility.DataValidator import DataValidator


class SubjectCtl(BaseCtl):

    # def preload(self, request, params={}):
    #     self.dynamic_preload = CourseService().preload()

    def request_to_form(self, requestForm):
        self.form['id'] = requestForm.get('id','')
        self.form['name'] = requestForm.get('name','')
        self.form['description'] = requestForm.get('description','')
        self.form['courseId'] = requestForm.get('courseId','')
        if self.form['courseId'] != '':
            course = CourseService().get(self.form['courseId'])
            self.form["courseName"] = course.name

    def form_to_model(self, obj):
        course = CourseService().get(self.form['courseId'])
        pk = int(self.form['id'])
        if (pk > 0):
            obj.id = pk
        obj.name = self.form['name']
        obj.description = self.form['description']
        obj.courseId = self.form['courseId']
        obj.courseName = course.name
        return obj

    def model_to_form(self, obj):
        if (obj == None):
            return
        self.form['id'] = obj.id
        self.form['name'] = obj.name
        self.form['description'] = obj.description
        self.form['courseId'] = obj.courseId
        self.form['courseName'] = obj.courseName

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if (DataValidator.isNull(self.form['name'])):
            inputError['name'] = "Subject Name can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isalphacehck(self.form['name'])):
                inputError['name'] = "Name contains only letters"
                self.form['error'] = True

        if (DataValidator.isNull(self.form['description'])):
            inputError['description'] = "Subject Description can not be null"
            self.form['error'] = True

        if (DataValidator.isNull(self.form['courseId'])):
            inputError['courseId'] = "Course can not be null"
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
            subject = self.form_to_model(Subject())
            self.get_service().save(subject)
            res["success"] = True
            res["result"]["data"] = subject.id
            res["result"]["message"] = "Subject added successfully"
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
                res["result"]["lastId"] = Subject.objects.last().id
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)


    def get(self, request, params={}):
        try:
            subject = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (subject != None):
                res["success"] = True
                res["result"]["data"] = subject.to_json()
            else:
                res["success"] = False
                res["result"]["message"] = "No record found"
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def delete(self, request, params={}):
        try:
            subject = self.get_service().get(params["id"])
            res = {"result": {}, "success": True}
            if (subject != None):
                self.get_service().delete(params["id"])
                res["success"] = True
                res["result"]["data"] = subject.to_json()
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
            course_list = CourseService().preload()
            preloadList = []
            for x in course_list:
                preloadList.append(x.to_json())
            res["result"]["courseList"] = preloadList
            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return SubjectService()