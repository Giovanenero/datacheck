import { NgModule, provideBrowserGlobalErrorListeners } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { AppRoutingModule } from './app-routing-module';

import { App } from './app';

import { MatInputModule } from '@angular/material/input';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatDatepickerModule } from '@angular/material/datepicker';
import { MatNativeDateModule } from '@angular/material/core'; // ou MatMomentDateModule se preferir moment.js
import { MatCheckboxModule } from '@angular/material/checkbox';
import { Projudi } from './components/projudi/projudi';

import { HttpClientModule } from '@angular/common/http';
import { Spinner } from './components/spinner/spinner';


@NgModule({
  declarations: [
    App,
    Projudi,
    Spinner
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    MatInputModule,
    MatFormFieldModule,
    MatNativeDateModule,
    MatDatepickerModule,
    MatCheckboxModule,
    HttpClientModule
    
  ],
  providers: [
    provideBrowserGlobalErrorListeners()
  ],
  bootstrap: [App]
})
export class AppModule { }
