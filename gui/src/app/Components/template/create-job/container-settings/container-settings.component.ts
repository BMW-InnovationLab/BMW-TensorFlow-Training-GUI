import {Component, EventEmitter, OnInit, Output, ViewChild} from '@angular/core';
import {AbstractControl, FormBuilder, FormControl, FormGroup, Validators} from '@angular/forms';
import {MatSnackBar} from '@angular/material';
import {IgeneralSettings} from '../../../../Interfaces/Igeneral-settings';
import {Input} from '@angular/core';
import {DataGetter} from '../../../../Services/data-getter.service';
import {DataValidatorService} from '../../../../Services/data-validator.service';
import {JobsService} from '../../../../Services/jobs.service';

@Component({
  selector: 'app-container-settings',
  templateUrl: './container-settings.component.html',
  styleUrls: ['./container-settings.component.css']
})
export class ContainerSettingsComponent implements OnInit {
  @Input() GPUsList: number[];
  @Output() outputContainerSettings = new EventEmitter<IgeneralSettings>();
  checkPointRequired = false;
  networksList = [''];
  FieldControl: FormGroup;
  checkPoints: string[];
  checkBoxDisabled = true;
  jobList: string[] = [];
  checkbox = false;
  generalSettings: IgeneralSettings = {
    containerName: '',
    networkArchitecture: '',
    gPUs: [],
    tensorBoard: 0,
    APIPort: 0
  };
  usedPorts: Array<string> = [];
  tooltipText = 'Network Architecture need to be selected to enable this option';

  constructor(private fb: FormBuilder,
              private snackBar: MatSnackBar,
              private getterService: DataGetter,
              private validatorService: DataValidatorService,
              private jobService: JobsService) {
  }

  ngOnInit() {
    // console.log(this.checkbox);
    this.jobService.getAllJobs().subscribe((value: string[]) => {
      this.jobList = value;
      this.jobService.getDownloadableModels().subscribe(value2 => {
        for ( let model of value2) {
          model = this.getNameOfModel(model);
          this.jobList.push(model);
        }
      }, error => this.openSnackBar('API Down' , true));
    }, error => this.openSnackBar('API Down ', true));


    this.FieldControl = new FormGroup({
      // tslint:disable-next-line:max-line-length
      tensorBoard: new FormControl(Number(this.functionToGetRandomNumber(this.usedPorts)), [Validators.required, this.checkIfNumberValidator, this.checkIfInRange , this.checkIfUsedPort.bind(this), this.checkIfSamePort.bind(this)]),
      // tslint:disable-next-line:max-line-length
      APIPort: new FormControl(Number(this.functionToGetRandomNumber(this.usedPorts)), [Validators.required, this.checkIfNumberValidator, this.checkIfInRange , this.checkIfUsedPort.bind(this), this.checkIfSamePort.bind(this)]),
      containerName: new FormControl('', [Validators.required, this.checkIfNameExists.bind(this)]),
      networkArchitecture: new FormControl('', [Validators.required]),
      gPUs: new FormControl('', [Validators.required]),
      checkPoints: new FormControl('', [Validators.required])
    });

    this.getUsedPorts();

  }

  checkIfNumberValidator(value: AbstractControl): { [Key: string]: boolean } | null {
    if (String(value.value).match(/^[0-9]+$/)) {
      return null;
    }
    return {isNotInteger: true};
  }

  checkIfInRange(value: AbstractControl): { [Key: string]: boolean } | null {
    if (Number(value.value) > 1024 && Number(value.value) <= 65535 ) {
      return null;
    }
    return {isNotInRange: true};
  }


  checkIfSamePort(): { [Key: string]: boolean } | null {
    if (this.FieldControl) {
      const apiPortValue = this.FieldControl.get('APIPort').value;
      const tensorboardPortValue = this.FieldControl.get('tensorBoard').value;
      return (tensorboardPortValue && apiPortValue && (apiPortValue === tensorboardPortValue)) ? {duplicatePort: true} : null;
    }
    return null;
  }

