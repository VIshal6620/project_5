import { Component } from '@angular/core';
import { BaseCtl } from '../base.component';
import { Router } from '@angular/router';
import { HttpServiceService } from '../http-service.service';

@Component({
  selector: 'app-changepassword',
  templateUrl: './changepassword.component.html',
  styleUrls: ['./changepassword.component.css']
})
export class ChangepasswordComponent {

  form: any = {
    error: false,
    message: '',
    data: { id: null },
    inputerror: {},
  };

  constructor(public httpService: HttpServiceService, private route: Router) {

  }
  changePassword() {
    var _self = this;
    console.log(localStorage.getItem("id"))
    this.form.data.id = localStorage.getItem("id")
    console.log(this.form)
    this.httpService.post("http://localhost:8000/orsapi/ChangePassword/submit", this.form.data, function (res: any) {
      _self.form.message = '';
      _self.form.inputerror = {};
      if (res.success) {
        _self.form.message = res.result.message;
        _self.form.data.id = res.result.data;
      } else {
        _self.form.error = true;
        if (res.result.inputerror) {
          _self.form.inputerror = res.result.inputerror;
        }
        _self.form.message = res.result.message;
      }
    });

  }

}