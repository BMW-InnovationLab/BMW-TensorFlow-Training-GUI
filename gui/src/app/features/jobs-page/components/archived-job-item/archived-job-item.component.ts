import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import {DataSenderFirstApiService} from "../../../../core/services/data-sender-first-api.service";
import {DataGetterSecondApiService} from "../../../../core/services/data-getter-second-api.service";
import {NzMessageService} from "ng-zorro-antd/message";
import {switchMap} from "rxjs/operators";
import {environment} from "../../../../../environments/environment";
import {fromEvent, Observable, Subscription} from "rxjs";

@Component({
    selector: 'app-archived-job-item',
    templateUrl: './archived-job-item.component.html',
    styleUrls: ['./archived-job-item.component.css']
})
export class ArchivedJobItemComponent implements OnInit {
    @Input() job_name: string;
    @Output() jobRemoved: EventEmitter<string> = new EventEmitter<string>();
    public mobile: boolean;
    private selectedJobsArray = [];
    private resizeObservable: Observable<Event>
    private resizeSubscription: Subscription

    constructor(private dataSenderFirstApi: DataSenderFirstApiService,
                private dataGetterSecondApi: DataGetterSecondApiService,
                private message: NzMessageService) {
    }

    ngOnInit(): void {
        this.initializeScreenSettings();
        this.resizeObservable = fromEvent(window, 'resize');
        this.resizeSubscription = this.resizeObservable.subscribe(() => {
            this.initializeScreenSettings();
        });
    }

    ngOnDestroy(): void {
        this.resizeSubscription.unsubscribe();
    }

    public onJobRemove() {
        this.jobRemoved.emit(this.job_name);
    }

    public getTensorboardPort() {
        this.selectedJobsArray.push(this.job_name);
        let tensorboardPort: number;
        this.dataSenderFirstApi.archivedTensorboardPort({name: this.job_name})
            .pipe(switchMap((res: number) => {
                tensorboardPort = res;
                return this.dataSenderFirstApi.refreshTensorboard({name: this.job_name});
            }))
            .subscribe((res: any) => {
                if (res.success) {
                    setTimeout(() => {
                        const url = environment.url + tensorboardPort;
                        window.open(url);
                        const index = this.selectedJobsArray.indexOf(this.job_name);
                        this.selectedJobsArray.splice(index, 1);
                    }, 4000);
                }
            }, error => this.message.error(error || 'An error has occurred'));
    }

    public loadingButton() {
        return this.selectedJobsArray.includes(this.job_name);
    }

    private initializeScreenSettings() {
        this.mobile = window.innerWidth <= 1024;
    }
}
