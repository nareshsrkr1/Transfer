// date-selector.component.ts

import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-date-selector',
  templateUrl: './date-selector.component.html',
  styleUrls: ['./date-selector.component.css']
})
export class DateSelectorComponent {
  selectedDate: Date;

  constructor(private http: HttpClient) {}

  onSubmit() {
    // Format the date as yyyy-mm-dd
    const formattedDate = this.formatDate(this.selectedDate);

    // Make a POST request to your backend
    this.http.post('your-backend-api-endpoint', { date: formattedDate })
      .subscribe(response => {
        console.log('Backend response:', response);
        // Add your further logic for handling the backend response
      });
  }

  private formatDate(date: Date): string {
    const year = date.getFullYear();
    const month = ('0' + (date.getMonth() + 1)).slice(-2); // Adding 1 to month as it is 0-indexed
    const day = ('0' + date.getDate()).slice(-2);
    return `${year}-${month}-${day}`;
  }
}
