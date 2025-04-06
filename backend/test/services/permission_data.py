"""Mock data for permissions in the system."""

import pytest
from sqlalchemy.orm import Session
from ...entities.permission_entity import PermissionEntity

from ...models.permission import Permission

from . import role_data
from .reset_table_id_seq import reset_table_id_seq

__authors__ = ["Dan Peng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

root_role_permission = Permission(id=1, action="*", resource="*")
ambassador_checkin_create_permission = Permission(
    id=2, action="checkin.create", resource="checkin"
)
ambassador_coworking_reservation_permission = Permission(
    id=3, action="coworking.reservation.*", resource="*"
)
cssg_leader_update_permission = Permission(
    id=4, action="organization.update", resource="organization/cssg"
)
cssg_leader_add_membership_permission = Permission(
    id=5, action="organization.add_membership", resource="organization/cssg"
)
cssg_leader_remove_membership_permission = Permission(
    id=6, action="organization.remove_membership", resource="organization/cssg"
)
cssg_leader_get_all_users_permission = Permission(
    id=7, action="organization.get_all_users", resource="organization/cssg"
)
acm_leader_update_permission = Permission(
    id=8, action="organization.update", resource="organization/acm"
)
acm_leader_add_membership_permission = Permission(
    id=9, action="organization.add_membership", resource="organization/acm"
)
acm_leader_remove_membership_permission = Permission(
    id=10, action="organization.remove_membership", resource="organization/acm"
)
acm_leader_get_all_users_permission = Permission(
    id=11, action="organization.get_all_users", resource="organization/acm"
)
cssg_member_get_all_users_permission = Permission(
    id=12, action="organization.get_all_users", resource="organization/cssg"
)
acm_member_get_all_users_permission = Permission(
    id=13, action="organization.get_all_users", resource="organization/acm"
)

ambassador_permission = [
    ambassador_checkin_create_permission,
    ambassador_coworking_reservation_permission,
]
cssg_leader_permission = [
    cssg_leader_update_permission,
    cssg_leader_add_membership_permission,
    cssg_leader_remove_membership_permission,
    cssg_leader_get_all_users_permission,
]
acm_leader_permission = [
    acm_leader_update_permission,
    acm_leader_add_membership_permission,
    acm_leader_remove_membership_permission,
    acm_leader_get_all_users_permission,
]
cssg_member_permissions = [cssg_member_get_all_users_permission]
acm_member_permissions = [acm_member_get_all_users_permission]


def insert_fake_data(session: Session):
    root_permission_entity = PermissionEntity(
        id=root_role_permission.id,
        role_id=role_data.root_role.id,
        action=root_role_permission.action,
        resource=root_role_permission.resource,
    )
    session.add(root_permission_entity)

    for i in range(len(ambassador_permission)):
        ambassador_permission_entity = PermissionEntity(
            id=ambassador_permission[i].id,
            role_id=role_data.ambassador_role.id,
            action=ambassador_permission[i].action,
            resource=ambassador_permission[i].resource,
        )
        session.add(ambassador_permission_entity)

    for i in range(len(cssg_leader_permission)):
        cssg_leader_permission_entity = PermissionEntity(
            id=cssg_leader_permission[i].id,
            role_id=role_data.cssg_leader_role.id,
            action=cssg_leader_permission[i].action,
            resource=cssg_leader_permission[i].resource,
        )
        session.add(cssg_leader_permission_entity)

    for i in range(len(acm_leader_permission)):
        acm_leader_permission_entity = PermissionEntity(
            id=acm_leader_permission[i].id,
            role_id=role_data.acm_leader_role.id,
            action=acm_leader_permission[i].action,
            resource=acm_leader_permission[i].resource,
        )
        session.add(acm_leader_permission_entity)

    for i in range(len(cssg_member_permissions)):
        cssg_member_permission_entity = PermissionEntity(
            id=cssg_member_permissions[i].id,
            role_id=role_data.cssg_member_role.id,
            action=cssg_member_permissions[i].action,
            resource=cssg_member_permissions[i].resource,
        )
        session.add(cssg_member_permission_entity)

    for i in range(len(acm_member_permissions)):
        acm_member_permission_entity = PermissionEntity(
            id=acm_member_permissions[i].id,
            role_id=role_data.acm_member_role.id,
            action=acm_member_permissions[i].action,
            resource=acm_member_permissions[i].resource,
        )
        session.add(acm_member_permission_entity)

    reset_table_id_seq(
        session,
        PermissionEntity,
        PermissionEntity.id,
        len(ambassador_permission)
        + len(acm_leader_permission)
        + len(cssg_leader_permission)
        + len(cssg_member_permissions)
        + len(acm_member_permissions)
        + 2,
    )


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
