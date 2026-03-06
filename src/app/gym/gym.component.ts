import { Component } from '@angular/core';
import { BaseCtl } from '../base.component';
import { ServiceLocatorService } from '../service-locator.service';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-gym',
  templateUrl: './gym.component.html',
  styleUrls: ['./gym.component.css']
})
export class GymComponent extends BaseCtl {
   constructor(public locator: ServiceLocatorService, route: ActivatedRoute) {
      super(locator.endpoints.GYM, locator, route);
    }


}
