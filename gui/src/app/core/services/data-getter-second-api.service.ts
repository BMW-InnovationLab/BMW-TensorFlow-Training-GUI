import {Injectable, ViewChild} from '@angular/core';
import {environment} from '../../../environments/environment';
import {HttpClient} from '@angular/common/http';

@Injectable({
  providedIn: 'root'
})
export class DataGetterSecondApiService {

  serviceUrl = environment.url;
  basePort = environment.baseEndPoint;

  constructor(private http: HttpClient) { }

  refreshTensorboard(apiPort) {
    return this.http.get<any>(this.serviceUrl + apiPort + '/tensorboard/refresh');
  }
}
