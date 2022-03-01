import {Injectable} from '@angular/core';
import {Observable, Subject} from "rxjs";

@Injectable({
    providedIn: 'root'
})
export class ArchiveDrawerActivationService {
    private isVisible = new Subject<boolean>();

    updateStatus() {
        this.isVisible.next(true);
    }

    onStatusUpdate(): Observable<any> {
        return this.isVisible.asObservable();
    }
}
