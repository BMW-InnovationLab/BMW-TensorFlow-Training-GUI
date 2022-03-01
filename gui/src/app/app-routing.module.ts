import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';

import {JobsPageComponent} from './features/jobs-page/jobs-page.component';
import {LandingPageComponent} from './core/components/landing_page/landing-page.component';
import {StepperPageComponent} from './features/stepper-page/stepper-page.component';

const routes: Routes = [
  {
    path: '',
    component: LandingPageComponent
  },
  {
    path: 'jobs',
    component: JobsPageComponent
  },
  {
    path: 'stepper',
    component: StepperPageComponent
  }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }

export const routingComponents = [LandingPageComponent, JobsPageComponent];
