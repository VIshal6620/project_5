import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MarksheetListComponent } from './marksheet-list.component';

describe('MarksheetListComponent', () => {
  let component: MarksheetListComponent;
  let fixture: ComponentFixture<MarksheetListComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [MarksheetListComponent]
    });
    fixture = TestBed.createComponent(MarksheetListComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
