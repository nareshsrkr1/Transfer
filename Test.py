<!-- date-selector.component.html -->

<div class="container-fluid d-flex align-items-center justify-content-center">
  <div class="form-group">
    <div class="d-flex align-items-center">
      <label for="businessDate" class="mr-2">Business Date:</label>
      <input type="date" id="businessDate" [(ngModel)]="selectedDate" class="form-control" required>
    </div>
    <div class="mt-3">
      <button (click)="onApplyDate()" class="btn btn-primary mr-2">Apply Date</button>
      <button (click)="onRestore()" class="btn btn-secondary">Restore</button>
    </div>
  </div>
</div>
