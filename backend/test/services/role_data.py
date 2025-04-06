"""Mock data for specific roles.

Two roles are setup for testing and development purposes:

1. root (will have sudo permissions to do everything)
2. ambassador (will have a subset of specific permissions)
3. cssg_leader (will have a subset of specific permissions)
4. acm_leader (will have a subset of specific permissions)
5. cssg_member (will have a subset of specific permissions)
6. acm_member (will have a subset of specific permissions)
"""

import pytest
from sqlalchemy.orm import Session
from .reset_table_id_seq import reset_table_id_seq
from ...entities.role_entity import RoleEntity
from ...models.role import Role

__authors__ = ["Dan Peng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

root_role = Role(id=1, name="root")
ambassador_role = Role(id=2, name="ambassadors")
cssg_leader_role = Role(id=3, name="cssg_leaders")
acm_leader_role = Role(id=4, name="acm_leaders")
cssg_member_role = Role(id=5, name="cssg_members")
acm_member_role = Role(id=6, name="acm_members")

roles = [
    root_role,
    ambassador_role,
    acm_leader_role,
    cssg_leader_role,
    cssg_member_role,
    acm_member_role,
]


def insert_fake_data(session: Session):
    for role in roles:
        entity = RoleEntity.from_model(role)
        session.add(entity)

    reset_table_id_seq(session, RoleEntity, RoleEntity.id, len(roles) + 1)
    session.commit()
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
