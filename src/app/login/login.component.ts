import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { HttpServiceService } from '../http-service.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html'
})

export class LoginComponent implements OnInit {  // <-- implements OnInit

  endpoint = "http://localhost:8000/orsapi/Login/auth/";

  form: any = {
    error: false,
    message: '',
    data: {},
    inputerror: {},
  };

  constructor(
    private httpService: HttpServiceService,
    private router: Router,
    private route: ActivatedRoute   // <-- inject ActivatedRoute
  ) {}

  ngOnInit(): void {
    // 🔥 Read errorMessage from URL
    this.route.queryParams.subscribe(params => {
      if (params['errorMessage']) {
        this.form.error = true;
        this.form.message = params['errorMessage'];
      }
    });
  }

  signIn() {
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

      if (res.success) {
        localStorage.setItem("firstName", res.result.data.firstName);
        localStorage.setItem("roleName", res.result.data.roleName);
        localStorage.setItem("loginId", res.result.data.loginId);
        localStorage.setItem("id", res.result.data.id);
        localStorage.setItem('token', 'Bearer ' + res.result.token)

        _self.router.navigateByUrl('dashboard');
        console.log(res.result.data.loginId);
        console.log(res.result.token)
        
      }
    });
  }

  signUp() {
    this.router.navigateByUrl('signup');
  }
}