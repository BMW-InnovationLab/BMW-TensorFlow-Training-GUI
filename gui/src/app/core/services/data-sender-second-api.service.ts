import {Injectable} from '@angular/core';
import {environment} from '../../../environments/environment';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Observable} from 'rxjs';
import {DataPreparation} from '../domain/models/data-preparation';
import {ConfigContent} from '../domain/models/config-content';
import {ContentAdvanced} from '../domain/models/content-advanced';
import { HttpHeaders } from '@angular/common/http';

@Injectable({
    providedIn: 'root'
})
export class DataSenderSecondApiService {

    serviceUrl = environment.url;

    constructor(private http: HttpClient) {
    }
    headers = new HttpHeaders().set('Content-Type','application/json');


    basicConfigPost(json, apiPort: number): Observable<HttpResponse<any>> {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + apiPort + '/configuration/', json,{headers:this.headers});
    }

    startTraining(json, apiPort: number): Observable<HttpResponse<any>> {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + apiPort + '/training/eval/', json,{headers:this.headers});
    }

    advancedConfigPost(json: ContentAdvanced, apiPort: number): Observable<HttpResponse<any>> {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + apiPort + '/configuration/advanced', json,{headers:this.headers});
    }

    datasetPost(json: DataPreparation, apiPort: number): Observable<HttpResponse<any>> {
        return this.http.post<HttpResponse<any>>(this.serviceUrl + apiPort + '/data_preparation/', json,{headers:this.headers});
    }

    configurationContent(json: ConfigContent, apiPort: number): Observable<string> {
        return this.http.post<string>(this.serviceUrl + apiPort + '/configuration/content', json,{headers:this.headers});
    }

    configurationDefault(json: ConfigContent, apiPort: number): Observable<any> {
        return this.http.post<JSON>(this.serviceUrl + apiPort + '/configuration/default', json,{headers:this.headers});
    }
}
