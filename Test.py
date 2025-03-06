<div class="container-fluid">
  <div class="row d-flex align-items-center mb-2" *ngFor="let row of rows; let i = index">
    <!-- First row shows "Select Business Segment", others show "AND" -->
    <label class="condition-label">
      {{ i === 0 ? 'Select Business Segment :' : 'AND' }}
    </label>

    <!-- Dropdown -->
    <app-select-dropdown
      [selectText]="i === 0 ? 'Select Business Segment' : ''"
      [listOfValues]="businessSegments"
      [(ngModel)]="row.selectedBusinessSegment"
      class="ml-2 dropdown-width"
    ></app-select-dropdown>

    <!-- Search Box -->
    <input
      type="text"
      class="form-control ml-2 search-width"
      placeholder="Type to search"
      [(ngModel)]="row.newBusinessSegment"
    />

    <!-- Add Button (Only on last row) -->
    <button *ngIf="i === rows.length - 1"
      class="btn btn-primary ml-2 btn-sm add-btn"
      (click)="addBusinessSegment()">
      Add
    </button>

    <!-- Remove Button (Visible for all except first row) -->
    <button *ngIf="i > 0"
      class="btn btn-danger btn-sm remove-btn"
      (click)="removeBusinessSegment(i)">
      Remove
    </button>
  </div>
</div>


        .container-fluid {
  max-width: 800px;
}

/* Ensure labels align properly */
.condition-label {
  font-weight: bold;
  width: 180px; /* Fixed width so "Select Business Segment" and "AND" align */
  text-align: right;
  padding-right: 10px;
}

/* Dropdown, search box, and buttons should align properly */
.dropdown-width {
  width: 250px;
}

.search-width {
  width: 250px;
  height: calc(2.8rem + 1px);
}

/* Align Add button properly */
.add-btn {
  height: calc(2.8rem + 2px);
}

/* Move Remove button to the right */
.remove-btn {
  margin-left: auto;
  height: calc(2.8rem + 2px);
}
        
