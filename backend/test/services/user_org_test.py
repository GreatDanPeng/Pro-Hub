"""Tests for the UserOrganizationService class.

organization_users = {
    organization_test_data.cssg.id: [user, leader],
    organization_test_data.acm.id: [president, uta],
}

"""

import pytest

# Tested Dependencies
from ...models.user import User, NewUser
from ...models.pagination import PaginationParams
from ...services import UserService, PermissionService
from ...services.user_organization import UserOrgService
from ...services.exceptions import ResourceNotFoundException, UserPermissionException

# Data Setup and Injected Service Fixtures
from .core_data import setup_insert_data_fixture
from .fixtures import user_svc, user_org_svc_integration, permission_svc

# Data Models for Fake Data Inserted in Setup
from .user_data import root, ambassador, user, president, leader, student, uta
from .organization import organization_test_data
from . import user_data

__authors__ = ["Dan Peng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


def test_leader_get_all_users_acm(user_org_svc_integration: UserOrgService):
    users = user_org_svc_integration.get_all_users(root, organization_test_data.acm)
    assert len(users) == 2
    # check whether the president is in the list of users
    assert user_data.president in users


def test_leader_get_all_users_cssg(user_org_svc_integration: UserOrgService):
    users = user_org_svc_integration.get_all_users(root, organization_test_data.cssg)
    print("user list:", users)
    # check whether the president is in the list of users
    assert user_data.leader in users


# organization_test_data.cssg.id: [user, leader]
def test_member_get_all_users_cssg(user_org_svc_integration: UserOrgService):
    users = user_org_svc_integration.get_all_users(user, organization_test_data.cssg)
    print("user list:", users)
    # check whether the president is in the list of users
    assert user_data.user in users
    assert user_data.leader in users


# organization_test_data.acm.id: [president, uta]
def test_member_get_all_users_acm(user_org_svc_integration: UserOrgService):
    users = user_org_svc_integration.get_all_users(uta, organization_test_data.acm)
    print("user list:", users)
    # check whether the president is in the list of users
    assert user_data.uta in users
    assert user_data.president in users


def test_guest_not_get_all_users_cssg(user_org_svc_integration: UserOrgService):
    with pytest.raises(UserPermissionException):
        user_org_svc_integration.get_all_users(student, organization_test_data.cssg)
        pytest.fail()


# Test president of acm to add new member student to acm
def test_leader_add_new_member_to_acm(
    permission_svc: PermissionService, user_org_svc_integration: UserOrgService
):
    assert (
        user_org_svc_integration.add_membership(
            president, student, organization_test_data.acm
        )
        is True
    )
    user_org_svc_integration.add_membership(
        president, student, organization_test_data.acm
    )
    users = user_org_svc_integration.get_all_users(
        president, organization_test_data.acm
    )
    assert len(users) == 3
    # check the student has the member permission
    assert (
        permission_svc.check(student, "organization.get_all_users", "organization/acm")
        is True
    )


# Test Leader of cssg to add new member student to cssg
def test_leader_add_new_member_to_cssg(
    permission_svc: PermissionService, user_org_svc_integration: UserOrgService
):
    assert (
        user_org_svc_integration.add_membership(
            leader, student, organization_test_data.cssg
        )
        is True
    )
    user_org_svc_integration.add_membership(
        leader, student, organization_test_data.cssg
    )
    users = user_org_svc_integration.get_all_users(leader, organization_test_data.cssg)
    assert len(users) == 3
    # check the student has the member permission
    assert (
        permission_svc.check(student, "organization.get_all_users", "organization/cssg")
        is True
    )


def test_guest_not_add_new_member_to_cssg(user_org_svc_integration: UserOrgService):
    with pytest.raises(UserPermissionException):
        user_org_svc_integration.add_membership(
            student, ambassador, organization_test_data.cssg
        )
        pytest.fail()


def test_member_not_add_new_member_to_cssg(user_org_svc_integration: UserOrgService):
    with pytest.raises(UserPermissionException):
        user_org_svc_integration.add_membership(
            user, ambassador, organization_test_data.cssg
        )
        pytest.fail()


def test_add_exist_member_to_acm(user_org_svc_integration: UserOrgService):
    user_org_svc_integration.add_membership(root, student, organization_test_data.acm)
    user_org_svc_integration.add_membership(root, student, organization_test_data.acm)
    users = user_org_svc_integration.get_all_users(root, organization_test_data.acm)
    assert len(users) == 3
    assert (student in users) is True


def test_remove_member_from_cssg(
    permission_svc: PermissionService, user_org_svc_integration: UserOrgService
):
    # first add user to acm
    user_org_svc_integration.add_membership(root, student, organization_test_data.cssg)
    users = user_org_svc_integration.get_all_users(root, organization_test_data.cssg)
    assert len(users) == 3
    # then remove user from acm
    user_org_svc_integration.remove_membership(
        root, student, organization_test_data.cssg
    )
    users = user_org_svc_integration.get_all_users(root, organization_test_data.cssg)
    assert len(users) == 2

    # check whether the user is not in the list of users
    assert (student in users) is False
    # check the student does not have the member permission
    assert (
        permission_svc.check(student, "organization.get_all_users", "organization/cssg")
        is False
    )


def test_add_new_member_to_cssg(
    permission_svc: PermissionService, user_org_svc_integration: UserOrgService
):
    user_org_svc_integration.add_membership(
        leader, student, organization_test_data.cssg
    )
    users = user_org_svc_integration.get_all_users(root, organization_test_data.cssg)
    assert len(users) == 3

    # check the student has the member permission
    assert (
        permission_svc.check(student, "organization.get_all_users", "organization/cssg")
        is True
    )


def test_is_leader_cssg(user_org_svc_integration: UserOrgService):
    assert (
        user_org_svc_integration.is_leader(leader, organization_test_data.cssg) is True
    )


def test_is_leader_acm(user_org_svc_integration: UserOrgService):
    assert (
        user_org_svc_integration.is_leader(president, organization_test_data.acm)
        is True
    )


def test_not_leader_cssg(user_org_svc_integration: UserOrgService):
    assert (
        user_org_svc_integration.is_leader(student, organization_test_data.cssg)
        is False
    )
