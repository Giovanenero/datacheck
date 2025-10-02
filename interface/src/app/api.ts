import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiURL = 'http://fswmldev01.wise.corp:5550';

  constructor(private http: HttpClient) { }

  getPessoa(cpf:string, nome:string, nascimento:string): Observable<any> {
    return this.http.get(`${this.apiURL}/pessoa?cpf=${cpf}&nome=${nome}&nascimento=${nascimento}`);
  }
}