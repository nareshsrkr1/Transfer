<div class="container-fluid">
    <div class="row">
        <!-- Business Segments Section -->
        <div class="col-md-5 business-segments-container">
            <h4 class="text-center">Business Segments</h4>
            <div *ngFor="let row of businessSegments; let i = index" class="segment-row">
                <div class="dropdown-container">
                    <app-select-dropdown [listOfValues]="businessSegmentOptions" [(ngModel)]="row.selectedSegment"></app-select-dropdown>
                </div>
                <input type="text" class="form-control search-box" [(ngModel)]="row.newBusinessSegment" placeholder="Type to search">
                <button *ngIf="i === businessSegments.length - 1" class="btn btn-primary btn-sm" (click)="addBusinessSegment()">Add</button>
                <button *ngIf="i > 0" class="btn btn-danger btn-sm" (click)="removeBusinessSegment(i)">Remove</button>
            </div>
        </div>

        <!-- Overrides Section -->
        <div class="col-md-5 overrides-container">
            <h4 class="text-center">Overrides</h4>
            <div *ngFor="let row of overrides; let i = index" class="override-row">
                <div class="dropdown-container">
                    <app-select-dropdown [listOfValues]="overrideOptions" [(ngModel)]="row.selectedOverride"></app-select-dropdown>
                </div>
                <input type="text" class="form-control search-box" [(ngModel)]="row.newOverride" placeholder="Type to search">
                <button *ngIf="i === overrides.length - 1" class="btn btn-primary btn-sm" (click)="addOverride()">Add</button>
                <button *ngIf="i > 0" class="btn btn-danger btn-sm" (click)="removeOverride(i)">Remove</button>
            </div>
        </div>
    </div>

    <!-- Submit & Reset Buttons -->
    <div class="row justify-content-center mt-3">
        <button class="btn btn-success mx-2" (click)="submitForm()">Submit</button>
        <button class="btn btn-warning mx-2" (click)="resetForm()">Reset</button>
    </div>
</div>
