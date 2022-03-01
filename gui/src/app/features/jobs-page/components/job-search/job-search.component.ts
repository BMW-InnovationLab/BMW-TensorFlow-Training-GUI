import {Component, EventEmitter, Input, OnChanges, Output, SimpleChanges} from '@angular/core';
import {ContainerInfo} from "../../../../core/domain/models/container-info";
import {getKeywords} from "../../helpers";

@Component({
    selector: 'app-job-search',
    templateUrl: './job-search.component.html',
    styleUrls: ['./job-search.component.css']
})
export class JobSearchComponent implements OnChanges {
    @Input() jobs: Array<ContainerInfo> = [];
    @Output() searchResults: EventEmitter<ContainerInfo[]> = new EventEmitter<ContainerInfo[]>();
    public searchQuery: string;

    constructor() {
    }

    public refreshFilter(jobs: ContainerInfo[]): void {
        this.jobs = jobs;
    }

    ngOnChanges(changes: SimpleChanges): void {
        this.search();
    }

    public search() {
        if (this.searchQuery == '' || !this.searchQuery) {
            const res = this.jobs;
            this.searchResults.emit(res);
            return res;
        }
        let searchQuery = this.searchQuery.trim();
        const keywords = getKeywords(searchQuery);
        const nameMatches = this.jobs
            .filter(job => {
                for (let keyword of keywords) {
                    if (job.name.toLowerCase().includes(keyword) ||
                        job.model.toLowerCase().includes(keyword) ||
                        job.dataset.toLowerCase().includes(keyword) ||
                        job.author.toLowerCase().includes(keyword)) {
                        return true;
                    }
                }
                return false;
            });
        this.searchResults.emit(nameMatches);
        return nameMatches;
    }
}
