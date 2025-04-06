import { HttpClient } from '@angular/common/http';
import { Component, Inject } from '@angular/core';
import { MatDialogRef, MAT_DIALOG_DATA } from '@angular/material/dialog';
import { MatSnackBar } from '@angular/material/snack-bar';

@Component({
  selector: 'application-form',
  templateUrl: './application-form.widget.html',
  styleUrls: ['./application-form.widget.css']
})
export class ApplicationForm {
  name: string = '';
  id: string = '';
  reason: string = '';
  organizationId: number;
  userId: number;
  warningMessage: string = '';

  constructor(
    public dialogRef: MatDialogRef<ApplicationForm>,
    @Inject(MAT_DIALOG_DATA)
    public data: { organizationId: number; userId: number },
    private snackBar: MatSnackBar,
    private http: HttpClient
  ) {
    this.organizationId = data.organizationId;
    this.userId = data.userId;
  }

  onSubmit() {
    if (this.name.length < 4) {
      this.warningMessage = 'Name must be at least 4 characters long.';
      return;
    }

    const idPattern = /^\d{9}$/;
    if (!idPattern.test(this.id)) {
      this.warningMessage = 'ID must be a 9-digit number.';
      return;
    }

    // All fields must be non-empty
    if (!this.reason) {
      this.warningMessage = 'Reason for joining is required.';
      return;
    }

    const application = {
      organization_id: this.organizationId,
      name: this.name,
      user_id: this.userId,
      reason_to_join: this.reason,
      status: 'pending'
    };

    this.http.post('/api/organizations/applications', application).subscribe({
      next: () => {
        this.snackBar.open('Application submitted successfully!', 'Close', {
          duration: 3000
        });
        this.dialogRef.close();
      },
      error: () => {
        this.snackBar.open('Error submitting application.', 'Close', {
          duration: 3000
        });
      }
    });

    // Display snackbar message
    this.snackBar.open('Application submitted successfully!', 'Close', {
      duration: 3000
    });
    this.dialogRef.close();
  }

  onCancel() {
    this.dialogRef.close();
  }
}
