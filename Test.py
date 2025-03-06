addBusinessSegment(): void {
  this.rows.push({ selectedBusinessSegment: '', newBusinessSegment: '' });

  // Run change detection asynchronously for a smoother UI update
  setTimeout(() => this.cdRef.detectChanges());
}
removeBusinessSegment(index: number): void {
  if (this.rows.length > 1) {
    this.rows.splice(index, 1);

    // Run change detection asynchronously
    setTimeout(() => this.cdRef.detectChanges());
  }
}
