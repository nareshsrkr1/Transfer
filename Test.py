<!-- date-selector.component.html -->

<div class="container-fluid d-flex align-items-center justify-content-center">
  <div class="form-group">
    <label for="businessDate">Business Date:</label>
    <div class="input-group">
      <input type="date" id="businessDate" [(ngModel)]="selectedDate" class="form-control" required>
      <div class="input-group-append">
        <button (click)="onSubmit()" class="btn btn-primary">Submit</button>
      </div>
    </div>
  </div>
</div>
