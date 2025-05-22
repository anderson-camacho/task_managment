// frontend/src/app/services/task.service.ts

import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

// ① Exportamos la interfaz para que otros archivos puedan importarla
export interface Task {
    id: string;
    title: string;
    status: string;
    due_date: string;
    priority?: string;
    tags?: string[];
}

@Injectable({ providedIn: 'root' })
export class TaskService {
    private api = environment.apiUrl + '/tasks';

    constructor(private http: HttpClient) { }

    private headers(): HttpHeaders {
        const token = localStorage.getItem('token');
        return new HttpHeaders({ Authorization: `Bearer ${token}` });
    }

    getTasks(): Observable<Task[]> {
        return this.http.get<Task[]>(this.api, { headers: this.headers() });
    }

    createTask(data: Partial<Task>): Observable<Task> {
        return this.http.post<Task>(this.api, data, { headers: this.headers() });
    }

    updateTask(id: string, data: Partial<Task>): Observable<Task> {
        return this.http.put<Task>(`${this.api}/${id}`, data, { headers: this.headers() });
    }

    deleteTask(id: string): Observable<any> {
        return this.http.delete(`${this.api}/${id}`, { headers: this.headers() });
    }
}
