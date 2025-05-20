import { Component, OnInit } from '@angular/core';
import { TaskService, Task } from '../../services/task.service';

@Component({
  selector: 'app-task-list',
  templateUrl: './task-list.component.html',
})
export class TaskListComponent implements OnInit {
  tasks: Task[] = [];  // ahora sí reconoce Task

  constructor(private taskSvc: TaskService) {}

  ngOnInit() {
    this.taskSvc.getTasks().subscribe(data => this.tasks = data);
  }
}
