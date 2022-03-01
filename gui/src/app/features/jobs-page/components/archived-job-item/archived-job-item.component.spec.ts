import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ArchivedJobItemComponent } from './archived-job-item.component';

describe('ArchivedJobItemComponent', () => {
  let component: ArchivedJobItemComponent;
  let fixture: ComponentFixture<ArchivedJobItemComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ArchivedJobItemComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ArchivedJobItemComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
