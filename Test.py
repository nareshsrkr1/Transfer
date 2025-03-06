import { Component, OnInit, ChangeDetectorRef } from '@angular/core';
import { ExecutionService } from '../components/d-and-t/service/execution.service';

@Component({
  selector: 'app-dynamic-segmentation',
  templateUrl: './dynamic-segmentation.component.html',
  styleUrls: ['./dynamic-segmentation.component.css'],
})
export class DynamicSegmentationComponent implements OnInit {
  businessSegments: string[] = [];
  rows: { selectedBusinessSegment: string; newBusinessSegment: string }[] = [];

  constructor(private executionService: ExecutionService, private cdRef: ChangeDetectorRef) {}

  ngOnInit(): void {
    this.fetchBusinessSegments();
    this.addBusinessSegment(); // Start with one row
  }

  fetchBusinessSegments(): void {
    this.executionService.fetchBusinessSegments().subscribe(
      (data) => {
        this.businessSegments = data;
      },
      (error) => console.error('Error fetching business segments', error)
    );
  }

  addBusinessSegment(): void {
    this.rows.push({ selectedBusinessSegment: '', newBusinessSegment: '' });

    // Force UI update to prevent rendering delay
    this.cdRef.detectChanges();
  }

  removeBusinessSegment(index: number): void {
    if (this.rows.length > 1) {
      this.rows.splice(index, 1);
      this.cdRef.detectChanges();
    }
  }
}

<div class="container">
  <div class="row justify-content-center">
    <div class="col-md-8">
      <div *ngFor="let row of rows; let i = index" class="d-flex align-items-center mb-2">
        <!-- Dropdown -->
        <app-select-dropdown
          [selectText]="'Select Business Segment : '"
          [listOfValues]="businessSegments"
          [(ngModel)]="row.selectedBusinessSegment"
          class="form-control"
          style="margin-top: 1rem; width: 200px;">
        </app-select-dropdown>

        <!-- Search Bar -->
        <input type="text" class="form-control ml-2" 
          style="width: 250px; height: 38px;" 
          placeholder="Type to search" 
          [(ngModel)]="row.newBusinessSegment">

        <!-- Add Button (Always on last row) -->
        <button *ngIf="i === rows.length - 1" class="btn btn-primary ml-2 btn-sm" 
          (click)="addBusinessSegment()">Add</button>

        <!-- Remove Button (Not for first row) -->
        <button *ngIf="i > 0" class="btn btn-danger ml-2 btn-sm" 
          (click)="removeBusinessSegment(i)">Remove</button>
      </div>
    </div>
  </div>
</div>
