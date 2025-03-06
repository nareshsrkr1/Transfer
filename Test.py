<div class="container-fluid">
  <div class="row d-flex justify-content-center" *ngFor="let row of rows; let i = index">
    <!-- Condition Label -->
    <label class="condition-label">
      {{ i === 0 ? 'Select Business Segment :' : 'AND' }}
    </label>

    <!-- Dropdown -->
    <app-select-dropdown
      [selectText]="'Select Business Segment'"
      [listOfValues]="businessSegments"
      [(ngModel)]="row.selectedBusinessSegment"
      class="ml-2"
    ></app-select-dropdown>

    <!-- Search Box -->
    <input
      type="text"
      class="form-control ml-2"
      style="width: 250px; height: calc(2.8rem + 1px);"
      placeholder="Type to search"
      [(ngModel)]="row.newBusinessSegment"
    />

    <!-- Add Button (Only on last row) -->
    <button *ngIf="i === rows.length - 1"
      class="btn btn-primary ml-2 btn-sm"
      style="height: calc(2.8rem + 2px);"
      (click)="addBusinessSegment()">
      Add
    </button>

    <!-- Remove Button (Visible for all except first row) -->
    <button *ngIf="i > 0"
      class="btn btn-danger ml-2 btn-sm"
      style="height: calc(2.8rem + 2px);"
      (click)="removeBusinessSegment(i)">
      Remove
    </button>
  </div>
</div>

 .container-fluid {
  max-width: 800px;
}

.condition-label {
  font-weight: bold;
  width: 180px;
  text-align: right;
  padding-right: 10px;
}       
