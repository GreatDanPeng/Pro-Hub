"""Mock data for users.

Three users are setup for testing and development purposes:

1. Rhonda Root (root user with all permissions)
2. Amy Ambassador (staff of XL with elevated permissions)
3. Sally Student (standard user without any special permissions)
4. Ina Instructor
5. Uhlissa UTA
6. Stewie Student
7. Lambda Leader (leader of CSSG)
8. Paul President (president of ACM)
"""

import pytest
from sqlalchemy.orm import Session

from ...entities.organization_entity import OrganizationEntity
from ...models.user import User
from ...entities.user_entity import UserEntity
from ...entities.user_role_table import user_role_table
from ...entities.user_organization_table import user_organization_table
from .reset_table_id_seq import reset_table_id_seq
from . import role_data
from .role_data import root_role, ambassador_role, cssg_leader_role, acm_leader_role
from .organization.organization_demo_data import acm, cssg

# how to import organization_demo_data
from ...test.services.organization import organization_test_data, organization_demo_data

__authors__ = ["Dan Peng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

root = User(
    id=1,
    pid=999999999,
    onyen="root",
    email="root@unc.edu",
    first_name="Rhonda",
    last_name="Root",
    pronouns="She / Her / Hers",
    accepted_community_agreement=True,
)

ambassador = User(
    id=2,
    pid=888888888,
    onyen="xlstan",
    email="amam@unc.edu",
    first_name="Amy",
    last_name="Ambassador",
    pronouns="They / Them / Theirs",
    accepted_community_agreement=True,
)

# user in CSSG
user = User(
    id=3,
    pid=111111111,
    onyen="user",
    email="user@unc.edu",
    first_name="Sally",
    last_name="Student",
    pronouns="She / They",
    accepted_community_agreement=True,
)

instructor = User(
    id=4,
    pid=222222222,
    onyen="ina",
    email="ina@unc.edu",
    first_name="Ina",
    last_name="Instructor",
    pronouns="They / Them / Theirs",
    accepted_community_agreement=True,
)

uta = User(
    id=5,
    pid=333333333,
    onyen="uhlissa",
    email="uhlissa@unc.edu",
    first_name="Uhlissa",
    last_name="UTA",
    pronouns="They / Them / Theirs",
    accepted_community_agreement=True,
)

# Another Student
student = User(
    id=6,
    pid=555555555,
    onyen="stewie",
    email="stewie@unc.edu",
    first_name="Stewie",
    last_name="Student",
    pronouns="They / Them / Theirs",
    accepted_community_agreement=True,
)

# Leader in CSSG
leader = User(
    id=7,
    pid=777777777,
    onyen="lambda",
    email="leader@unc.edu",
    first_name="Lambda",
    last_name="Leader",
    pronouns="He / Him / His",
    accepted_community_agreement=True,
)

# President in ACM
president = User(
    id=8,
    pid=444444444,
    onyen="paul",
    email="paul@unc.edu",
    first_name="Paul",
    last_name="President",
    pronouns="He / Him / His",
    accepted_community_agreement=True,
)

users = [root, ambassador, user, instructor, uta, student, leader, president]

roles_users = {
    role_data.root_role.id: [root],
    role_data.ambassador_role.id: [ambassador],
    role_data.cssg_leader_role.id: [leader],
    role_data.acm_leader_role.id: [president],
    role_data.cssg_member_role.id: [user],
    role_data.acm_member_role.id: [uta],
}

## For final pre, we need to use organization_demo_data
organization_users = {
    organization_demo_data.cssg.id: [user, leader],
    organization_demo_data.acm.id: [president, uta],
}


def insert_fake_data(session: Session):
    roles = session.query(role_data.RoleEntity).all()
    organizations = session.query(organization_demo_data.OrganizationEntity).all()
    print(f"Roles: {[role.id for role in roles]}")
    print(f"Inserted organizations: {[org.id for org in organizations]}")

    global users
    entities = []
    for user in users:
        entity = UserEntity.from_model(user)
        session.add(entity)
        entities.append(entity)
    reset_table_id_seq(session, UserEntity, UserEntity.id, len(users) + 1)
    session.commit()  # Commit to ensure User IDs in database

    # Associate Users with the Role(s) they are in
    for role_id, members in roles_users.items():
        for user in members:
            session.execute(
                user_role_table.insert().values(
                    {"role_id": role_id, "user_id": user.id}
                )
            )
    session.commit()

    # # # # Debug: FK doesn't match
    for organization, members in organization_users.items():
        print(
            f"Inserting organization_id={organization} with members {[user.id for user in members]}"
        )
        for user in members:
            session.execute(
                user_organization_table.insert().values(
                    {"organization_id": organization, "user_id": user.id}
                )
            )
    session.commit()


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    insert_fake_data(session)
    session.commit()
    yield
