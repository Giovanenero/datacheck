import { Component, Input } from '@angular/core';


@Component({
  selector: 'app-projudi',
  standalone: false,
  templateUrl: './projudi.html',
  styleUrl: './projudi.css'
})
export class Projudi {

  @Input() projudi: any;

  expandedItems: Set<number> = new Set();

  isExpanded(index: number): boolean {
    return this.expandedItems.has(index);
  }

  toggle(index: number) {
    if (this.expandedItems.has(index)) {
      this.expandedItems.delete(index);
    } else {
      this.expandedItems.add(index);
    }
  }

}
