"""Organization API

Organization routes are used to create, retrieve, and update Organizations."""

from fastapi import APIRouter, Depends, HTTPException, logger

from backend.services.user import UserService

from ..services import OrganizationService, RoleService, UserPermissionException
from ..models.organization import Organization
from ..services.user_organization import UserOrgService
from ..models.organization_details import OrganizationDetails
from ..api.authentication import registered_user
from ..models.user import User
import logging

__authors__ = ["Dan Peng", "Ajay Gandecha", "Jade Keegan", "Brianna Ta", "Audrey Toney"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

api = APIRouter(prefix="/api/organizations")
openapi_tags = {
    "name": "Organizations",
    "description": "Create, update, delete, and retrieve CS Organizations.",
}


@api.get("", response_model=list[Organization], tags=["Organizations"])
def get_organizations(
    organization_service: OrganizationService = Depends(),
) -> list[Organization]:
    """
    Get all organizations

    Parameters:
        organization_service: a valid OrganizationService

    Returns:
        list[Organization]: All `Organization`s in the `Organization` database table
    """

    # Return all organizations
    try:
        return organization_service.all()
    except Exception as e:
        logger.error(f"Error fetching organizations: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


@api.post("", response_model=Organization, tags=["Organizations"])
def new_organization(
    organization: Organization,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
    role_service: RoleService = Depends(),
) -> Organization:
    """
    Create organization

    Parameters:
        organization: a valid Organization model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        Organization: Created organization

    Raises:
        HTTPException 403 if create() raises a UserPermissionException
        HTTPException 422 if create() raises an Exception
    """
    try:
        new_organization = organization_service.create(subject, organization)
        # Create a new role for the organization newly created
        role_service.create(subject, new_organization.slug)
        return new_organization
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=422, detail=str(e))


@api.get(
    "/{slug}",
    response_model=OrganizationDetails,
    tags=["Organizations"],
)
def get_organization_by_slug(
    slug: str, organization_service: OrganizationService = Depends()
) -> OrganizationDetails:
    """
    Get organization with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        organization_service: a valid OrganizationService

    Returns:
        Organization: Organization with matching slug

    Raises:
        HTTPException 404 if get_by_slug() raises an Exception
    """
    try:
        return organization_service.get_by_slug(slug)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get(
    "/{slug}/status",
    response_model=str,
    tags=["Organizations"],
)
def get_organization_status_by_slug(
    slug: str, organization_service: OrganizationService = Depends()
) -> str:
    """
    Get organization status with matching slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        organization_service: a valid OrganizationService

    Returns:
        str: Status of the organization with matching slug

    Raises:
        HTTPException 404 if get_by_slug() raises an Exception
    """
    try:
        return organization_service.get_status_by_slug(slug)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.put(
    "/{slug}",
    response_model=Organization,
    tags=["Organizations"],
)
def update_organization(
    organization: Organization,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
) -> Organization:
    """
    Update organization

    Parameters:
        organization: a valid Organization model
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Returns:
        Organization: Updated organization

    Raises:
        HTTPException 403 if update() raises a UserPermissionException
        HTTPException 404 if update() raises an Exception
    """
    try:
        return organization_service.update(subject, organization)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.delete("/{slug}", response_model=None, tags=["Organizations"])
def delete_organization(
    slug: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
):
    """
    Delete organization based on slug

    Parameters:
        slug: a string representing a unique identifier for an Organization
        subject: a valid User model representing the currently logged in User
        organization_service: a valid OrganizationService

    Raises:
        HTTPException 403 if delete() raises a UserPermission
        HTTPException 403 if delete() raises a UserPermission
        HTTPException 404 if delete() raises an Exception
    """
    try:
        organization_service.delete(subject, slug)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/{slug}/{onyen}/authleader", response_model=bool, tags=["Organizations"])
def is_leader(
    slug: str,
    onyen: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
    user_service: UserService = Depends(),
    user_org_service: UserOrgService = Depends(),
):
    """
    Check if the current registered user is a leader of the organization

    Parameters:
        organization: Organization to check if the user is a leader of
        subject: a valid User model representing the currently logged in User
        user_org_service: a valid UserOrgService

    Returns:
        bool: True if the user is a leader of the organization, False otherwise

    Raises:
        HTTPException 403 if is_leader() raises a UserPermissionException
        HTTPException 404 if is_leader() raises an Exception
    """
    try:
        organization = organization_service.get_by_slug(slug)
        user = user_service.get_by_onyen(subject, onyen)
        if not organization:
            raise HTTPException(status_code=404, detail="Organization not found")
        return user_org_service.is_leader(user, organization)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@api.get("/{slug}/members", response_model=list[User], tags=["Organizations"])
def get_organization_members(
    slug: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
    user_org_service: UserOrgService = Depends(),
):
    """
    Get all members of an organization

    Parameters:
        organization: a valid Organization model
        user_org_service: a valid UserOrgService

    Returns:
        list[User]: All users in the organization
    """
    organization = organization_service.get_by_slug(slug)
    return user_org_service.get_all_users(subject, organization)


@api.post("/{slug}/add_membership/{onyen}", response_model=bool, tags=["Organizations"])
def add_member_to_organization(
    slug: str,
    onyen: str,
    subject: User = Depends(registered_user),
    organization_service: OrganizationService = Depends(),
    user_service: UserService = Depends(),
    user_org_service: UserOrgService = Depends(),
):
    """
    Add a user to an organization

    Parameters:
        subject: a valid User model representing the currently logged in User
        user: a valid User model to add to the organization
        organization: a valid Organization model to add the user to
        user_org_service: a valid UserOrgService

    Raises:
        HTTPException 403 if add_membership() raises a UserPermissionException
        HTTPException 404 if add_membership() raises an Exception
    """
    try:
        organization = organization_service.get_by_slug(slug)
        user = user_service.get_by_onyen(subject, onyen)
        if not organization or not user:
            raise HTTPException(
                status_code=404, detail="Organization or User not found"
            )
        return user_org_service.add_membership(subject, user, organization)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=405, detail=str(e))


@api.delete(
    "/{slug}/remove_membership/{onyen}", response_model=bool, tags=["Organizations"]
)
def remove_member_from_organization(
    slug: str,
    onyen: str,
    subject: User = Depends(registered_user),
    user_service: UserService = Depends(),
    organization_service: OrganizationService = Depends(),
    user_org_service: UserOrgService = Depends(),
):
    """
    Remove a user from an organization

    Parameters:
        subject: a valid User model representing the currently logged in User
        user: a valid User model to add to the organization
        organization: a valid Organization model to add the user to
        user_org_service: a valid UserOrgService

    Raises:
        HTTPException 403 if remove_membership() raises a UserPermissionException
        HTTPException 404 if remove_membership() raises an Exception
    """
    try:
        organization = organization_service.get_by_slug(slug)
        user = user_service.get_by_onyen(subject, onyen)
        if not organization or not user:
            raise HTTPException(
                status_code=404, detail="Organization or User not found"
            )
        return user_org_service.remove_membership(subject, user, organization)
    except UserPermissionException as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=405, detail=str(e))
