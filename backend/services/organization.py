"""
The Organizations Service allows the API to manipulate organizations data in the database.
"""

from fastapi import Depends
from sqlalchemy import String, select
from sqlalchemy.orm import Session

from ..database import db_session
from ..models.organization import Organization
from ..models.organization_details import OrganizationDetails
from ..entities.organization_entity import OrganizationEntity
from ..models import User
from .permission import PermissionService

from .exceptions import ResourceNotFoundException


__authors__ = ["Dan Peng", "Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


class OrganizationService:
    """Service that performs all of the actions on the `Organization` table"""

    def __init__(
        self,
        session: Session = Depends(db_session),
        permission: PermissionService = Depends(),
    ):
        """Initializes the `OrganizationService` session, and `PermissionService`"""
        self._session = session
        self._permission = permission

    # Waiting to be fixed but doesn't affect the overall functionality
    def get(self, name: str) -> Organization:
        """
        Get the organization from a name
        If none retrieved, a debug description is displayed.

        Parameters:
            name: a string representing a unique organization name

        Returns:
            Organization: Object with corresponding name

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding name
        """

        # Query the organization with matching name
        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.name == name)
            .one_or_none()
        )

        # Check if result is null
        if organization is None:
            raise ResourceNotFoundException(
                f"No organization found with matching name: {name}"
            )

        return organization

    def all(self) -> list[Organization]:
        """
        Retrieves all organizations from the table

        Returns:
            list[Organization]: List of all `Organization`
        """
        # Select all entries in `Organization` table
        entities = self._session.query(OrganizationEntity).all()
        # Convert entries to a model and return
        print("line76: ", [entity.to_model() for entity in entities])
        return [entity.to_model() for entity in entities]

    def create(self, subject: User, organization: Organization) -> Organization:
        """
        Creates a organization based on the input object and adds it to the table.
        If the organization's ID is unique to the table, a new entry is added.
        If the organization's ID already exists in the table, it raises an error.

        Parameters:
            subject: a valid User model representing the currently logged in User
            organization (Organization): Organization to add to table

        Returns:
            Organization: Object added to table
        """

        # Check if user has admin permissions
        self._permission.enforce(subject, "organization.create", f"organization")

        # Checks if the organization already exists in the table
        if organization.id:
            # Set id to None so database can handle setting the id
            organization.id = None

        # Otherwise, create new object
        organization_entity = OrganizationEntity.from_model(organization)

        # Add new object to table and commit changes
        self._session.add(organization_entity)
        self._session.commit()

        # Return added object
        return organization_entity.to_model()

    def get_by_slug(self, slug: str) -> OrganizationDetails:
        """
        Get the organization from a slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique organization slug

        Returns:
            Organization: Object with corresponding slug

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding slug
        """

        # Query the organization with matching slug
        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == slug)
            .one_or_none()
        )

        # Check if result is null
        if organization is None:
            raise ResourceNotFoundException(
                f"No organization found with matching slug: {slug}"
            )

        return organization.to_details_model()

    def get_status_by_slug(self, slug: str) -> String:
        """
        Get the status of organization by slug
        If none retrieved, a debug description is displayed.

        Parameters:
            slug: a string representing a unique organization name

        Returns:
            public: the status of the organization

        Raises:
            ResourceNotFoundException if no organization is found with the corresponding name
        """
        organization = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == slug)
            .one_or_none()
        )

        if organization is None:
            raise ResourceNotFoundException(
                f"No organization found with matching slug: {slug}"
            )

        return organization.public

    def update(self, subject: User, organization: Organization) -> Organization:
        """
        Update the organization
        If none found with that id, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            organization (Organization): Organization to add to table

        Returns:
            Organization: Updated organization object

        Raises:
            ResourceNotFoundException: If no organization is found with the corresponding ID
        """

        # Check if user has admin permissions
        self._permission.enforce(
            subject, "organization.update", f"organization/{organization.slug}"
        )

        # Query the organization with matching id
        obj = (
            self._session.get(OrganizationEntity, organization.id)
            if organization.id
            else None
        )

        # Check if result is null
        if obj is None:
            raise ResourceNotFoundException(
                f"No organization found with matching ID: {organization.id}"
            )

        # Update organization object
        obj.name = organization.name
        obj.shorthand = organization.shorthand
        obj.slug = organization.slug
        obj.logo = organization.logo
        obj.short_description = organization.short_description
        obj.long_description = organization.long_description
        obj.website = organization.website
        obj.email = organization.email
        obj.instagram = organization.instagram
        obj.linked_in = organization.linked_in
        obj.youtube = organization.youtube
        obj.heel_life = organization.heel_life
        obj.public = organization.public
        obj.application_required = organization.application_required

        # Save changes
        self._session.commit()

        # Return updated object
        return obj.to_model()

    def delete(self, subject: User, slug: str) -> None:
        """
        Delete the organization based on the provided slug.
        If no item exists to delete, a debug description is displayed.

        Parameters:
            subject: a valid User model representing the currently logged in User
            slug: a string representing a unique organization slug

        Raises:
            ResourceNotFoundException: If no organization is found with the corresponding slug
        """
        # Check if user has admin permissions
        self._permission.enforce(subject, "organization.delete", f"organization")

        # Find object to delete
        obj = (
            self._session.query(OrganizationEntity)
            .filter(OrganizationEntity.slug == slug)
            .one_or_none()
        )

        # Ensure object exists
        if obj is None:
            raise ResourceNotFoundException(
                f"No organization found with matching slug: {slug}"
            )

        # Delete object and commit
        self._session.delete(obj)
        # Save changes
        self._session.commit()
