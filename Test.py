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

  removeBusinessSegment(index: number): void {
    if (this.rows.length > 1) {
      this.rows.splice(index, 1);
    }
  }
}


<div class="container-fluid">
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div *ngFor="let row of rows; let i = index" class="d-flex align-items-center mb-2">
        <!-- Dropdown -->
        <app-select-dropdown
          [selectText]="'Select Business Segment : '"
          [listOfValues]="businessSegments"
          [(ngModel)]="row.selectedBusinessSegment"
          style="margin-top: 1rem; height: calc(5rem);">
        </app-select-dropdown>

        <!-- Input Field -->
        <input type="text" class="form-control ml-2" 
          style="width: 250px; height: calc(2.8rem + 1px);" 
          placeholder="Type to search" 
          [(ngModel)]="row.newBusinessSegment">

        <!-- Add Button (Only for last row) -->
        <button *ngIf="i === rows.length - 1" class="btn btn-primary ml-2 btn-sm" 
          style="height: calc(2.8rem + 2px);" 
          (click)="addBusinessSegment()">Add</button>

        <!-- Remove Button (Not for first row) -->
        <button *ngIf="i > 0" class="btn btn-danger ml-2 btn-sm" 
          style="height: calc(2.8rem + 2px);" 
          (click)="removeBusinessSegment(i)">Remove</button>
      </div>
    </div>
  </div>
</div>
