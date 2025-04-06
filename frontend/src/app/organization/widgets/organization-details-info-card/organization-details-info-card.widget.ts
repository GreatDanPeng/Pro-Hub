/**
 * The Organization Details Info Card widget abstracts the implementation of each
 * individual organization detail card from the whole organization detail page.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Component, Input, OnInit } from '@angular/core';
import { OrganizationService } from '../../organization.service';
import { Organization } from '../../organization.model';
import { Profile } from '../../../profile/profile.service';
import { SocialMediaIconWidgetService } from 'src/app/shared/social-media-icon/social-media-icon.widget.service';
import { ProfileService } from '../../../profile/profile.service';
import { User } from '../../../models.module';
@Component({
  selector: 'organization-details-info-card',
  templateUrl: './organization-details-info-card.widget.html',
  styleUrls: ['./organization-details-info-card.widget.css']
})
export class OrganizationDetailsInfoCard {
  /** The organization to show */
  @Input() organization: any;
  /** The currently logged in user */
  @Input() profile?: Profile;
  /** Whether or not the user has permission to create events */
  @Input() eventCreationPermissions!: boolean | null;

  members: User[] = [];
  isMemberFlag: boolean = false;
  leaders: User[] = [];
  displayedColumns: string[] = [
    'firstName',
    'lastName',
    'onyen',
    'email',
    'pronouns'
  ];
  leaderColumns: string[] = ['firstName', 'lastName', 'onyen'];

  constructor(
    private organizationService: OrganizationService,
    private icons: SocialMediaIconWidgetService,
    private profileService: ProfileService
  ) {}

  ngOnInit() {
    this.checkIfMember();
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
              this.collectLeaders();
            },
            error: (error) => {
              if (error.status === 404 || error.status === 403) {
                this.isMemberFlag = false;
              }
            }
          });
      },
      error: () => {
        this.isMemberFlag = false;
      }
    });
  }

  collectLeaders() {
    this.members.forEach((member) => {
      this.organizationService
        .checkLeaderStatus(this.organization.slug, member.onyen)
        .subscribe({
          next: (isLeader) => {
            console.log(
              `Checked leader status for ${member.onyen}: ${isLeader}`
            );
            if (isLeader) {
              this.leaders.push(member);
            }
          },
          error: (error) => {
            console.error(
              `Error checking leader status for ${member.onyen}:`,
              error
            );
          }
        });
    });
    console.log('Members:', this.members);
    console.log('Leaders:', this.leaders);
  }
}
