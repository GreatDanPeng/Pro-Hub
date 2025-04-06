/**
 * The Organization Service abstracts HTTP requests to the backend
 * from the components.
 *
 * @author Ajay Gandecha, Jade Keegan, Brianna Ta, Audrey Toney
 * @copyright 2024
 * @license MIT
 */

import { Injectable, WritableSignal, computed, signal } from '@angular/core';

import { HttpClient } from '@angular/common/http';
import { AuthenticationService } from '../authentication.service';
import { MatSnackBar } from '@angular/material/snack-bar';
import { Observable, tap } from 'rxjs';
import { Organization } from './organization.model';
import { PermissionService } from '../permission.service';
import { User } from '../models.module';

@Injectable({
  providedIn: 'root'
})
export class OrganizationService {
  /** Organizations signal */
  private organizationsSignal: WritableSignal<Organization[]> = signal([]);
  organizations = this.organizationsSignal.asReadonly();

  /** Computed organization signals */
  adminOrganizations = computed(() => {
    return this.organizations().filter((organization) => {
      return this.permissionService.checkSignal(
        'organization.*',
        'organization/' + organization.slug
      );
    });
  });

  /** Constructor */
  constructor(
    protected http: HttpClient,
    protected auth: AuthenticationService,
    protected snackBar: MatSnackBar,
    protected permissionService: PermissionService
  ) {
    this.getOrganizations();
  }

  /** Refreshes the organization data emitted by the organizations signal. */
  getOrganizations() {
    this.http
      .get<Organization[]>('/api/organizations')
      .subscribe((organizations) => {
        this.organizationsSignal.set(organizations);
      });
  }

  /** Gets an organization based on its slug.
   * @param slug: String representing the organization slug
   * @returns {Observable<Organization | undefined>}
   */
  getOrganization(slug: string): Observable<Organization | undefined> {
    return this.http.get<Organization>('/api/organizations/' + slug);
  }

  /** Returns the new organization object from the backend database table using the backend HTTP post request
   *  and updates the organizations signal to include the new organization.
   * @param organization: Organization to add
   * @returns {Observable<Organization>}
   */
  createOrganization(organization: Organization): Observable<Organization> {
    return this.http
      .post<Organization>('/api/organizations', organization)
      .pipe(
        tap((organization) =>
          this.organizationsSignal.update((organizations) => [
            ...organizations,
            organization
          ])
        )
      );
  }

  /** Returns the updated organization object from the backend database table using the backend HTTP put request
   *  and update the organizations signal to include the updated organization.
   * @param organization: Represents the updated organization
   * @returns {Observable<Organization>}
   */
  updateOrganization(organization: Organization): Observable<Organization> {
    return this.http
      .put<Organization>('/api/organizations/$(organization)', organization)
      .pipe(
        tap((updatedOrganization) =>
          this.organizationsSignal.update((organizations) => [
            ...organizations.filter((o) => o.id != updatedOrganization.id),
            updatedOrganization
          ])
        )
      );
  }

  /** Returns the deleted organization object from the backend database table using the backend HTTP delete request
   *  and updates the organizations signal to exclude the deleted organization.
   * @param organization: Represents the deleted organization
   * @returns {Observable<Organization>}
   */
  deleteOrganization(organization: Organization): Observable<Organization> {
    return this.http
      .delete<Organization>(`/api/organizations/${organization.slug}`)
      .pipe(
        tap((deletedOrganization) => {
          this.organizationsSignal.update((organizations) =>
            organizations.filter((o) => o.id != deletedOrganization.id)
          );
        })
      );
  }

  addMember(organizationSlug: string, onyen: string): Observable<void> {
    return this.http
      .post<void>(
        `/api/organizations/${organizationSlug}/add_membership/${onyen}`,
        {}
      )
      .pipe(
        tap({
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
              `Error adding member: you might input an invalid onyen`,
              'Close',
              { duration: 3000 }
            );
          }
        })
      );
  }

  removeMember(organizationSlug: string, onyen: string): Observable<void> {
    return this.http
      .delete<void>(
        `/api/organizations/${organizationSlug}/remove_membership/${onyen}`
      )
      .pipe(
        tap({
          next: () => {
            this.snackBar.open(
              `Successfully removed ${onyen} from organization`,
              'Close',
              {
                duration: 3000
              }
            );
          },
          error: (error) => {
            this.snackBar.open(
              `Error removing member: you might input an invalid onyen or the user is not a member of this organization}`,
              'Close',
              { duration: 3000 }
            );
          }
        })
      );
  }

  getOrganizationMembers(organizationSlug: string): Observable<User[]> {
    return this.http
      .get<User[]>(`/api/organizations/${organizationSlug}/members`)
      .pipe(
        tap({
          error: (error) => {
            if (error.status !== 404 && error.status !== 403) {
              this.snackBar.open(
                'Error fetching organization members.',
                'Close',
                {
                  duration: 3000
                }
              );
            }
          }
        })
      );
  }

  checkLeaderStatus(
    organizationSlug: string,
    onyen: string
  ): Observable<boolean> {
    return this.http
      .get<boolean>(
        `/api/organizations/${organizationSlug}/${onyen}/authleader`
      )
      .pipe(
        tap({
          error: () => {
            this.snackBar.open('Error checking leader status.', 'Close', {
              duration: 3000
            });
          }
        })
      );
  }

  getOrganizationStatus(organizationSlug: string): Observable<string> {
    return this.http
      .get<string>(`/api/organizations/${organizationSlug}/status`)
      .pipe(
        tap({
          error: () => {
            this.snackBar.open('Error fetching organization status.', 'Close', {
              duration: 3000
            });
          }
        })
      );
  }
}
