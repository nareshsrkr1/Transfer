<!-- Search Box -->
<input type="text" 
  class="form-control ml-2" 
  [ngClass]="{'short-input': i === rows.length - 1 && i > 0}" 
  style="height: calc(2.8rem + 1px);" 
  placeholder="Type to search" 
  [(ngModel)]="row.newBusinessSegment" />

.short-input {
  width: calc(250px - 50px); /* Reduce width by Add button size */
}
