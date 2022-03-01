import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormGroup, Validators} from '@angular/forms';
import {DataGetterFirstApiService} from '../../../../core/services/data-getter-first-api.service';
import {DataSenderFirstApiService} from '../../../../core/services/data-sender-first-api.service';
import {DatasetLabelTypes} from '../../../../core/domain/models/dataset-label-types';
import {NzMessageService} from "ng-zorro-antd/message";

@Component({
    selector: 'app-prepare-dataset',
    templateUrl: './prepare-dataset.component.html',
    styleUrls: ['./prepare-dataset.component.css']
})
export class PrepareDatasetComponent implements OnInit {
    public prepareDatasetForm: FormGroup;
    public availableFiles: string[] = [];
    public labelTypes: string[] = [];

    constructor(private fb: FormBuilder,
                private dataGetterFirstApi: DataGetterFirstApiService,
                private message: NzMessageService,
                private dataSenderFirstApiService: DataSenderFirstApiService) {
        this.prepareDatasetForm = this.fb.group({
            dataset_name: ['', [Validators.required]],
            dataset_label_type: ['', [Validators.required]],
            training: [80, [Validators.required]],
            testing: [20, [Validators.required]]
        });
    }

    ngOnInit(): void {
        this.dataGetterFirstApi.getDataSets().subscribe((availableFolders: string[]) => {
            availableFolders.sort();
            this.availableFiles = availableFolders;
        }, error => this.message.error(error));
    }

    parserPercent = (value: string) => value.replace(/[.]\d*/, '');

    public submitForm(): boolean {
        for (const key in this.prepareDatasetForm.controls) {
            this.prepareDatasetForm.controls[key].markAsDirty();
            this.prepareDatasetForm.controls[key].updateValueAndValidity();
        }
        return this.prepareDatasetForm.valid;
    }

    public changeTesting() {
        this.prepareDatasetForm.controls.testing.setValue(100 - this.prepareDatasetForm.value.training);
    }

    onDatasetFolderSelection() {
        const datasetLabelTypes: DatasetLabelTypes = {
            dataset_name: this.prepareDatasetForm.value.dataset_name
        };
        this.dataSenderFirstApiService.labelTypes(datasetLabelTypes).subscribe(res => {
            this.labelTypes = res;
        }, error => this.message.error(error));
    }
}
