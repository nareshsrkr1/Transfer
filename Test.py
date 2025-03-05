export class DynamicSegmentationComponent implements OnInit {
  businessSegments: string[] = [];
  overRides: string[] = [];
  rows: { selectedBusinessSegment: string; newBusinessSegment: string }[] = [];

  constructor(private executionService: ExecutionService) {}

  ngOnInit(): void {
    this.fetchBusinessSegments();
    this.fetchOverRides();
    this.addBusinessSegment(); // Add the first row initially
  }

  fetchBusinessSegments(): void {
    this.executionService.fetchBusinessSegments().subscribe(
      (data) => {
        this.businessSegments = data;
      },
      (error) => console.error('Error fetching business segments', error)
    );
  }

  fetchOverRides(): void {
    // Fetch overrides if needed
  }

  addBusinessSegment(): void {
    this.rows.push({ selectedBusinessSegment: '', newBusinessSegment: '' });
  }
}

<div class="container-fluid row d-flex justify-content-center">
  <div *ngFor="let row of rows; let i = index" class="d-flex align-items-center">
    <app-select-dropdown
      [selectText]="'Select Business Segment : '"
      [listOfValues]="businessSegments"
      [(ngModel)]="row.selectedBusinessSegment"
      style="margin-top: 1rem; height: calc(5rem);">
    </app-select-dropdown>

    <input type="text" class="form-control ml-2" 
      style="width: 250px; height: calc(2.8rem + 1px);" 
      placeholder="Type to search" 
      [(ngModel)]="row.newBusinessSegment">

    <button class="btn btn-primary ml-2 btn-sm" 
      style="height: calc(2.8rem + 2px);" 
      (click)="addBusinessSegment()">Add</button>
  </div>
</div>
