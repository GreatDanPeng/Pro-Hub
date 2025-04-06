# Pro Hub Overview

## Team Member (Sorted by Last Name)

- Peichun Hua
- Haiyun Lv
- Dan Peng

[Project CFP](https://comp423-24f.github.io/exercises/final-project-ideas.html#student-organization-roster-management-and-members-only-features)

Our project aims to extend the organization roaster and add the management of membership of each organization. More specifically:

1. The ability to distinguish type of organization (open to all, application/request-based, closed)
2. The ability for a user to request to join an organization that is not a closed organization
3. The ability for organization leaders to add new members / remove members by using their onyen and update organization information
4. Memberships to have a "level" assigned to it (member, leadership)
5. Memberships to have optional titles (e.g. President, Treasurer)
6. The ability for an organization to list its leaders (and members) on the detailed information page for members.

# Permissions & User Stories

## Guest

### Guest Permissions

| Services       | Create | Read | Update | Delete |
| -------------- | ------ | ---- | ------ | ------ |
| `Organization` | ❌     | ✅   | ❌     | ❌     |
| `Leader`       | ❌     | ✅   | ❌     | ❌     |
| `Member`       | ❌     | ❌   | ❌     | ❌     |

### User Story with Views (eg. Stewie Student as Guest)

As a guest, Stewie Student, I want to check the organization details so that I can decide whether applying to this organization.

![image-20241209181835189](./assets/image-20241209181835189.png)

### Tech Specs

#### Frontend:

- `organization-card` widget: this widget is reused for each organization and updated to accomodate new features, including the display of different organization status (open/application required/private) and membership (non-member, member, leader). We currently opt not to display this information directly, but instead implicitly convey it through different button appearances, as this approach is both informative and concise.
  - The buttons call various functions in `organization-card.widget.ts` to get those information, which in turn call frontend service in `organization.module.ts`.
- `organization-application-form` widget: this widget is created for the guests to hand in application to join the organization that requires so. Note that the backend of this part hasn't been implemented. After having the backend API of this feature, you should add service call to backend API in `organization.module.ts`, and replace Line 56-68 with the added service call.
  - In the frontend, we implement some simple logic to avoid inadvertent touching on "submit" before finishing the form. Basically, the name must contain at least four characters and ID must be 9-digit numbers in accord with UNC convention, and the reason should be filled out.

#### Backend Databases and Entities:

- `OrganizationEntity`: includes an `organization` table with general information about this organization such as `long_description`, `slug`, and `users` (member roster).
  - To decide whether the organization is open or closed, we use boolean `public`. To decide whether the organization is request-based, we use boolean `application_required`. Therefore, we can distinguish types of organiztaions (open, closed, request-based).
  
- `UserEntity`: includes an `user` table with general user information such as `onyen`, `pid`, `roles`, `permissions`, and `organizations`.

#### Backend Models:

- `Organization`: includes an `Organization` model based on `OrganizationEntity`
- `User`: includes a `User` model based on `UserEntity`

#### Backend Services:

- `get_by_slug` in backend/services/organization: Gets the organization by a slug
- `get_status_by_slug` in backend/services/organization: Gets the organization status by a slug

#### Backend APIs:

- `GET /api/organizations/{slug}` to get the general details about this organization
- `GET /api/organizations/{slug}/status` to get the type of this organiztaion, where we distingush `public` as `True` (open), `False` (closed/request-based)

## Member

### Member Permissions

| Services       | Create | Read | Update | Delete |
| -------------- | ------ | ---- | ------ | ------ |
| `Organization` | ❌     | ✅   | ❌     | ❌     |
| `Leader`       | ❌     | ✅   | ❌     | ❌     |
| `Member`       | ❌     | ✅   | ❌     | ❌     |

### User Story with Views (eg. Sally Student in CSSG)

As an authenticated member, Sally Student, in the `CS+Social Good` organization, I want to see the member roster from organization details page so that I can view other members and their basic information in this organization.

![image-20241209220020357](./assets/image-20241209220020357.png)

### Tech Specs

#### Frontend:

- `organization-card` widget: the card of a member is the same with others, except that the `apply` or `join` button disappears after checking with the backend that the current user is a member of the organization. The design choice is covered in the `Guest` section.
- `organization-details-info-card` widget: we update this card to include detailed information of members and leaders in the form of tables when the current user is a member. For those outside of the organization, this is not shown. For each organization and the current user, this is set by `isMemberFlag`. 
  - `checkIfMember`: note that the current backend does not expose API solely for checking membership, so the implementation calls `getOrganizationMembers` from frontend service and compare one by one, which leaves room for improvement. Note that if the current user is not a member, the service call will error out and return nothing, in which case we do not display the two tables above.
  - `collectLeaders` will collect leaders by calling `checkLeaderStatus` frontend service with each of the member. This can also be improved by efforts at the backend.

#### Backend Databases and Entities:

In addition to `OrganizationEntity` and `UserEntity`, members can access to `user_organization_table`, `PermissionEntity` and `RoleEntity` with `user_role_table`:

- `user_organization_table`: includes a user_organization table to be used as a join table to persist a `many-to-many` relationship between the `user` table and `organization` table
- `PermissionEntity`: includes `action`, `resource`, `users`, and `roles` to make sure the users with different roles have corresponding permissions
- `RoleEntity`: includes `users` and `permissions` to make sure the users with different roles have corresponding permissions
- `user_role_table`: matches a `many-to-many` relations between `user` table and `role` table

#### Backend Models:

- `Organization`: includes an `Organization` model based on `OrganizationEntity`
- `User`: includes a `User` model based on `UserEntity`
- `Role`: includes a `Role` model based on `RoleEntity`
- `Permission`: includes a `Permission` model based on `PermissionEntity`

#### Backend Services:

- `get_by_slug` in backend/services/organization: Gets the organization by a slug
- `get_all_users` in backend/services/user_organization: Gets the member roster of the organization by matching users of the same organization in `user_organization_table`
- `is_leader` in backend/services/user_organiztaion: Checks if the current registered user is a leader of the organization

#### Backend APIs:

- `GET /api/organizations/{slug}` to get the general details about this organization
- `GET /api/organizations/{slug}/members` to get the member roster of this organization
- `GET /api/organizations/{slug}/{onyen}/authleader` to get whether the user is the leader of this organization. This API is used to further get a leader roster which is open to public on organization details page.

## Leader

### Leader Permissions

| Services       | Create | Read | Update | Delete |
| -------------- | ------ | ---- | ------ | ------ |
| `Organization` | ❌     | ✅   | ✅     | ✅     |
| `Leader`       | ❌     | ✅   | ❌     | ✅     |
| `Member`       | ❌     | ✅   | ❌     | ✅     |

### User Story with Views (eg. Paul President in ACM)

As a leader (President), Paul President, in the ACM organization, I want to add other users to ACM so that they can have ACM membership and member-only permissions.

![image-20241209221220062](./assets/image-20241209221220062.png)

![image-20241209222421887](./assets/image-20241209222421887.png)

### Tech Specs

#### Frontend:

- `organization-card` calls frontend service `checkLeaderStatus` in `organization.service.ts`, which in turn calls backend APIs, to check if the current user is a leader for this organization. If so, a little gear will show up on the card.
- `organization-settings-dialog`: the main component where the leader manages the organization is implemented here, as shown above. After clicking "save", it will call `updateOrganization` frontend service to update information in the backend, including the information represented by the `toggle`. Currently we don't support updating Organization name because of limited time for a thorough testing. Also, we haven't implemented the `Applications` button logic, which will allow the leaders to approve or deny applications from students.
- The current way to manage membership is to directly add or remove using `Add/Delete Member` button. The logic is implemented in `add-member-dialog` widget.
  - After inputing the onyen and clicking `add` or `delete`, it will call `addMember` or `removeMember` in `organization.service.ts` frontend service. The backend API will check if this is a valid onyen in both cases and a snackbar will pop up to denote whether the operation is successful.

#### Backend Databases and Entities:

Same as `Member`

#### Backend Models:

Same as `Member`

#### Backend Services:

In addition to `get_by_slug`, `get_all_users` and `is_leader`, leaders can get access to:

- `add_membership` in backend/services/user_organization: Adds a user to an organization and allows the user with member role and permissions in this organization, which checks the permission first.
- `remove_membership` in backend/services/user_organization: Removes a user from an organizatio, which checks the permission first.
- `update` in backend/services/organization: Update the organization information, which checks the permission first.

#### Backend APIs:

In addition to `GET /api/organizations/{slug}`, `GET /api/organizations/{slug}/members`, and `GET /api/organizations/{slug}/{onyen}/authleader`, leaders have:

- `POST /api/organizations/{slug}/add_membership/{onyen}`: add new members to the organization and throws exceptions if no permission or no resource exists
- `DELETE /api/organizations/{slug}/remove_membership/{onyen}`: remove members from the organization and throws exceptions if no permission or no resource exists
- `PUT /api/organizations/{slug}`: updates the organizaton information by slug and throws exceptions if no permission or no resource exists

## Admin (root)

### Admin Permissions

| Services       | Create | Read | Update | Delete |
| -------------- | ------ | ---- | ------ | ------ |
| `Organization` | ✅     | ✅   | ✅     | ✅     |
| `Leader`       | ✅     | ✅   | ✅     | ✅     |
| `Member`       | ✅     | ✅   | ✅     | ✅     |

### Admin Frontend Views

#### Original Interface

![image-20241122145640821](./assets/image-20241122145640821.png)

#### Current Interface

![image-20241209222854446](./assets/image-20241209222854446.png)

Rhonda the root is currently not a member of any organization (and thus the `Apply/Join` button, but has leader permission to all organizations (and thus the little gears in each card). Please refer to previous sections for each of these features (both backend and frontend).
