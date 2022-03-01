import {Component, OnDestroy, OnInit, ViewChild} from '@angular/core';
import {PrepareDatasetComponent} from './components/prepare-dataset/prepare-dataset.component';
import {GeneralSettingsComponent} from './components/general-settings/general-settings.component';
import {HyperParametersComponent} from './components/hyper-parameters/hyper-parameters.component';
import {DataGetterFirstApiService} from '../../core/services/data-getter-first-api.service';
import {AddJob} from '../../core/domain/models/add-job';
import {DataSenderFirstApiService} from '../../core/services/data-sender-first-api.service';
import {RemoveJob} from '../../core/domain/models/remove-job';
import {BasicConfig} from '../../core/domain/models/basic-config';
import {DataSenderSecondApiService} from '../../core/services/data-sender-second-api.service';
import {
    AdvancedHyperParametersComponent
} from './components/advanced-hyper-parameters/advanced-hyper-parameters.component';
import {NzMessageService} from 'ng-zorro-antd/message';
import {Router} from '@angular/router';
import {ValidateDataset} from '../../core/domain/models/validate-dataset';
import {DataPreparation} from '../../core/domain/models/data-preparation';
import {ConfigContent} from '../../core/domain/models/config-content';
import {ContentAdvanced} from '../../core/domain/models/content-advanced';
import {forkJoin, of} from 'rxjs';
import {concatMap, tap} from 'rxjs/operators';
import {HeaderTitle} from '../../core/domain/enums/header-title';
import {retryWithDelay} from 'rxjs-boost/lib/operators';
import {ContainerInfo} from "../../core/domain/models/container-info";

@Component({
    selector: 'app-stepper-page',
    templateUrl: './stepper-page.component.html',
    styleUrls: ['./stepper-page.component.css']
})
export class StepperPageComponent implements OnInit, OnDestroy {
    @ViewChild(PrepareDatasetComponent) prepareDataset: PrepareDatasetComponent;
    @ViewChild(GeneralSettingsComponent) generalSettings: GeneralSettingsComponent;
    @ViewChild(HyperParametersComponent) hyperParameters: HyperParametersComponent;
    @ViewChild(AdvancedHyperParametersComponent) advancedHyperParameters: AdvancedHyperParametersComponent;
    public readonly title = HeaderTitle.CREATE;
    public current = 0;
    public step2PreviousButtonDisabled: boolean;
    public step2NextButtonLoading: boolean;
    public doneButtonLoading: boolean;
    public cancelButtonDisabled: boolean;
    public switchState: boolean;
    public allowMemoryGrowth = false;
    public hyperParametersHidden = false;
    public advancedHyperParametersHidden = true;
    public allJobs: Array<ContainerInfo> = [];
    public finishedJobs: Array<string> = [];
    public downloadableModels: any;
    public mobile: boolean;
    public isCPU: boolean;
    numberOfClasses: number;
    configContent: ConfigContent = {
        network_architecture: '',
        model_name: ''
    };
    contentAdvanced: ContentAdvanced = {
        content: ''
    };
    private readonly TIMEOUT = 35000;
    private interval;
    private basicConfig: BasicConfig = {
        num_classes: null,
        batch_size: null,
        learning_rate: null,
        checkpoint_name: null,
        width: null,
        height: null,
        network_architecture: null,
        training_steps: null,
        eval_steps: null,
        name: null,
        allow_growth: null
    };

    constructor(private dataGetterFirstApi: DataGetterFirstApiService,
                private dataSenderFirstApi: DataSenderFirstApiService,
                private dataSenderSecondApi: DataSenderSecondApiService,
                private message: NzMessageService,
                private router: Router) {
    }

    ngOnInit() {
        this.mobile = window.screen.width < 769;
        window.onresize = () => {
            this.mobile = window.screen.width < 769;
        };
        this.getJobs();
        this.initPage();
    }

    ngOnDestroy() {
        clearInterval(this.interval);
    }

    private initPage() {
        return forkJoin([
            this.dataGetterFirstApi.getFinishedJobs()
                .pipe(tap((finishedJobs: string[]) => this.finishedJobs = finishedJobs)),
            this.dataGetterFirstApi.getDownloadableModels()
                .pipe(tap((models) => this.downloadableModels = models))
        ]).subscribe(() => {
        }, (error) => this.message.error(error));
    }

    private getJobs(): void {
        this.dataGetterFirstApi.getAllJobs()
            .subscribe((allJobs: ContainerInfo[]) => this.allJobs = allJobs,
                (error) => this.message.error(error));
    }

    private changeContent(): void {
        this.step2NextButtonLoading = false;
        this.step2PreviousButtonDisabled = this.current === 2;
    }

