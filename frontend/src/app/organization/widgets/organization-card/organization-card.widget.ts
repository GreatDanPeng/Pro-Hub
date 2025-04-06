/**
 * The Organization Card widget abstracts the implementation of each
 * individual organization card from the whole organization page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, Inject } from '@angular/core';
import { Organization } from '../../organization.model';
import { Profile } from '../../../profile/profile.service';
import { MatDialog } from '@angular/material/dialog';
import { ApplicationForm } from '../organization-application-form/application-form.widget';
import { MatSnackBar } from '@angular/material/snack-bar';
import { OrganizationSettingsDialogComponent } from '../organization-settings-dialog/organization-settings-dialog.component';
import { HttpClient } from '@angular/common/http';
import { ProfileService } from '../../../profile/profile.service';
import { User } from '../../../models.module';
import { OrganizationService } from 'src/app/organization/organization.service';

@Component({
  selector: 'organization-card',
  templateUrl: './organization-card.widget.html',
  styleUrls: ['./organization-card.widget.css']
})
export class OrganizationCard {
  /** The organization to show */
  @Input() organization!: Organization;
  /** The profile of the currently signed in user */
  @Input() profile?: Profile;
  isLeader: boolean = false;
  organizationStatus: string = '';
  isMemberFlag: boolean = false;
  members: User[] = [];

  constructor(
    private profileService: ProfileService,
    @Inject(OrganizationService)
    private organizationService: OrganizationService,
    private snackBar: MatSnackBar,
    public dialog: MatDialog
  ) {}

  loading: boolean = true;

  ngOnInit() {
    this.loading = true;
    Promise.all([
      this.checkIfLeader(),
      this.getOrganizationStatus(),
      this.checkIfMember()
    ]).finally(() => {
      this.loading = false;
    });
  }

  checkIfMember() {
    this.profileService.getCurrentUserProfile().subscribe({
      next: (currentUser) => {
        this.organizationService
          .getOrganizationMembers(this.organization.slug)
          .subscribe({
            next: (members) => {
              this.members = members;
              this.isMemberFlag = members.some(
                (member) => member.onyen === currentUser.onyen
              );
            },
            error: (error) => {
              if (error.status === 404 || error.status === 403) {
                this.isMemberFlag = false;
              }
            }
          });
      },
      error: () => {
        this.snackBar.open('Error fetching user profile.', 'Close', {
          duration: 3000
        });
      }
    });
  }

  isMember(): boolean {
    return this.isMemberFlag;
  }

  checkIfLeader() {
    this.profileService.getCurrentUserProfile().subscribe({
      next: (currentUser) => {
        this.organizationService
          .checkLeaderStatus(this.organization.slug, currentUser.onyen)
          .subscribe({
            next: (isLeader) => {
              this.isLeader = isLeader;
            }
          });
      },
      error: () => {
        this.snackBar.open('Error fetching user profile.', 'Close', {
          duration: 3000
        });
      }
    });
  }

  getOrganizationStatus() {
    this.organizationService
      .getOrganizationStatus(this.organization.slug)
      .subscribe({
        next: (status) => {
          this.organizationStatus = status;
        }
      });
  }

  applyToOrganization() {
    const dialogRef = this.dialog.open(ApplicationForm, {
      width: '800px',
      data: { organization: this.organization }
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log('The dialog was closed');
      // TODO: Handle the result here
    });
  }

  joinOrganization() {
    this.profileService.getCurrentUserProfile().subscribe({
      next: (currentUser) => {
        this.organizationService
          .addMember(this.organization.slug, currentUser.onyen)
          .subscribe({
            next: () => {
              window.location.reload();
            }
          });
      },
      error: () => {
        this.snackBar.open('Error fetching user profile.', 'Close', {
          duration: 3000
        });
      }
    });
  }

  isJoinButton(): boolean {
    return this.organizationStatus === 'open' && !this.isMemberFlag;
  }

  isPrivateButton(): boolean {
    return this.organizationStatus === 'closed';
  }

  isLeaderButton(): boolean {
    return this.isLeader;
  }

  isRequestRequired(): boolean {
    return this.organizationStatus === 'request' && !this.isMemberFlag;
  }

  openSettingsDialog() {
    const dialogRef = this.dialog.open(OrganizationSettingsDialogComponent, {
      width: '600px',
      data: { organization: this.organization }
    });

    dialogRef.afterClosed().subscribe((result) => {
      console.log('The dialog was closed');
      // TODO: Handle the result here
    });
  }
}
