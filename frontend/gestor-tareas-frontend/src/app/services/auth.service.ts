import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, tap } from 'rxjs';
import { environment } from '../../environments/environment';

interface AuthResp { access_token: string; }
interface UserCreds { email: string; password: string; }

@Injectable({ providedIn: 'root' })
export class AuthService {
    private api = environment.apiUrl + '/auth';

    constructor(private http: HttpClient) { }

    register(creds: UserCreds): Observable<any> {
        return this.http.post(`${this.api}/register`, creds);
    }

    login(creds: UserCreds): Observable<AuthResp> {
        return this.http.post<AuthResp>(`${this.api}/login`, creds)
            .pipe(tap(res => localStorage.setItem('token', res.access_token)));
    }

    logout(): void {
        localStorage.removeItem('token');
    }

    getToken(): string | null {
        return localStorage.getItem('token');
    }
}
