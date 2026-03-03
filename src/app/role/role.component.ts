import { Component } from '@angular/core';
import { BaseCtl } from '../base.component';
import { ActivatedRoute } from '@angular/router';
import { ServiceLocatorService } from '../service-locator.service';

@Component({
  selector: 'app-role',
  templateUrl: './role.component.html',
  styleUrls: ['./role.component.css']
})
export class RoleComponent extends BaseCtl{
  constructor(public locator: ServiceLocatorService, route: ActivatedRoute) {
      super(locator.endpoints.ROLE, locator, route);
    }
  
  override preload(): void {
      
  }
}