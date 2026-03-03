import { HttpErrorResponse, HttpEvent, HttpHandler, HttpInterceptor, HttpRequest } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { Router } from '@angular/router';
import { Observable, throwError } from 'rxjs';
import { catchError } from 'rxjs/operators';

@Injectable({
  providedIn: 'root'
})
export class AuthServiceService implements HttpInterceptor {

  token: any

  constructor(private router: Router) { }

  intercept(req: HttpRequest<any>, next: HttpHandler): Observable<HttpEvent<any>> {

    console.log('in auth service intercept method....!!!')

    if (localStorage.getItem('firstName') && localStorage.getItem('token')) {
      this.token = localStorage.getItem('token')
      req = req.clone({
        setHeaders: {
          Authorization: this.token
        }
      })
    }
    console.log(req.headers.get("Authorization"))
    return next.handle(req).pipe(
      catchError((error: HttpErrorResponse) => {
        if (error.status === 401) {
          localStorage.clear();
          console.log("error = > ", error.error.error)
          this.router.navigate(['/login'], {
            queryParams: { errorMessage: error.error.error },
          });
        }
        return throwError(error);
      })
    );
  }
}