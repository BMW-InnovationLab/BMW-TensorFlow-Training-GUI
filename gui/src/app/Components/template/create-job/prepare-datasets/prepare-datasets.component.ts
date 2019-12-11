import {Component, DoCheck, EventEmitter, OnChanges, OnInit, Output, SimpleChanges} from '@angular/core';
import {AbstractControl, FormControl, FormGroup, Validators} from '@angular/forms';
import {IPrepareDataSet} from '../../../../Interfaces/prepare-data-set';
import {MatSnackBar} from '@angular/material';
import {FolderGetterService} from '../../../../Services/folder-getter.service';
import {JobsService} from '../../../../Services/jobs.service';

@Component({
  selector: 'app-prepare-datasets',
  templateUrl: './prepare-datasets.component.html',
  styleUrls: ['./prepare-datasets.component.css']
})
export class PrepareDatasetsComponent implements OnInit , DoCheck {
  constructor(private snackBar: MatSnackBar, private  folderGetter: FolderGetterService) {
  }

  @Output() outputPrepareDataset = new EventEmitter<IPrepareDataSet>();
  sendRequest = false;

  labelTypes = [];

  FieldControl: FormGroup;
  prepareDatasetInterface: IPrepareDataSet = {
    datasetFolder: '',
    typeOfLabel: '',
    splitPercentage: 0.8
  };
  availableFiles: string[] = [];
  initialDatasetFolder = '';

  ngOnInit() {
    this.folderGetter.getDataSets().subscribe((availableFolders: string[]) => {
      this.availableFiles = availableFolders;
    });
    this.FieldControl = new FormGroup({
      datasetFolder: new FormControl('', [Validators.required]),
      typeOfLabel: new FormControl('', [Validators.required]),
      splitPercentage: new FormControl('0.8', [Validators.required, this.checkIfFloatValidator]),
    });
  }


  ngDoCheck(): void {
    // console.log('field control ' , this.FieldControl.value.datasetFolder );
    if ( this.initialDatasetFolder !== this.FieldControl.value.datasetFolder) {
       this.initialDatasetFolder = this.FieldControl.value.datasetFolder;
       this.sendRequest = true;
       setTimeout( () => {
         this.sendRequest = false;
       }, 160);
   }
  }



  checkIfFloatValidator(value: AbstractControl): { [Key: string]: boolean } | null {
    if (String(value.value).match(/^[0]+(\.[0-9]{1,50})?$/)) {
      return null;
    }
    return {isNotFloat: true};
  }

  // validateData() {
  //   const dataSet = this.FieldControl.get('datasetFolder').hasError('required');
  //   const typeOfLabel = this.FieldControl.get('typeOfLabel').hasError('required');
  //   // tslint:disable-next-line:max-line-length
  // tslint:disable-next-line:max-line-length
  //   const splitPercentage: boolean = this.FieldControl.get('splitPercentage').hasError('isNotFloat') || this.FieldControl.get('splitPercentage').hasError('required');
  //
  //
  //   if (!dataSet && !typeOfLabel && !splitPercentage) {
  //     this.prepareDatasetInterface.datasetFolder = this.dataSetPathField;
  //     this.prepareDatasetInterface.typeOfLabel = this.labelTypeField;
  //     this.prepareDatasetInterface.splitPercentage = this.splitPercentageField;
  //     this.outputPrepareDataset.emit(this.prepareDatasetInterface);
  //     return true;
  //   }
  //   const splitPercentageRequired: boolean = this.FieldControl.get('splitPercentage').hasError('required');
  //   if (dataSet || typeOfLabel || splitPercentageRequired) {
  //     this.openSnackBar('Please finish assigning values before continuing', true);
  //   } else {
  //     this.openSnackBar('Please enter the correct values before continuing', true);
  //   }
  //   return false;
  // }


  validateData() {
    // console.log('the field control is ');
    // console.log(this.FieldControl.value);
    //
    // console.log(this.FieldControl.valid);
    if (this.FieldControl.valid) {
      this.prepareDatasetInterface = this.FieldControl.value;
      // console.log(this.prepareDatasetInterface);
      this.outputPrepareDataset.emit(this.prepareDatasetInterface);
      return this.FieldControl.valid;
    }
    this.openSnackBar('Please enter the correct values before continuing', true);


  }

  openSnackBar(message: string, isError: boolean) {
    this.snackBar.open(message, '', {
      duration: 3000, panelClass: isError ? 'redSnackBar' : 'greenSnackBar'
    });
  }



  matTooltipOfLabel = () => {
    // tslint:disable-next-line:max-line-length
    return this.labelTypes.length === 0 ? 'Specify your labels type pascal (.xml) or json (.json), you must select a dataset before the label type'
        : 'Specify your labels type pascal (.xml) or json (.json)';
  }


}
