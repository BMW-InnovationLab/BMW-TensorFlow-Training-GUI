import {Injectable} from '@angular/core';
import {HttpClient, HttpResponse} from '@angular/common/http';
import {Config} from 'codelyzer';
import {Ijob} from '../Interfaces/ijob';
import {environment} from '../../environments/environment';
import {BehaviorSubject} from 'rxjs';


@Injectable({
  providedIn: 'root'
})
export class JobsService {
  serviceUrl = environment.url;
  baseEndPoint = environment.baseEndPoint;

  jobs = new BehaviorSubject([]);
  downloadableModels = new BehaviorSubject([]);

  runningDatasetFolder = new BehaviorSubject<string>('');
  runningNetworkArchitecture = new BehaviorSubject<string>('');
  runningJobName = new BehaviorSubject<string>('');

  constructor(private http: HttpClient) {
  }

  getDownloadableModels() {
    return this.http.get<string[]>(this.serviceUrl + this.baseEndPoint + '/get_downloadable_models');

  }

  getAllJobs() {
    // return this.allJobs;
    return this.http.get<string[]>(this.serviceUrl + this.baseEndPoint + '/get_all_jobs');
  }

  getFinishedJobs() {
    return this.http.get<string[]>(this.serviceUrl + this.baseEndPoint + '/get_finished_jobs');
  }

  stopJob(jobName: Ijob) {
    return this.http.post<HttpResponse<Config>>(this.serviceUrl + this.baseEndPoint + '/stop_job', JSON.stringify(jobName));
  }

  getJobLogs(jobName: Ijob) {
    return this.http.post<string[]>(this.serviceUrl + this.baseEndPoint + '/get_logs', JSON.stringify(jobName));
  }

  monitorJob(jobName: Ijob) {
    return this.http.post<number>(this.serviceUrl + this.baseEndPoint + '/monitor_job', JSON.stringify(jobName));
  }

}
