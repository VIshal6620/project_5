import { HttpClient } from '@angular/common/http';
import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { HttpServiceService } from '../http-service.service';

@Component({
  selector: 'app-signup',
  templateUrl: './signup.component.html'
})
export class SignupComponent {
  endpoint = "http://localhost:8000/orsapi/Registration/signup/";

  form: any = {
    error: false,
    message: '',
    data: { id: 0 },
    inputerror: {},
  };

  constructor(private httpService: HttpServiceService, private router: Router) {
  }

  signUp() {
    var _self = this;
    this.httpService.post(this.endpoint, this.form.data, function (res: any) {

      _self.form.message = '';
      _self.form.inputerror = {};

      if (res.result.message) {
        _self.form.message = res.result.message;
      }

      _self.form.error = !res.success;
      if (_self.form.error && res.result.inputerror) {
        _self.form.inputerror = res.result.inputerror;
      }
    });
  }

  reset() {
    location.reload();
  }
}