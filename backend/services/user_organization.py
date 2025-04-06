"""
The User Organizations Service allows the API to manipulate user_organizations data in the database.
"""

from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.organization import Organization
from ..entities.user_organization_table import user_organization_table
from ..entities.user_role_table import user_role_table
from ..models import User
from ..entities import RoleEntity, UserEntity, OrganizationEntity
from .permission import PermissionService


__authors__ = ["Dan Peng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class UserOrgService:
    """Service that performs all of the actions on the `User_Organization` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `UserOrganizationService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission

    def get_all_users(self, subject: User, organization: Organization) -> list[User]:
        """
        Retrieves all users associated with a given organization

        Parameters:
            organization (Organization): Organization to retrieve users from

        Returns:
            list[User]: List of all users associated with the organization
        """
        self._permission.enforce(
            subject, "organization.get_all_users", f"organization/{organization.slug}"
        )

        # Query the organization with matching name
        users = (
            self._session.query(UserEntity)
            .join(user_organization_table)
            .filter(user_organization_table.c.organization_id == organization.id)
            .all()
        )

        return [user.to_model() for user in users]

    def is_leader(self, subject: User, organization: Organization) -> bool:
        """
        Checks if the current registered user is a leader of the organization

        Parameters:
            organization (Organization): Organization to check if the user is a leader of

        Returns:
            bool: True if the user is a leader of the organization, False otherwise
        """

        if self._permission.check(
            subject, "organization.update", f"organization/{organization.slug}"
        ):
            return True
        return False

    def add_membership(
        self, subject: User, user: User, organization: Organization
    ) -> bool:
        """
        Adds a user to an organization

        Context: when a user is added to an organization, the user is given the member permissions of the organization and the user is added to the user_organization table

        Parameters:
            subject (User): The user adding the user to the organization
            user (User): User to add to the organization
            organization (Organization): Organization to add the user to
        """
        ## Check if the subject has permission to add a user to the organization
        self._permission.enforce(
            subject, "organization.add_membership", f"organization/{organization.slug}"
        )

        try:
            # Check if the user exists and add the user to the organization
            if user:
                self._session.execute(
                    user_organization_table.insert().values(
                        user_id=user.id, organization_id=organization.id
                    )
                )
                # grant the user with the member role (cssg_members or acm_members)
                # if the user is added to the member role, the user will have the permissions of the member role
                if organization.slug == "cssg":
                    member_role = (
                        self._session.query(RoleEntity)
                        .filter(RoleEntity.name == "cssg_members")
                        .first()
                    )
                elif organization.slug == "acm":
                    member_role = (
                        self._session.query(RoleEntity)
                        .filter(RoleEntity.name == "acm_members")
                        .first()
                    )
                self._session.execute(
                    user_role_table.insert().values(
                        user_id=user.id, role_id=member_role.id
                    )
                )
                self._session.commit()
                return True
            else:
                print("User does not exist.")
                self._session.rollback()
                return False

        except Exception as e:
            print(f"Error adding user to organization: {e}")
            self._session.rollback()
            return False

    def remove_membership(
        self, subject: User, user: User, organization: Organization
    ) -> bool:
        """
        Removes a user from an organization

        Parameters:
            user (User): User to remove from the organization
            organization (Organization): Organization to remove the user from
        """
        ## Check if the subject has permission to add a user to the organization
        self._permission.enforce(
            subject,
            "organization.remove_membership",
            f"organization/{organization.slug}",
        )

        try:
            # Check if the user exists and add the user to the organization
            if user:
                self._session.execute(
                    user_organization_table.delete().where(
                        user_organization_table.c.user_id == user.id,
                        user_organization_table.c.organization_id == organization.id,
                    )
                )

                # revoke the user from the member role (cssg_members or acm_members)
                if organization.slug == "cssg":
                    member_role = (
                        self._session.query(RoleEntity)
                        .filter(RoleEntity.name == "cssg_members")
                        .first()
                    )
                elif organization.slug == "acm":
                    member_role = (
                        self._session.query(RoleEntity)
                        .filter(RoleEntity.name == "acm_members")
                        .first()
                    )
                self._session.execute(
                    user_role_table.delete().where(
                        user_role_table.c.user_id == user.id,
                        user_role_table.c.role_id == member_role.id,
                    )
                )

                self._session.commit()
                return True
            else:
                print("User does not exist.")
                self._session.rollback()
                return False

        except Exception as e:
            print(f"Error removing user to organization: {e}")
            self._session.rollback()
            return False