    public cancel(): void {
        const removeJob: RemoveJob = {
            name: this.generalSettings.generalSettingsForm.value.name
        };
        this.dataSenderFirstApi.removeJob(removeJob)
            .subscribe(() => {
            }, (error) => this.message.error(error));
    }

    public pre(): void {
        this.current -= 1;
        this.changeContent();
    }

    private validateDataset() {
        const datasetValidation: ValidateDataset = {
            dataset_path: this.prepareDataset.prepareDatasetForm.value.dataset_name,
            labels_type: this.prepareDataset.prepareDatasetForm.value.dataset_label_type
        };
        this.dataSenderFirstApi.validateDataset(datasetValidation)
            .subscribe((res: any) => {
                if (!res.success) {
                    this.message.error('Dataset Invalid!', {
                        nzDuration: 3000
                    });
                } else {
                    this.current += 1;
                    this.changeContent();
                }
            }, (error) => this.message.error(error));
    }

    private setHyperParameters(res) {
        this.hyperParameters.hyperParameterForm.controls.learning_rate.setValue(res.learning_rate);
        this.hyperParameters.hyperParameterForm.controls.batch_size.setValue(res.batch_size);
        this.hyperParameters.hyperParameterForm.controls.numberOfClasses.setValue(res.num_classes);
        this.hyperParameters.hyperParameterForm.controls.trainingSteps.setValue(res.training_steps);
        this.hyperParameters.hyperParameterForm.controls.evalSteps.setValue(res.eval_steps);
        this.advancedHyperParameters.advancedHyperParametersForm.controls
            .trainingSteps.setValue(res.training_steps);
        this.advancedHyperParameters.advancedHyperParametersForm
            .controls.evalSteps.setValue(res.eval_steps);
        this.numberOfClasses = res.num_classes;
    }

    private beginJob() {
        const newJob: AddJob = {
            name: this.generalSettings.generalSettingsForm.value.name,
            author: this.generalSettings.generalSettingsForm.value.author,
            gpus: this.generalSettings.generalSettingsForm.value.gpus,
            api_port: this.generalSettings.generalSettingsForm.value.api_port,
            tensorboard_port: this.generalSettings.generalSettingsForm.value.tensorboard_port,
            network_architecture: this.generalSettings.generalSettingsForm.value.network_architecture,
            dataset_path: this.prepareDataset.prepareDatasetForm.value.dataset_name
        };

        if (this.generalSettings.generalSettingsForm.value.gpus.includes(-1)) {
            this.isCPU = true;
        } else {
            this.isCPU = false;
        }

        this.configContent.network_architecture = this.generalSettings.generalSettingsForm.value.network_architecture;
        this.configContent.model_name = this.generalSettings.generalSettingsForm.value.name;
        this.generalSettings.disableAllInputParams();
        this.step2PreviousButtonDisabled = true;
        this.step2NextButtonLoading = true;

        this.dataSenderFirstApi.addJob(newJob)
            .pipe(concatMap((message: any) => {
                if (message.success) {
                    return this.dataSenderSecondApi
                        .configurationDefault(this.configContent, this.generalSettings.generalSettingsForm.value.api_port)
                        .pipe(tap(res => this.setHyperParameters(res)), retryWithDelay(5000, 5));
                }
                return of(null);
            }))
            // .pipe(concatMap(_ => of('_').pipe(delay(5000))))
            .pipe(concatMap(_ => {
                return this.dataSenderSecondApi
                    .configurationContent(this.configContent, this.generalSettings.generalSettingsForm.value.api_port)
                    .pipe(tap((res: string) => {
                        this.advancedHyperParameters.advancedHyperParametersForm.controls.configContent
                            .setValue(res.substring(0, res.length).split(/\n/g).join('\n'));
                    }));
            }))
            .subscribe(() => {
                if (this.generalSettings.generalSettingsForm.value.gpus.length === 2) {
                    this.hyperParameters.hyperParameterForm.get('batch_size').setAsyncValidators(
                        [this.hyperParameters.checkIfIntValidator, this.hyperParameters.checkIfDivisibleByTwoValidator]
                    );
                }
                this.current += 1;
                this.changeContent();
                this.cancelButtonDisabled = false;
                this.doneButtonLoading = false;
                this.getJobs();
            }, (error) => {
                this.message.error(error);
                this.dataSenderFirstApi.removeJob({name: newJob.name}).subscribe();
                this.router.navigate(['/jobs']);
            });
    }

    next(): void {
        if (this.current === 0) {
            if (this.prepareDataset.submitForm()) {
                this.validateDataset();
            }
        } else if (this.current === 1) {
            if (this.generalSettings.submitForm()) {
                this.beginJob();
            }
        }
    }

