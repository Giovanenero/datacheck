import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-spinner',
  standalone: false,
  templateUrl: './spinner.html',
  styleUrl: './spinner.css'
})
export class Spinner {

  @Input() isLoading: boolean = false;

}
