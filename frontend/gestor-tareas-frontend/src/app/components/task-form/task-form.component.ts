// frontend/src/app/components/task-form/task-form.component.ts

import { Component } from '@angular/core';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { TaskService } from '../../services/task.service';

@Component({
  selector: 'app-task-form',
  templateUrl: './task-form.component.html',
})
export class TaskFormComponent {
  form: FormGroup;  // sólo declaramos

  constructor(
    private fb: FormBuilder,
    private taskSvc: TaskService
  ) {
    // ① Inicializamos aquí el formulario, después de que fb ya está asignado
    this.form = this.fb.nonNullable.group({
      title: ['', Validators.required],
      due_date: [''],
      priority: ['Media']
    });
  }

  submit() {
    if (this.form.valid) {
      const payload = this.form.value; // { title, due_date, priority } sin null
      this.taskSvc.createTask(payload).subscribe();
      this.form.reset({ priority: 'Media' });
    }
  }
}