    done(): void {
        const dataPreparation: DataPreparation = {
            labels_type: this.prepareDataset.prepareDatasetForm.value.dataset_label_type,
            split_percentage: this.prepareDataset.prepareDatasetForm.value.training / 100
        };
        this.basicConfig.learning_rate = this.hyperParameters.hyperParameterForm.value.learning_rate;
        this.basicConfig.batch_size = this.hyperParameters.hyperParameterForm.value.batch_size;
        this.basicConfig.num_classes = this.numberOfClasses;
        this.basicConfig.network_architecture = this.generalSettings.generalSettingsForm.value.network_architecture;
        this.basicConfig.training_steps = this.hyperParameters.hyperParameterForm.value.trainingSteps;
        this.basicConfig.eval_steps = this.hyperParameters.hyperParameterForm.value.evalSteps;
        this.basicConfig.name = this.generalSettings.generalSettingsForm.value.name;
        this.basicConfig.network_architecture = this.generalSettings.generalSettingsForm.value.network_architecture;

        if (this.generalSettings.checked) {
            this.basicConfig.checkpoint_name = this.generalSettings.generalSettingsForm.value.checkPoints;
        }

        if (this.generalSettings.generalSettingsForm.value.gpus.includes(-1)) {
            this.basicConfig.allow_growth = false;
        } else {
            this.basicConfig.allow_growth = this.allowMemoryGrowth;
        }

        const advancedConfig: BasicConfig = {
            allow_growth: this.basicConfig.allow_growth,
            batch_size: null,
            checkpoint_name: null,
            eval_steps: this.advancedHyperParameters.advancedHyperParametersForm.value.evalSteps,
            height: null,
            learning_rate: null,
            name: this.basicConfig.name,
            network_architecture: this.basicConfig.network_architecture,
            num_classes: null,
            width: null,
            training_steps: Number(this.advancedHyperParameters.advancedHyperParametersForm.value.trainingSteps)
        };

        if (this.advancedHyperParameters.submitForm() && this.hyperParametersHidden === true) {
            const content: Array<string[]> = this.advancedHyperParameters.advancedHyperParametersForm.value.configContent.substring(0,
                this.advancedHyperParameters.advancedHyperParametersForm.value.configContent.length.length).split(/\n/g);
            this.contentAdvanced.content = content.join('\\n').replace(/["]+/g, '\\"');
            this.doneButtonLoading = true;
            this.dataSenderSecondApi.datasetPost(dataPreparation, this.generalSettings.generalSettingsForm.value.api_port)
                .pipe(concatMap((datasetMessage: any) => {
                    if (datasetMessage.success) {
                        return this.dataSenderSecondApi
                            .advancedConfigPost(this.contentAdvanced, this.generalSettings.generalSettingsForm.value.api_port);
                    }
                    return of(null);
                }))
                .pipe(concatMap((configMessage: any) => {
                    if (configMessage.success) {
                        return this.dataSenderSecondApi
                            .startTraining(advancedConfig, this.generalSettings.generalSettingsForm.value.api_port);
                    }
                    this.message.error('Configuration Content Is Invalid!', {
                        nzDuration: 3000
                    });
                    return of(null);
                }))
                .subscribe(() => {
                    this.doneButtonLoading = false;
                    this.current += 1;
                    this.changeContent();
                    this.router.navigate(['/jobs']);
                }, (error) => this.message.error(error));
        } else {
            if (this.hyperParameters.submitForm()) {
                this.doneButtonLoading = true;
                this.dataSenderSecondApi.datasetPost(dataPreparation, this.generalSettings.generalSettingsForm.value.api_port)
                    .pipe(concatMap(() => this.dataSenderSecondApi
                        .basicConfigPost(this.basicConfig, this.generalSettings.generalSettingsForm.value.api_port)))
                    .pipe(concatMap(() => this.dataSenderSecondApi
                        .startTraining(this.basicConfig, this.generalSettings.generalSettingsForm.value.api_port)))
                    .subscribe(() => {
                        this.doneButtonLoading = false;
                        this.current += 1;
                        this.changeContent();
                        this.router.navigate(['/jobs']);
                    }, (error) => this.message.error(error));
            }
        }
    }

    // switch between hyper and advanced hyper parameters
    public switch() {
        this.switchState = !this.switchState;
        this.hyperParametersHidden = this.switchState;
        this.advancedHyperParametersHidden = !this.switchState;
    }

    public getDownloadableModels() {
        return (this.downloadableModels !== null && this.downloadableModels !== undefined) ? Object.keys(this.downloadableModels) : [];
    }
}
