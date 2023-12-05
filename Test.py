<!-- date-selector.component.html -->

<div class="container-fluid d-flex align-items-center justify-content-center">
  <div class="form-group">
    <div class="d-flex align-items-center">
      <label for="businessDate" class="mr-2">Business Date:</label>
      <input type="date" id="businessDate" [(ngModel)]="selectedDate" class="form-control" required>
    </div>
    <button (click)="onSubmit()" class="btn btn-primary mt-3">Submit</button>
  </div>
</div>
