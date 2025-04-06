"""Tests for the OrganizationService class."""

# PyTest
import pytest
from unittest.mock import create_autospec

from ...services.exceptions import UserPermissionException, ResourceNotFoundException

# Injected Service Fixtures
from .fixtures import application_svc

# Tested Dependencies
from ...models.user import User, NewUser
from ...models.pagination import PaginationParams
from ...services import UserService, PermissionService
from ...services.organization_application import OrganizationApplicationService
from ...services.user_organization import UserOrgService
from ...services.exceptions import ResourceNotFoundException

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import user_svc, user_org_svc_integration, permission_svc

# Data Models for Fake Data Inserted in Setup
from .user_data import root, ambassador, user, president, leader, student
from .organization import organization_test_data
from . import user_data

__authors__ = ["Dan Peng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


# Test Functions
def test_get_all_applications_acm(org_application_svc: OrganizationApplicationService):
    application = org_application_svc.get_user_application(
        organization_test_data.cssg.id, student
    )
    assert len(application) == 1
