// frontend/src/app/components/task-card/task-card.component.ts
import { Component, Input, Output, EventEmitter } from '@angular/core';
@Component({
  selector: 'app-task-card',
  templateUrl: './task-card.component.html',
})
export class TaskCardComponent {
  @Input() task!: any;
  @Output() deleted = new EventEmitter<string>();
  onDelete() { this.deleted.emit(this.task.id); }
}
