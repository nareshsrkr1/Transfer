<div class="container-fluid d-flex align-items-center justify-content-center">
  <div class="row">
    <!-- Business Date and Business Text Block -->
    <div class="col-md-6">
      <div class="form-group">
        <div class="d-flex flex-column align-items-start">
          <label class="mb-2">Business Date:</label>
          <input type="date" id="businessDate" [(ngModel)]="selectedDate" class="form-control" required>
          <label class="mb-2">Business Text:</label>
          <input type="text" id="businessText" [(ngModel)]="selectedText" class="form-control" required>
        </div>
      </div>
    </div>

    <!-- Buttons Block -->
    <div class="col-md-6">
      <div class="form-group">
        <div class="d-flex flex-column align-items-start">
          <button (click)="onRestoreDate()" class="btn btn-primary btn-block mb-2">Restore Date</button>
          <button (click)="onArchiveData()" class="btn btn-secondary btn-block">Archive Data</button>
        </div>
      </div>
    </div>
  </div>
</div>
