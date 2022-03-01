import {Component, OnInit} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {Observable, Observer} from 'rxjs';

@Component({
    selector: 'app-hyper-parameters',
    templateUrl: './hyper-parameters.component.html',
    styleUrls: ['./hyper-parameters.component.css']
})
export class HyperParametersComponent implements OnInit {
    public hyperParameterForm: FormGroup;

    constructor(private fb: FormBuilder) {
        this.hyperParameterForm = this.fb.group({
            learning_rate: [0.01, [Validators.required], [this.checkIfFloatValidator]],
            batch_size: [1, [Validators.required], [this.checkIfIntValidator]],
            numberOfClasses: [1, [Validators.required], [this.checkIfIntValidator]],
            trainingSteps: [1000, [Validators.required], [this.checkIfIntValidator]],
            evalSteps: [1, [Validators.required], [this.checkIfIntValidator]],
        });
    }

    ngOnInit(): void {
        this.hyperParameterForm.controls.numberOfClasses.disable();
    }

    public checkIfFloatValidator = (control: FormControl) =>
        new Observable((observer: Observer<ValidationErrors | null>) => {
            if (!String(control.value).match(/^[0]+(\.[0-9]{1,50})?$/)) {
                observer.next({error: true, notFloat: true});
            } else {
                observer.next(null);
            }
            observer.complete();
        })

    public checkIfIntValidator = (control: FormControl) =>
        new Observable((observer: Observer<ValidationErrors | null>) => {
            if (!String(control.value).match(/^[0-9]+$/)) {
                observer.next({error: true, notInt: true});
            } else {
                observer.next(null);
            }
            observer.complete();
        })

    public checkIfDivisibleByTwoValidator = (control: FormControl) =>
        new Observable((observer: Observer<ValidationErrors | null>) => {
            if (!String(control.value).match(/^\d*[02468]$/)) {
                observer.next({error: true, notEven: true});
            } else {
                observer.next(null);
            }
            observer.complete();
        })

    public submitForm(): boolean {
        for (const key in this.hyperParameterForm.controls) {
            this.hyperParameterForm.controls[key].markAsDirty();
            this.hyperParameterForm.controls[key].updateValueAndValidity();
        }
        return this.hyperParameterForm.valid;
    }

}
