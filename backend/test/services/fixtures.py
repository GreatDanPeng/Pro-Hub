"""Fixtures used for testing the core services."""

import pytest
from unittest.mock import create_autospec
from sqlalchemy.orm import Session
from ...services import (
    PermissionService,
    UserService,
    RoleService,
    OrganizationService,
    EventService,
    RoomService,
    ApplicationService,
)
from ...services.user_organization import UserOrgService
from ...services.academics import HiringService
from ...services.article import ArticleService
from ...services.coworking import PolicyService, OperatingHoursService

__authors__ = ["Kris Jordan", "Ajay Gandecha"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


@pytest.fixture()
def permission_svc(session: Session):
    return PermissionService(session)


@pytest.fixture()
def permission_svc_mock():
    """This mocks the PermissionService class to avoid testing its implementation here."""
    return create_autospec(PermissionService)


@pytest.fixture()
def user_svc(session: Session, permission_svc_mock: PermissionService):
    """This fixture is used to test the UserService class with a mocked PermissionService."""
    return UserService(session, permission_svc_mock)


@pytest.fixture()
def user_svc_integration(session: Session):
    """This fixture is used to test the UserService class with a real PermissionService."""
    return UserService(session, PermissionService(session))


@pytest.fixture()
def user_org_svc_integration(session: Session):
    """This fixture is used to test the UserOrganizationService class with a real PermissionService."""
    return UserOrgService(session, PermissionService(session))


@pytest.fixture()
def role_svc(session: Session, permission_svc_mock: PermissionService):
    return RoleService(session, permission_svc_mock)


@pytest.fixture()
def organization_svc_integration(session: Session):
    """This fixture is used to test the OrganizationService class with a real PermissionService."""
    return OrganizationService(session, PermissionService(session))


@pytest.fixture()
def event_svc_integration(session: Session, user_svc_integration: UserService):
    """This fixture is used to test the EventService class with a real PermissionService."""
    return EventService(session, PermissionService(session))


@pytest.fixture()
def room_svc(session: Session):
    """RoomService fixture."""
    return RoomService(session, PermissionService(session))


@pytest.fixture()
def article_svc(session: Session):
    return ArticleService(
        session,
        PermissionService(session),
        PolicyService(),
        OperatingHoursService(session, PermissionService(session)),
    )


@pytest.fixture()
def application_svc(session: Session):
    """ApplicationService fixture."""
    return ApplicationService(session, PermissionService(session))
