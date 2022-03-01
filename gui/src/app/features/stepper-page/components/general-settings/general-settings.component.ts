import {Component, Input, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {DataGetterFirstApiService} from '../../../../core/services/data-getter-first-api.service';
import {forkJoin, Observable, Observer} from 'rxjs';
import {DataSenderFirstApiService} from '../../../../core/services/data-sender-first-api.service';

import {tap} from 'rxjs/operators';
import {NzMessageService} from "ng-zorro-antd/message";

@Component({
    selector: 'app-general-settings',
    templateUrl: './general-settings.component.html',
    styleUrls: ['./general-settings.component.css']
})

export class GeneralSettingsComponent implements OnInit {
    @Input() runningJobs: Array<string> = [];
    @Input() downloadableModelsKey = [];
    public generalSettingsForm: FormGroup;
    public availableGPUs: any = [];
    public availableGPUsKeys: Array<number> = [];
    public availableGPUsValues: Array<string> = [];
    public selectedGPUs: Array<number> = [];
    public networksList: Array<string> = [];
    public checkpointsList: any;
    public containerNameDisabled = false;
    public gpusCountDisabled = false;
    public weightTypeDisabled = false;
    public networksDisabled = false;
    public checkpointsDisabled = false;
    public checked = false;

    constructor(private fb: FormBuilder,
                private dataGetterFirstApi: DataGetterFirstApiService,
                private message: NzMessageService,
                private dataSenderFirstApi: DataSenderFirstApiService) {
        this.generalSettingsForm = this.fb.group({
            name: ['', [Validators.required], [this.userNameAsyncValidator]],
            author: ['', [Validators.required]],
            gpus: [[], [Validators.required]],
            api_port: [0, [Validators.required]],
            tensorboard_port: [0, [Validators.required]],
            network_architecture: ['', [Validators.required]],
            checkPoints: [],
        });
    }

    private static getRandomPort(): string {
        return (Math.floor(Math.random() * (9999 - 1000 + 1)) + 1000).toString();
    }

    ngOnInit(): void {
        this.generalSettingsForm.controls.checkPoints.clearValidators();
        forkJoin([
            this.dataGetterFirstApi.getAvailableGPUs()
                .pipe(tap((availableGPUs) => {
                    // @ts-ignore
                    for (const key in availableGPUs) {
                        const value = availableGPUs[key];
                        this.availableGPUsKeys.push(Number(key));
                        this.availableGPUsValues.push(String(value));
                    }
                })),
            this.dataGetterFirstApi.getAvailableNetworks()
                .pipe(tap((availableNetworks: string[]) => this.networksList = availableNetworks)),
            this.dataGetterFirstApi.getUsedPorts()
                .pipe(tap((usedPorts: string[]) => {
                    let randomPort;
                    let randomTensorPort;
                    do {
                        randomPort = GeneralSettingsComponent.getRandomPort();
                        randomTensorPort = GeneralSettingsComponent.getRandomPort();
                    } while (!this.portsValid([randomPort, randomTensorPort], usedPorts));
                    this.generalSettingsForm.controls.api_port.setValue(Number(randomPort));
                    this.generalSettingsForm.controls.tensorboard_port.setValue(Number(randomTensorPort));
                }))
        ]).subscribe(() => {
        }, () => this.message.error('An error has occurred'));
    }

    private portsValid(ports: string[], usedPorts: string[]) {
        // check for duplicates:
        if (new Set(ports).size !== ports.length) {
            return false;
        }
        // check is randomly generated ports are taken
        return !ports.some(port => usedPorts.indexOf(port) >= 0);
    }

    public excludedCharacters(val) {
        this.generalSettingsForm.get('name').setAsyncValidators(this.userNameAsyncValidator);
        if (/[/\\^\[\]|`]/.test(val.key)) {
            val.preventDefault();
        }
    }

    public getCheckpoints() {
        const checkpoints = {
            network_architecture: this.generalSettingsForm.value.network_architecture
        };
        this.dataSenderFirstApi.modelCheckPoints(checkpoints)
            .subscribe(res => this.checkpointsList = res,
                (error) => this.message.error(error));
    }

    public checkPointsValidator() {
        (this.checked) ? this.generalSettingsForm.controls.checkPoints.clearValidators() :
            this.generalSettingsForm.controls.checkPoints.setValidators([Validators.required]);

    }

    public userNameAsyncValidator = (control: FormControl) =>
        new Observable((observer: Observer<ValidationErrors | null>) => {
            const modelFound = this.downloadableModelsKey.find(model => control.value === model.slice(0, -4));
            const jobFound = this.runningJobs.find(job => control.value === job);
            if (modelFound || jobFound) {
                observer.next({error: true, duplicated: true});
            } else {
                this.generalSettingsForm.get('name').clearAsyncValidators();
                observer.next(null);
            }
            observer.complete();
        })

    public submitForm(): boolean {
        for (const key in this.generalSettingsForm.controls) {
            this.generalSettingsForm.controls[key].markAsDirty();
            this.generalSettingsForm.controls[key].updateValueAndValidity();
        }
        return this.generalSettingsForm.valid;
    }

    public isNotSelected(value: number): boolean {
        return this.selectedGPUs.indexOf(value) === -1;
    }

    public disableAllInputParams() {
        this.containerNameDisabled = true;
        this.gpusCountDisabled = true;
        this.weightTypeDisabled = true;
        this.networksDisabled = true;
        this.checkpointsDisabled = true;
    }
}
