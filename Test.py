<div class="container-fluid">
  <div class="row d-flex justify-content-center" *ngFor="let row of rows; let i = index">
    
    <!-- Flex Container for Proper Column Alignment -->
    <div class="d-flex align-items-center w-100">
      
      <!-- Label only for the first row -->
      <label *ngIf="i == 0" class="mr-2">Select Business Segment :</label>
      
      <!-- AND (Visible from second row onwards) -->
      <span *ngIf="i > 0" class="mr-2">AND</span>

      <!-- Dropdown -->
      <app-select-dropdown 
        [listOfValues]="businessSegments"
        [(ngModel)]="row.selectedBusinessSegment"
        class="ml-2 flex-grow-1">
      </app-select-dropdown>

      <!-- Search Box -->
      <input type="text" 
        class="form-control ml-2 flex-grow-1" 
        style="width: 250px; height: calc(2.8rem + 1px);" 
        placeholder="Type to search" 
        [(ngModel)]="row.newBusinessSegment" />

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
</div>
