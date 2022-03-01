import {Component, EventEmitter, Input, OnDestroy, OnInit, Output} from '@angular/core';
import {environment} from '../../../../../environments/environment';
import {switchMap} from 'rxjs/operators';
import {AddJob} from '../../../../core/domain/models/add-job';
import {DataSenderFirstApiService} from '../../../../core/services/data-sender-first-api.service';
import {DataGetterSecondApiService} from '../../../../core/services/data-getter-second-api.service';
import {NzMessageService} from "ng-zorro-antd/message";
import {ContainerInfo} from "../../../../core/domain/models/container-info";
import {fromEvent, Observable, Subscription} from "rxjs";

@Component({
    selector: 'app-job-item',
    templateUrl: './job-item.component.html',
    styleUrls: ['./job-item.component.css']
})
export class JobItemComponent implements OnInit, OnDestroy {
    public readonly URL = environment.url + environment.baseEndPoint + '/models_services/';
    @Input() item: ContainerInfo;
    @Input() finishedJobs: Array<string> = [];
    @Input() downloadableModels: any = [];
    @Output() jobRemoved: EventEmitter<string> = new EventEmitter<string>();
    @Output() logsRequested: EventEmitter<string> = new EventEmitter<string>();
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
            this.initializeScreenSettings()
        });
    }

    ngOnDestroy(): void {
        this.resizeSubscription.unsubscribe()
    }

    public onJobRemove() {
        this.jobRemoved.emit(this.item.name);
    }

    public logsButton() {
        this.logsRequested.emit(this.item.name);
    }

    public jobIsDone = () => {
        if (this.finishedJobs !== undefined) {
            return this.finishedJobs.indexOf(this.item.name);
        }
        return -1;
    }

    public downloadResults(): void {
        let specificJobDownloadableModelValue;

        for (const [key, value] of Object.entries(this.downloadableModels)) {
            if (this.item.name + '.zip' === key) {
                specificJobDownloadableModelValue = value;
            }
        }

        const url: string = this.URL + specificJobDownloadableModelValue + '/' + this.item.name + '.zip';
        window.open(url);
    }

    public getTensorboardPort() {
        this.selectedJobsArray.push(this.item.name);
        let tensorboardPort;
        this.dataSenderFirstApi.tensorboardPort({name: this.item.name})
            .pipe(switchMap((res: AddJob) => {
                tensorboardPort = res.tensorboard_port;
                return this.dataGetterSecondApi.refreshTensorboard(res.api_port);
            }))
            .subscribe((res: any) => {
                if (res.success) {
                    setTimeout(() => {
                        const url = environment.url + tensorboardPort;
                        window.open(url);
                        const index = this.selectedJobsArray.indexOf(this.item.name);
                        this.selectedJobsArray.splice(index, 1);
                    }, 4000);
                }
            }, error => this.message.error(error || 'An error has occurred'));
    }

    public loadingButton() {
        return this.selectedJobsArray.includes(this.item.name);
    }

    private initializeScreenSettings() {
        this.mobile = window.innerWidth <= 1024;
    }
}
