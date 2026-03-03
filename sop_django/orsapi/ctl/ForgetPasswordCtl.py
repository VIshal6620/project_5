import json
from django.http import JsonResponse
from .BaseCtl import BaseCtl
from .ErrorCtl import ErrorCtl
from ..utility.DataValidator import DataValidator
from ..service.ForgetPasswordService import ForgetPasswordService
from ..service.EmailService import EmailService
from ..service.EmailMessege import EmailMessege
from ..models import User


class ForgetPasswordCtl(BaseCtl):

    def request_to_form(self, requestFrom):
        self.form['loginId'] = requestFrom.get('loginId','')

    def input_validation(self):
        super().input_validation()
        inputError = self.form['inputError']

        if DataValidator.isNull(self.form['loginId']):
            inputError['loginId'] = "Login Id can not be null"
            self.form['error'] = True
        else:
            if (DataValidator.isemail(self.form['loginId'])):
                inputError['loginId'] = "Login ID must be like student@gmail.com"
                self.form['error'] = True
        return self.form['error']

    def submit(self, request, params={}):
        try:
            json_request = json.loads(request.body)
            self.request_to_form(json_request)
            res = {"result": {}, "success": True}
            if (self.input_validation()):
                res["success"] = False
                res["result"]["inputerror"] = self.form["inputError"]
                return JsonResponse(res)
            else:
                try:
                    user = self.get_service().find_by_login(self.form)
                    if user is None:
                        res["success"] = False
                        res["result"]["message"] = "Login ID is incorrect"
                        return JsonResponse(res)

                    emailMessage = EmailMessege()
                    emailMessage.to = [user.loginId]
                    emailMessage.subject = "Forget Password"

                    mail_response = EmailService.send(emailMessage, "forgetPassword", user)

                    if mail_response == 1:
                        res["success"] = True
                        res["result"]["message"] = "Your password has been sent successfully"
                    else:
                        res["success"] = False
                        res["result"]["message"] = "Please check your Internet connection"
                except User.DoesNotExist:
                    res["success"] = False
                    res["result"]["message"] = "Login ID is incorrect"
                except Exception as ex:
                    return ErrorCtl.handle(ex)

            return JsonResponse(res)
        except Exception as ex:
            return ErrorCtl.handle(ex)

    def get_service(self):
        return ForgetPasswordService()