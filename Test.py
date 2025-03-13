<div class="container">
  <div class="row">
    <!-- Business Segments Section -->
    <div class="col-md-6">
      <h4>Business Segments</h4>
      <div *ngFor="let row of businessRows; let i = index" class="segment-row">
        <app-select-dropdown [listOfValues]="businessSegments" [(ngModel)]="row.selectedSegment"></app-select-dropdown>
        <input type="text" class="search-box" [(ngModel)]="row.newBusinessSegment" placeholder="Type to search" />
        <button *ngIf="i === businessRows.length - 1" class="btn btn-primary btn-sm" (click)="addBusinessSegment()">Add</button>
        <button *ngIf="i > 0" class="btn btn-danger btn-sm" (click)="removeBusinessSegment(i)">Remove</button>
      </div>
    </div>

    <!-- Overrides Section -->
    <div class="col-md-6">
      <h4>Overrides</h4>
      <div *ngFor="let row of overrideRows; let i = index" class="override-row">
        <app-select-dropdown [listOfValues]="overrideSegments" [(ngModel)]="row.selectedOverride"></app-select-dropdown>
        <input type="text" class="search-box" [(ngModel)]="row.newOverrideSegment" placeholder="Type to search" />
        <button *ngIf="i === overrideRows.length - 1" class="btn btn-primary btn-sm" (click)="addOverrideSegment()">Add</button>
        <button *ngIf="i > 0" class="btn btn-danger btn-sm" (click)="removeOverrideSegment(i)">Remove</button>
      </div>
    </div>
  </div>

  <!-- Submit & Reset Buttons -->
  <div class="row justify-content-center mt-3">
    <button class="btn btn-success">Submit</button>
    <button class="btn btn-warning ml-2">Reset</button>
  </div>
</div>


.container {
  width: 90%;
  margin: auto;
}

.segment-row, .override-row {
  display: flex;
  align-items: center;
  margin-bottom: 10px;
}

app-select-dropdown {
  width: 200px;
  margin-right: 10px;
}

.search-box {
  flex-grow: 1;
  max-width: 250px;
  margin-right: 10px;
}

button {
  height: 30px;
}