  checkIfUsedPort(value: AbstractControl): { [Key: string]: boolean } | null {
    if (this.usedPorts.includes(value.value.toString())) {
      return {alreadyAllocatedPort: true};
    }
    return null;
  }

  getUsedPorts() {
    this.getterService.getUsedPorts().subscribe((response) => {
      this.usedPorts = response;
      console.log(this.usedPorts);

      this.FieldControl.value.APIPort = Number(this.functionToGetRandomNumber(this.usedPorts));
      this.FieldControl.value.tensorBoard = Number(this.functionToGetRandomNumber(this.usedPorts));

    });
  }

  functionToGetRandomNumber(tab: string[]) {
    const x = this.generateRandomValue().toString();
    if ( this.checkNumberIfInArray(x , tab) === false) {
      return x;
    }
    return this.functionToGetRandomNumber(tab);
  }

  generateRandomValue() {
    const min = 1025;
    const max = 10000;
    return (Math.floor(Math.random() * (max - min)) + min).toString();
  }

  checkNumberIfInArray(value: string , tab: string[]) {
    for ( const key of tab ) {
      if ( key === value ) {
        return true;
      }
    }
    return false;
  }


  checkIfNameExists(value: AbstractControl): { [Key: string]: boolean } | null {
    if (this.jobList.includes(value.value)) {
      return {alreadyExists: true};
    }
    return null;
  }

  networkArchitectureChanged() {
    console.log(this.checkbox);
    this.tooltipText = this.FieldControl.controls.networkArchitecture.value !== 'frcnn_resnet_101' ?
    'Network Architecture need to be selected to enable this option' : 'Custom Checkpoint not available for frcnn_resnet_101';
    this.checkPoints = null;
    this.checkBoxDisable();
    this.checkbox = false;
    if (this.FieldControl.get('networkArchitecture').value === 'frcnn_resnet_101') {
      this.checkBoxDisabled = true;
    }
  }

  checkBoxDisable() {
    if (this.FieldControl.get('networkArchitecture').value !== '') {
      this.checkBoxDisabled = false;
      if (this.FieldControl.get('networkArchitecture').value === 'frcnn_resnet_101') {
        this.checkBoxDisabled = true;
      }
    }
  }

  checkBoxClicked() {
    this.checkbox = !this.checkbox;
    this.FieldControl.get('checkPoints').setValue('');
    this.checkPointRequired = !this.checkPointRequired;
    this.checkPoints = [];
    if (this.checkbox) {
      this.getterService.getAvailableCheckPoints(this.FieldControl.get('networkArchitecture').value).subscribe((checkPoints: string[]) => {
        this.checkPoints = checkPoints;
      }, error => this.openSnackBar('Sorry but we couldn\'t find you any CheckPoints', true));
    }
  }

  validateData() {
    if (this.checkPointRequired) {
      this.validatorService.setCheckPointAvailable(true);
    } else {
      this.FieldControl.get('checkPoints').setErrors(null);
    }
    if (this.FieldControl.valid) {
      console.log('I AM HERER');
      this.generalSettings = Object.assign({}, this.FieldControl.value);
      this.outputContainerSettings.emit(this.generalSettings);
      console.log('GENERAL SETTINGS', this.generalSettings);
    }

    console.log('VALID', this.FieldControl.valid);
    return this.FieldControl.valid;
  }

  openSnackBar(message: string, isError: boolean) {
    this.snackBar.open(message, '', {
      duration: 3000, panelClass: isError ? 'redSnackBar' : 'greenSnackBar'
    });
  }



  getNameOfModel(model: string) {
    const arr = model.split('-');
    let name = '';
    for ( let i = 0 ; i < arr.length - 1 ; i++) {
      if ( i === arr.length - 2 ) {
        name = name + arr[i];
      } else {
        name = name + arr[i] + '-';
      }
    }
    if ( arr.length === 1 ) {
      name = model;
    }

    return name;
  }


}
