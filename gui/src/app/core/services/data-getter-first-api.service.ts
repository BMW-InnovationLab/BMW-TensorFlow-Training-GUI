import { Injectable } from '@angular/core';
import { environment } from '../../../environments/environment';
import {HttpClient} from '@angular/common/http';
import {ContainerInfo} from "../domain/models/container-info";

@Injectable({
  providedIn: 'root'
})
export class DataGetterFirstApiService {
  serviceUrl = environment.url;
  basePort = environment.baseEndPoint;

  constructor(private http: HttpClient) { }

  getDataSets() {
    return this.http.get<string[]>(this.serviceUrl + this.basePort + '/dataset/');
  }

  getAvailableGPUs() {
    return this.http.get<number[]>(this.serviceUrl + this.basePort + '/infrastructure/gpu/info');
  }

  getUsedPorts() {
    return this.http.get<string[]>(this.serviceUrl + this.basePort + '/infrastructure/used/ports');
  }

  getAvailableNetworks() {
    return this.http.get<string[]>(this.serviceUrl + this.basePort + '/models/architecture');
  }

  getDownloadableModels() {
    return this.http.get<any>(this.serviceUrl + this.basePort + '/models/downloadable');

  }

  getAllJobs() {
    return this.http.get<ContainerInfo[]>(this.serviceUrl + this.basePort + '/jobs/');
  }

  getFinishedJobs() {
    return this.http.get<string[]>(this.serviceUrl + this.basePort + '/jobs/container/finished');
  }

  getArchivedJobs() {
    return this.http.get<string[]>(this.serviceUrl + this.basePort + '/jobs/archived')
  }
}
