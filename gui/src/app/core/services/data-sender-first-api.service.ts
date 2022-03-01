import {Injectable} from '@angular/core';
import {environment} from '../../../environments/environment';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {AddJob} from '../domain/models/add-job';
import {RemoveJob} from '../domain/models/remove-job';
import {ValidateDataset} from '../domain/models/validate-dataset';
import {DatasetLabelTypes} from '../domain/models/dataset-label-types';
import {Checkpoints} from '../domain/models/checkpoints';
import {HttpHeaders} from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class DataSenderFirstApiService {
    serviceUrl = environment.url;
    basePort = environment.baseEndPoint;
    headers = new HttpHeaders().set('Content-Type', 'application/json');

    constructor(private http: HttpClient) {
    }

    addJob(json: AddJob): Observable<HttpResponse<any>> {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + this.basePort + '/jobs/start', JSON.stringify(json), {headers: this.headers});
    }

    removeJob(json: RemoveJob): Observable<HttpResponse<any>> {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + this.basePort + '/jobs/stop', JSON.stringify(json), {headers: this.headers});
    }

    logs(json: RemoveJob) {
        return this.http.post<string[]>(this.serviceUrl + this.basePort + '/jobs/container/logs', JSON.stringify(json), {headers: this.headers});
    }

    tensorboardPort(json: RemoveJob) {
        return this.http.post<AddJob>(this.serviceUrl + this.basePort + '/infrastructure/tensorboard/port', JSON.stringify(json), {headers: this.headers});
    }

    validateDataset(json: ValidateDataset) {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + this.basePort + '/dataset/validate', JSON.stringify(json), {headers: this.headers});
    }

    labelTypes(json: DatasetLabelTypes) {
        return this.http.post<string[]>(this.serviceUrl + this.basePort + '/dataset/labels/type', JSON.stringify(json), {headers: this.headers});
    }

    modelCheckPoints(json: Checkpoints) {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + this.basePort + '/models/checkpoints', JSON.stringify(json), {headers: this.headers});
    }

    removeArchivedJob(json: RemoveJob) {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + this.basePort + '/tensorboard/delete', JSON.stringify(json), {headers: this.headers});
    }

    archivedTensorboardPort(json: RemoveJob) {
        return this.http.post<number>(this.serviceUrl + this.basePort + '/infrastructure/archived/tensorboard/port', JSON.stringify(json), {headers: this.headers});
    }

    refreshTensorboard(json: RemoveJob) {
        return this.http.post<number>(this.serviceUrl + this.basePort + '/tensorboard/refresh', JSON.stringify(json), {headers: this.headers});
    }
}
