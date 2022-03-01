import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {DataGetterFirstApiService} from '../../core/services/data-getter-first-api.service';
import {DataSenderFirstApiService} from '../../core/services/data-sender-first-api.service';
import {DataGetterSecondApiService} from '../../core/services/data-getter-second-api.service';
import {NzMessageService} from 'ng-zorro-antd/message';
import {forkJoin, fromEvent, Observable, Subscription} from 'rxjs';
import {tap} from 'rxjs/operators';
import {HeaderTitle} from '../../core/domain/enums/header-title';
import {ContainerInfo} from "../../core/domain/models/container-info";
import {ArchiveDrawerActivationService} from "../../core/services/archive-drawer-activation.service";
import {JobSearchComponent} from "./components/job-search/job-search.component";

@Component({
    selector: 'app-jobs-page',
    templateUrl: './jobs-page.component.html',
    styleUrls: ['./jobs-page.component.css']
})
export class JobsPageComponent implements OnInit, OnDestroy {
    @ViewChild(JobSearchComponent, {static: false}) searchComponent: JobSearchComponent;

    public readonly title: HeaderTitle = HeaderTitle.DISPLAY;
    public readonly numberOfJobsPerPage = 4;
    public pageIndex = 1;
    public downloadableModels: any;
    public allJobs: Array<ContainerInfo> = [];
    public displayList: Array<ContainerInfo> = [];
    public searchList: Array<ContainerInfo> = [];
    public finishedJobs: Array<string> = [];
    public archivedJobs: Array<string> = [];
    public logsModalSettings = {
        isVisible: false,
        specificLogsJobTitle: ''
    };
    public logs: Array<string> = [];
    public mobile: boolean;
    public windowHeight: boolean;
    public archiveDrawerIsVisible: boolean;
    public tensorboardArchivesSubscription: Subscription;
    private interval;
    private resizeObservable: Observable<Event>
    private resizeSubscription: Subscription

    constructor(private dataGetterFirstApi: DataGetterFirstApiService,
                private dataSenderFirstApi: DataSenderFirstApiService,
                private dataGetterSecondApi: DataGetterSecondApiService,
                private message: NzMessageService,
                private archiveDrawerActivation: ArchiveDrawerActivationService) {

    }

    ngOnInit(): void {
        this.initializeScreenSettings();
        this.resizeObservable = fromEvent(window, 'resize');
        this.resizeSubscription = this.resizeObservable.subscribe(() => {
            this.initializeScreenSettings()
        });

        this.dataGetterFirstApi.getAllJobs()
            .subscribe((allJobs) => {
                this.allJobs = allJobs;
                this.updatePage();
            }, (error) => {
                this.message.error(error);
            });

        this.tensorboardArchivesSubscription = this.archiveDrawerActivation.onStatusUpdate().subscribe(status => {
            this.archiveDrawerIsVisible = status;
        });

        this.initPage();
        this.interval = setInterval(this.initPage, 5000);
    }

    ngOnDestroy() {
        clearInterval(this.interval);
        this.tensorboardArchivesSubscription.unsubscribe();
        this.resizeSubscription.unsubscribe()
    }

    public page($event) {
        this.pageIndex = $event;
        this.updatePage();
    }

    public logsButton(jobs: string) {
        this.logsModalSettings.specificLogsJobTitle = jobs;
        this.dataSenderFirstApi.logs({name: jobs})
            .subscribe((logs) => {
                this.logs = logs;
            }, error => {
                this.message.error(error);
                this.logsModalSettings.isVisible = false;
            });
        this.logsModalSettings.isVisible = true;
    }

    public onJobRemove(jobs: string) {
        let jobToRemove: ContainerInfo = this.allJobs.find(job => job.name == jobs)
        const indexToRemove = this.allJobs.indexOf(jobToRemove);
        this.allJobs.splice(indexToRemove, 1);
        this.updatePage();
        this.dataSenderFirstApi.removeJob({name: jobs})
            .subscribe(() => {
            }, (error) => {
                this.allJobs.unshift(jobToRemove);
                this.updatePage();
                this.message.error(error);
            });
    }

    public handleRefreshMiddle(): void {
        this.dataSenderFirstApi.logs({name: this.logsModalSettings.specificLogsJobTitle})
            .subscribe((logs) => this.logs = logs,
                (error) => this.message.error(error));
    }

    closeArchiveDrawer(): void {
        this.archiveDrawerIsVisible = false;
    }

    onArchivedJobRemove(jobToRemove: string) {
        const indexToRemove = this.archivedJobs.indexOf(jobToRemove);
        this.archivedJobs.splice(indexToRemove, 1);
        this.dataSenderFirstApi.removeArchivedJob({name: jobToRemove})
            .subscribe(() => {
            }, (error) => {
                this.archivedJobs.unshift(jobToRemove)
                this.message.error(error);
            });
    }

    private initializeScreenSettings() {
        this.mobile = window.innerWidth <= 1024;
        this.windowHeight = window.innerHeight < 710;
    }

    private initPage = () => {
        return forkJoin([
            this.dataGetterFirstApi.getFinishedJobs()
                .pipe(tap((finishedJobs: string[]) => this.finishedJobs = finishedJobs)),
            this.dataGetterFirstApi.getDownloadableModels()
                .pipe(tap((models) => this.downloadableModels = models)),
            this.dataGetterFirstApi.getArchivedJobs()
                .pipe(tap((archivedJobs: string[]) => this.archivedJobs = archivedJobs))
        ]).subscribe(() => this.updatePage(),
            (error) => {
                this.message.error(error);
            });
    }

    private updatePage() {
        this.searchComponent?.refreshFilter(this.allJobs);
        this.paginate();
    }

    showFiltered($event: ContainerInfo[]) {
        this.searchList = $event;
        this.paginate();
    }

    private paginate() {
        this.displayList = [...this.searchList].splice
        ((this.pageIndex - 1) * this.numberOfJobsPerPage, this.numberOfJobsPerPage);
    }
}
