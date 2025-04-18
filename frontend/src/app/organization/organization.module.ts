/**
 * The Organization Module couples all features of the Organization feature
 * into a single unit that can be loaded at once. This decreases load time
 * for the overall application and decouples this feature from other features
 * in the application.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';

/* Angular Material Modules */
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { MatDialogModule } from '@angular/material/dialog';
import { MatButtonModule } from '@angular/material/button';
import { MatListModule } from '@angular/material/list';
import { MatAutocompleteModule } from '@angular/material/autocomplete';
import { MatSelectModule } from '@angular/material/select';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatPaginatorModule } from '@angular/material/paginator';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { ReactiveFormsModule } from '@angular/forms';
import { MatIconModule } from '@angular/material/icon';
import { MatTooltipModule } from '@angular/material/tooltip';

import { OrganizationPageComponent } from './organization-page/organization-page.component';
import { OrganizationRoutingModule } from './organization-routing.module';
import { OrganizationDetailsComponent } from './organization-details/organization-details.component';
import { OrganizationAdminComponent } from './organization-admin/organization-admin.component';

import { OrganizationFilterPipe } from './pipes/organization-filter.pipe';

/* UI Widgets */
import { OrganizationCard } from './widgets/organization-card/organization-card.widget';
import { RouterModule } from '@angular/router';
import { SharedModule } from '../shared/shared.module';
import { OrganizationDetailsInfoCard } from './widgets/organization-details-info-card/organization-details-info-card.widget';
import { OrganizationEditorComponent } from '/workspace/frontend/src/app/organization/organization-editor/organization-editor.component';
import { OrganizationNotFoundCard } from './widgets/organization-not-found-card/organization-not-found-card.widget';
import { ApplicationForm } from './widgets/organization-application-form/application-form.widget';
import { OrganizationSettingsDialogComponent } from './widgets/organization-settings-dialog/organization-settings-dialog.component';
import { AddMemberDialogComponent } from './widgets/add-member-dialog/add-member-dialog.component';

@NgModule({
  declarations: [
    OrganizationPageComponent,
    OrganizationDetailsComponent,
    OrganizationEditorComponent,
    OrganizationAdminComponent,

    // Pipes
    OrganizationFilterPipe,

    // UI Widgets
    OrganizationCard,
    OrganizationDetailsInfoCard,
    OrganizationNotFoundCard,
    ApplicationForm,
    OrganizationSettingsDialogComponent,
    AddMemberDialogComponent
  ],
  imports: [
    CommonModule,
    MatTabsModule,
    MatTableModule,
    MatCardModule,
    MatDialogModule,
    MatButtonModule,
    MatSelectModule,
    MatFormFieldModule,
    MatInputModule,
    MatPaginatorModule,
    MatListModule,
    MatAutocompleteModule,
    FormsModule,
    ReactiveFormsModule,
    MatIconModule,
    MatTooltipModule,
    OrganizationRoutingModule,
    RouterModule,
    SharedModule
  ]
})
export class OrganizationModule {}
