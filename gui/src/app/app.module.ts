import {BrowserModule} from '@angular/platform-browser';
import {NgModule} from '@angular/core';

import {AppRoutingModule, routingComponents} from './app-routing.module';

import {AppComponent} from './app.component';
import {FormsModule, ReactiveFormsModule} from '@angular/forms';
import {HTTP_INTERCEPTORS, HttpClientModule} from '@angular/common/http';
import {BrowserAnimationsModule} from '@angular/platform-browser/animations';
import {en_US, NZ_I18N} from 'ng-zorro-antd/i18n';
import {registerLocaleData} from '@angular/common';
import en from '@angular/common/locales/en';
import {NzPageHeaderModule} from 'ng-zorro-antd/page-header';
import {NzButtonModule} from 'ng-zorro-antd/button';
import {NzIconModule} from 'ng-zorro-antd/icon';
import {StepperPageComponent} from './features/stepper-page/stepper-page.component';
import {PrepareDatasetComponent} from './features/stepper-page/components/prepare-dataset/prepare-dataset.component';
import {GeneralSettingsComponent} from './features/stepper-page/components/general-settings/general-settings.component';
import {HyperParametersComponent} from './features/stepper-page/components/hyper-parameters/hyper-parameters.component';
import {ScrollingModule} from '@angular/cdk/scrolling';
import {
    AdvancedHyperParametersComponent
} from './features/stepper-page/components/advanced-hyper-parameters/advanced-hyper-parameters.component';
import {ErrorHandler} from './core/interceptors/error-handler';
import {NzMessageModule} from 'ng-zorro-antd/message';
import {NotFoundComponent} from './core/components/not-found/not-found.component';
import {HeaderComponent} from './shared/components/header/header.component';
import {JobItemComponent} from './features/jobs-page/components/job-item/job-item.component';
import {LogsModalComponent} from './features/jobs-page/components/logs-modal/logs-modal.component';
import {NzPopoverModule} from "ng-zorro-antd/popover";
import {NzDividerModule} from "ng-zorro-antd/divider";
import {NzListModule} from "ng-zorro-antd/list";
import {NzEmptyModule} from "ng-zorro-antd/empty";
import {NzGridModule} from 'ng-zorro-antd/grid';
import {NzPaginationModule} from "ng-zorro-antd/pagination";
import {NzPopconfirmModule} from "ng-zorro-antd/popconfirm";
import {NzLayoutModule} from 'ng-zorro-antd/layout';
import {NzCardModule} from "ng-zorro-antd/card";
import {NzStepsModule} from "ng-zorro-antd/steps";
import {NzInputNumberModule} from "ng-zorro-antd/input-number";
import {NzToolTipModule} from "ng-zorro-antd/tooltip";
import {NzAlertModule} from "ng-zorro-antd/alert";
import {NzBadgeModule} from "ng-zorro-antd/badge";
import {NzModalModule} from "ng-zorro-antd/modal";
import {NzSelectModule} from "ng-zorro-antd/select";
import {NzFormModule} from "ng-zorro-antd/form";
import {NzInputModule} from "ng-zorro-antd/input";
import {NzDropDownModule} from "ng-zorro-antd/dropdown";
import {NzTagModule} from "ng-zorro-antd/tag";
import {NzSwitchModule} from "ng-zorro-antd/switch";
import {NzDrawerModule} from 'ng-zorro-antd/drawer';
import {ArchivedJobItemComponent} from "./features/jobs-page/components/archived-job-item/archived-job-item.component";
import {NzCheckboxModule} from "ng-zorro-antd/checkbox";
import { JobSearchComponent } from './features/jobs-page/components/job-search/job-search.component';

registerLocaleData(en);

@NgModule({
    declarations: [
        AppComponent,
        routingComponents,
        StepperPageComponent,
        PrepareDatasetComponent,
        GeneralSettingsComponent,
        HyperParametersComponent,
        AdvancedHyperParametersComponent,
        NotFoundComponent,
        HeaderComponent,
        JobItemComponent,
        LogsModalComponent,
        ArchivedJobItemComponent,
        JobSearchComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        FormsModule,
        HttpClientModule,
        BrowserAnimationsModule,
        NzPageHeaderModule,
        NzButtonModule,
        NzIconModule,
        NzDividerModule,
        NzPopoverModule,
        NzEmptyModule,
        NzGridModule,
        NzCardModule,
        NzListModule,
        NzPaginationModule,
        NzPopconfirmModule,
        NzLayoutModule,
        NzStepsModule,
        ReactiveFormsModule,
        NzFormModule,
        NzInputModule,
        NzSelectModule,
        NzInputNumberModule,
        NzAlertModule,
        NzToolTipModule,
        NzBadgeModule,
        NzModalModule,
        ScrollingModule,
        // NgZorroAntdModule,
        NzMessageModule,
        NzDropDownModule,
        NzTagModule,
        NzSwitchModule,
        NzDrawerModule,
        NzCheckboxModule
    ],
    providers: [
        {
            provide: NZ_I18N, useValue: en_US
        },
        {
            provide: HTTP_INTERCEPTORS,
            useClass: ErrorHandler,
            multi: true
        }
    ], bootstrap: [AppComponent]
})
export class AppModule {
}
