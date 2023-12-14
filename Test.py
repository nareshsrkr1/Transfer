<div class="container-fluid d-flex align-items-center justify-content-center">
  <div class="row">
    <!-- First Block -->
    <div class="col-md-6">
      <div class="form-group">
        <div class="d-flex flex-column align-items-start">
          <label class="mb-2">Restore Data:</label>
          <label for="businessDate" style="white-space: nowrap;">Business Date:</label>
          <input type="date" id="businessDate" [(ngModel)]="selectedDate" class="form-control" required>
          <div class="mt-3">
            <button (click)="onApplyDate()" class="btn btn-primary btn-block mb-2">Apply Date</button>
            <button (click)="onRestore()" class="btn btn-secondary btn-block">Restore</button>
          </div>
        </div>
      </div>
    </div>

    <!-- Second Block -->
    <div class="col-md-6">
      <div class="form-group">
        <div class="d-flex flex-column align-items-start">
          <label class="mb-2">Adhoc Run:</label>
          <label for="businessText" style="white-space: nowrap;">Business Text:</label>
          <input type="text" id="businessText" [(ngModel)]="selectedText" class="form-control" required>
          <div class="mt-3">
            <button (click)="onApplyText()" class="btn btn-primary btn-block mb-2">Apply Text</button>
            <button (click)="onRestoreText()" class="btn btn-secondary btn-block">Restore Text</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
