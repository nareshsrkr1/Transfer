<div class="container-fluid">
  <div class="row justify-content-center">
    
    <!-- Left Panel: Business Segments -->
    <div class="col-md-5">
      <h5>Business Segments</h5>
      <div *ngFor="let row of businessRows; let i = index" class="row align-items-center mb-2">
        
        <app-select-dropdown [listOfValues]="businessSegments"
          [(ngModel)]="row.selectedBusinessSegment" class="col-md-4"></app-select-dropdown>

        <input type="text" class="form-control col-md-4" 
          [ngClass]="{'short-input': i === businessRows.length - 1 && i > 0}" 
          placeholder="Type to search" [(ngModel)]="row.newBusinessSegment"/>

        <button *ngIf="i === businessRows.length - 1" class="btn btn-primary ml-2 btn-sm" 
          (click)="addBusinessSegment()">Add</button>

        <button *ngIf="i > 0" class="btn btn-danger ml-2 btn-sm" 
          (click)="removeBusinessSegment(i)">Remove</button>

      </div>
    </div>

    <!-- Right Panel: Overrides -->
    <div class="col-md-5">
      <h5>Overrides</h5>
      <div *ngFor="let row of overrideRows; let i = index" class="row align-items-center mb-2">
        
        <app-select-dropdown [listOfValues]="overrideSegments"
          [(ngModel)]="row.selectedOverrideSegment" class="col-md-4"></app-select-dropdown>

        <input type="text" class="form-control col-md-4" 
          [ngClass]="{'short-input': i === overrideRows.length - 1 && i > 0}" 
          placeholder="Type to search" [(ngModel)]="row.newOverrideSegment"/>

        <button *ngIf="i === overrideRows.length - 1" class="btn btn-primary ml-2 btn-sm" 
          (click)="addOverrideSegment()">Add</button>

        <button *ngIf="i > 0" class="btn btn-danger ml-2 btn-sm" 
          (click)="removeOverrideSegment(i)">Remove</button>

      </div>
    </div>

  </div>

  <!-- AND, Submit, and Reset buttons at the bottom center -->
  <div class="row justify-content-center mt-4">
    <button class="btn btn-secondary mx-2">AND</button>
    <button class="btn btn-success mx-2">Submit</button>
    <button class="btn btn-warning mx-2">Reset</button>
  </div>
</div>


.short-input {
  width: calc(250px - 50px); /* Reduce width for last-row inputs with Add + Remove */
}

.container-fluid {
  padding: 20px;
}

h5 {
  text-align: center;
  margin-bottom: 10px;
}



businessRows = [{ selectedBusinessSegment: '', newBusinessSegment: '' }];
overrideRows = [{ selectedOverrideSegment: '', newOverrideSegment: '' }];

addBusinessSegment() {
  this.businessRows.push({ selectedBusinessSegment: '', newBusinessSegment: '' });
}

removeBusinessSegment(index: number) {
  this.businessRows.splice(index, 1);
}

addOverrideSegment() {
  this.overrideRows.push({ selectedOverrideSegment: '', newOverrideSegment: '' });
}

removeOverrideSegment(index: number) {
  this.overrideRows.splice(index, 1);
}
