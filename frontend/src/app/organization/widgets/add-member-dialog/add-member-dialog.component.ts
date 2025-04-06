import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';
import { HttpClient } from '@angular/common/http';
import { OrganizationService } from '../../organization.service';

@Component({
  selector: 'add-member-dialog',
  templateUrl: './add-member-dialog.component.html',
  styleUrls: ['./add-member-dialog.component.css']
})
export class AddMemberDialogComponent {
  onyen: string = '';

  constructor(
    public dialogRef: MatDialogRef<AddMemberDialogComponent>,
    @Inject(MAT_DIALOG_DATA) public data: { organizationSlug: string },
    private snackBar: MatSnackBar,
    private http: HttpClient,
    private organizationService: OrganizationService
  ) {}

  onConfirm() {
    if (!this.onyen.trim()) {
      this.snackBar.open('Please enter a valid onyen', 'Close', {
        duration: 3000
      });
      return;
    }

    this.organizationService
      .addMember(this.data.organizationSlug, this.onyen)
      .subscribe({
        next: () => this.dialogRef.close(true),
        error: () => this.dialogRef.close(false)
      });
  }

  onDelete() {
    if (!this.onyen.trim()) {
      this.snackBar.open('Please enter a valid onyen', 'Close', {
        duration: 3000
      });
      return;
    }
    this.organizationService
      .removeMember(this.data.organizationSlug, this.onyen)
      .subscribe({
        next: () => this.dialogRef.close(true),
        error: () => this.dialogRef.close(false)
      });
  }

  onCancel() {
    this.dialogRef.close();
  }
}
