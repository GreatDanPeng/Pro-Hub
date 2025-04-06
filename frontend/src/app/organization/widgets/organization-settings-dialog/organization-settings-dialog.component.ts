import { Component, Inject } from '@angular/core';
import {
  MatDialogRef,
  MAT_DIALOG_DATA,
  MatDialog
} from '@angular/material/dialog';
import { Organization } from '../../organization.model';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationService } from '../../organization.service';
import { HttpClient } from '@angular/common/http';
import { AddMemberDialogComponent } from '../add-member-dialog/add-member-dialog.component';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'organization-settings-dialog',
  templateUrl: './organization-settings-dialog.component.html',
  styleUrls: ['./organization-settings-dialog.component.css']
})
export class OrganizationSettingsDialogComponent {
  organization: Organization;
  description: string;
  org_name: string;
  shortname: string;
  isPublic: boolean = false;
  requiresApplication: boolean = false;

  warningMessage: string = '';
  constructor(
    public dialogRef: MatDialogRef<OrganizationSettingsDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { organization: Organization },
    private snackBar: MatSnackBar,
    private organizationService: OrganizationService,
    private http: HttpClient,
    private dialog: MatDialog
  ) {
    this.organization = data.organization;
    this.description = data.organization.short_description;
    this.org_name = data.organization.name;
    this.shortname = data.organization.shorthand;
    this.isPublic = data.organization.public;
    this.requiresApplication = data.organization.application_required;
  }

  onSave() {
    if (
      !this.org_name.trim() ||
      !this.organization.slug.trim() ||
      !this.shortname.trim() ||
      !this.organization.logo.trim()
    ) {
      this.warningMessage = 'All fields must be filled out.';
      return;
    }
    this.warningMessage = '';
    this.organization.name = this.org_name;
    this.organization.short_description = this.description;
    this.organization.shorthand = this.shortname;
    this.organization.public = this.isPublic;
    this.organization.application_required = this.requiresApplication;
    // Handle save logic here
    console.log('Settings saved');
    // Pop up a snackbar to indicate that the settings have been saved
    this.http
      .put<Organization>(
        `/api/organizations/${this.organization.slug}`,
        this.organization
      )
      .subscribe({
        next: (updatedOrg) => {
          this.snackBar.open('Settings saved successfully!', 'Close', {
            duration: 3000
          });
          this.dialogRef.close(updatedOrg);
        },
        error: (error) => {
          this.snackBar.open(
            `Error saving settings: ${error.error?.detail || 'Unknown error'}`,
            'Close',
            { duration: 3000 }
          );
        }
      });
  }

  addMember(onyen: string) {
    if (!onyen?.trim()) {
      this.snackBar.open('Please enter a valid onyen', 'Close', {
        duration: 3000
      });
      return;
    }

    this.http
      .post(
        `/api/organizations/${this.organization.slug}/add_membership/${onyen}`,
        {}
      )
      .subscribe({
        next: () => {
          this.snackBar.open(
            `Successfully added ${onyen} to organization`,
            'Close',
            {
              duration: 3000
            }
          );
        },
        error: (error) => {
          this.snackBar.open(
            `Error adding member: ${error.error?.detail || 'Unknown error'}`,
            'Close',
            { duration: 3000 }
          );
        }
      });
  }

  onCancel() {
    this.dialogRef.close();
  }

  updateCharCount(): void {
    // This function will be triggered on every input event,
    // and the character count will be automatically updated in the template due to Angular's data binding.
  }

  openAddMemberDialog() {
    const dialogRef = this.dialog.open(AddMemberDialogComponent, {
      width: '400px',
      data: { organizationSlug: this.organization.slug }
    });
    dialogRef.afterClosed().subscribe((result: any) => {
      if (result) {
        // Handle the result if needed
      }
    });
  }

  viewApplications() {}
}
