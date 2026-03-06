import { Component } from '@angular/core';
import { ServiceLocatorService } from '../service-locator.service';
import { BaseListCtl } from '../base-list.component';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-gym-list',
  templateUrl: './gym-list.component.html',
  styleUrls: ['./gym-list.component.css']
})
export class GymListComponent extends BaseListCtl{
  constructor(locator: ServiceLocatorService, route: ActivatedRoute) {
        super(locator.endpoints.GYM, locator, route);
      }

}
