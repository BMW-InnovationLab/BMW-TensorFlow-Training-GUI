import {Component} from '@angular/core';
import {FormBuilder, FormControl, FormGroup, ValidationErrors, Validators} from '@angular/forms';
import {Observable, Observer} from 'rxjs';

@Component({
    selector: 'app-advanced-hyper-parameters',
    templateUrl: './advanced-hyper-parameters.component.html',
    styleUrls: ['./advanced-hyper-parameters.component.css']
})
export class AdvancedHyperParametersComponent {
    public advancedHyperParametersForm: FormGroup;

    constructor(private fb: FormBuilder) {
        this.advancedHyperParametersForm = this.fb.group({
            configContent: [[], [Validators.required]],
            trainingSteps: [1000, [Validators.required], [this.checkIfIntValidator]],
            evalSteps: [1, [Validators.required], [this.checkIfIntValidator]],
        });
    }

    public checkIfIntValidator = (control: FormControl) =>
        new Observable((observer: Observer<ValidationErrors | null>) => {
            if (!String(control.value).match(/^[0-9]+$/)) {
                observer.next({error: true, notInt: true});
            } else {
                observer.next(null);
            }
            observer.complete();
        })

    public submitForm(): boolean {
        for (const key in this.advancedHyperParametersForm.controls) {
            this.advancedHyperParametersForm.controls[key].markAsDirty();
            this.advancedHyperParametersForm.controls[key].updateValueAndValidity();
        }
        return this.advancedHyperParametersForm.valid;
    }
}
