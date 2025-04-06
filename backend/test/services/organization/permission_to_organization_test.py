"""These tests are used to ensure that the methods in ...services/organization are functioning with permissions as intended.

Each method contains detialed inline comments to help developers understand what is being tested, as well as why.

To run these tests, navigate to the root directory and run `pytest` in the terminal:

Run the following command in the terminal and get 100% coverage:
pytest -cov=/workspace/backend/services/organization.py /workspace/backend/test/services/organization/permission_to_organization_test.py


"""

import pytest
from sqlalchemy.orm import Session
from ....database import engine
from ....services.organization import OrganizationService
from ....services.permission import (
    PermissionService,
    PermissionEntity,
)
from ....services.exceptions import UserPermissionException
from ....entities.organization_entity import OrganizationEntity
from ....entities.user_entity import UserEntity
from ....entities.role_entity import RoleEntity, Role
from ....models.organization import Organization
from ....models.user import User


__authors__ = ["Dan Peng", "Jackson Davis, Antonio Tudela"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"


# mock user and role
root = User(id=1, pid=730233445, onyen="root", email="root@unc.edu")
root_role = Role(id=1, name="root")
root_user_entity = UserEntity.from_model(root)

leader = User(id=3, pid=730299873, onyen="leaderlee", email="lee@unc.edu")
leader_role = Role(id=3, name="leaderlee")
leader_user_entity = UserEntity.from_model(leader)

member = User(id=4, pid=730299874, onyen="membermary", email="mary@unc.edu")
member_role = Role(id=4, name="membermary")
member_user_entity = UserEntity.from_model(member)

# Mock organizations
org1 = Organization(
    id=1,
    name="CS+Social Good",
    overview="Through technology, we have the opportunity to be a part of the positive change and evolution of a growing world of possibility. We aim to give nonprofits and organizations for social good in the Chapel Hill area the tools to effectively complete their goals with the use of knowledge and programs. We partner with 2-3 organizations per semester and develop custom technology solutions for their needs. These groups include 501(c) organizations, student groups, and Ph.D. candidates.",
    description="Mission Statement: ",
    slug="cssg",
    shorthand="CSSG",
    logo="https://se-images.campuslabs.com/clink/images/ee0bc303-002e-4aca-aaba-81ad270d3901c0ac95ac-7e47-4ee6-95bf-c6f9598dd2fd.jpg?preset=med-sq",
    short_description="We build apps for nonprofits and organizations for social good.",
    long_description="Through technology, we have the opportunity to be a part of the positive change and evolution of a growing world of possibility. We aim to give nonprofits and organizations for social good in the Chapel Hill area the tools to effectively complete their goals with the use of knowledge and programs. We partner with 2-3 organizations per semester and develop custom technology solutions for their needs. These groups include 501(c) organizations, student groups, and Ph.D. candidates.",
    website="https://cssgunc.org/",
    email="cssg@unc.edu",
    instagram="https://www.instagram.com/unc_cssg/",
    linked_in="cssg",
    youtube="cssg",
    heel_life="cssg",
    public=True,
    application_required=True,
)


org2 = Organization(
    id=2,
    name="Ackland Art Museum",
    overview="The Ackland Art Museum features a collection of over 19,000 artworks and rotating exhibitions throughout the year. Admission to the Museum is free for all. A vibrant schedule of events and opportunities for students to get involved are available.",
    description="The Ackland Art Museum, located on S. Columbia Street near Franklin St., features a permanent collection of over 20,000 works of art. Rotating special exhibitions feature a wide range of art: from sound and video installations to early modern prints and photographs, from 19th-century French paintings to contemporary Japanese ceramics. Ackland Upstairs is the Museum’s second floor gallery where they display art selected by UNC-Chapel Hill faculty members to complement the courses they teach. It’s likely you will have a class at the Ackland during your time at Carolina! The Ackland also offers a vibrant year-round schedule of free and low-cost public programs featuring live music, ﬁlms, hands-on art making classes, gallery tours, and evening and weekend activities. Their ART& community space is food & beverage friendly and makes a great study spot. The Ackland offers a variety of opportunities for students to engage with the Museum, including the Ackland Student Guide program and internships. In addition, student memberships to the Museum are free for UNC undergraduate and graduate students and offer benefits including 10'%' off at the Museum Store. Sign up for FREE Ackland Student Membership. To stay connected, follow the Ackland on social media and sign up for our e-news! https://www.youtube.com/watch?v=0H1nKdxZp-E&t=2s",
    slug="ackland",
    shorthand="Ackland",
    logo="https://se-images.campuslabs.com/clink/images/ee0bc303-002e-4aca-aaba-81ad270d3901c0ac95ac-7e47-4ee6-95bf-c6f9598dd2fd.jpg?preset=med-sq",
    short_description="The Ackland Art Museum features a collection of over 19,000 artworks and rotating exhibitions throughout the year.",
    long_description="long description",
    website="https://ackland.unc.edu/",
    email="ackland@unc.edu",
    instagram="https://www.instagram.com/ackland",
    linked_in="ackland",
    youtube="ackland",
    heel_life="ackland",
    public=True,
    application_required=False,
)

org6 = Organization(
    id=6,
    name="1789",
    overview="1789, powered by Innovate Carolina,  is free a co-working space and venture lab designed for students to take their idea to the next level, meet other student entrepreneurs, connect to resources and grow a team. ",
    description="1789, powered by Innovate Carolina, is the University's central hub where innovation and entrepreneurship happen for all UNC students with an idea. Any UNC student is welcome to join.  1789 is free a co-working space and venture lab designed for students to take their idea to the next level, meet other student entrepreneurs, connect to resources and grow a team. With an open, flexible workspace conveniently located at 173 E. Franklin Street in the heart of downtown Chapel Hill, members may use the space for individual brainstorming, small meetings or larger events.  Innovate Carolina works to connect and support all students and programs on campus interested in innovation or entrepreneurship.  1789 members are not only connected to the Innovate Carolina network, but are also provided individualized support in starting their own ventures with access to workshops, classes, office hours and events in partnership with groups like Launch Chapel Hill, the Campus Y, the UNC Minor in Entrepreneurship, the Carolina Challenge and a plethora of other student organizations. ",
    slug="1789",
    shorthand="1789",
    logo="https://se-images.campuslabs.com/clink/images/13f76c3b-9504-46be-9b9a-0362c5ffb8d7f82aa3e6-2be6-4000-85f1-227422f703bc.jpg?preset=med-sq",
    short_description="1789, powered by Innovate Carolina,  is free a co-working space and venture lab designed for students to take their idea to the next level, meet other student entrepreneurs, connect to resources and grow a team. ",
    long_description="1789 long description",
    website="https://innovate.unc.edu/1789/",
    email="1789@unc.edu",
    instagram="https://www.instagram.com/1789",
    linked_in="1789",
    youtube="1789",
    heel_life="1789",
    public=True,
    application_required=False,
)


@pytest.fixture(autouse=True)
def setup_teardown(session: Session):
    # Bootstrap root User and Role
    global root_user_entity
    root_user_entity = UserEntity.from_model(root)
    session.add(root_user_entity)
    root_role_entity = RoleEntity.from_model(root_role)
    root_role_entity.users.append(root_user_entity)
    session.add(root_role_entity)
    root_permission_entity = PermissionEntity(
        action="*", resource="*", role=root_role_entity
    )
    session.add(root_permission_entity)
    session.commit()

    # Bootstrap leaderlee User and Role, this user should not be able to make /delete events/ orgs
    global leader_user_entity
    leader_user_entity = UserEntity.from_model(leader)
    session.add(leader_user_entity)
    leader_role_entity = RoleEntity.from_model(leader_role)
    leader_role_entity.users.append(leader_user_entity)
    session.add(leader_role_entity)
    leader_permission_entity = PermissionEntity(
        action="*", resource="*", role=leader_role_entity
    )
    session.add(leader_permission_entity)

    # Bootstrap member user and role
    global member_user_entity
    member_user_entity = UserEntity.from_model(member)
    session.add(member_user_entity)
    member_role_entity = RoleEntity.from_model(member_role)
    member_role_entity.users.append(member_user_entity)
    session.add(member_role_entity)
    member_permission_entity = PermissionEntity(
        action="organization.get_organization_by_slug",
        resource="*",
        role=member_role_entity,
    )
    session.add(member_permission_entity)

    # Bootstrap org1
    org_one_entity = OrganizationEntity.from_model(org1)
    session.add(org_one_entity)
    session.commit()
    # Bootstrap org2
    org_two_entity = OrganizationEntity.from_model(org2)
    session.add(org_two_entity)
    session.commit()
    # Bootstrap org6
    org_six_entity = OrganizationEntity.from_model(org6)
    session.add(org_six_entity)
    session.commit()
    yield


@pytest.fixture()
def organization(session: Session):
    return OrganizationService(session, PermissionService(session))


def test_organization_get_id_valid(organization: OrganizationService):
    assert organization.get_by_slug("cssg").id == 1


# This test makes sure that an invalid club name, i.e, one that does not exist, raises an exception (as it should as thats how we handle it in the OrganizationService class)
def test_organization_get_id_invalid(organization: OrganizationService):
    with pytest.raises(Exception) as e:
        organization.get_by_slug("cssssg")


def test_edit_organization_valid(organization: OrganizationService):
    # first check to make sure the normal overview is there
    assert organization.get_by_slug("cssg").name == "CS+Social Good"
    # then we make a "new org" with the desired values to be passed into the service method
    org: Organization = Organization(
        id=1,
        name="CS+Social Hella Good",
        overview="this is a test",
        description="Mission Statement: ",
        slug="csshg",
        shorthand="this is a test",
        logo="https://se-images.campuslabs.com/clink/images/ee0bc303-002e-4aca-aaba-81ad270d3901c0ac95ac-7e47-4ee6-95bf-c6f9598dd2fd.jpg?preset=med-sq",
        short_description="We build apps for nonprofits and organizations for social good.",
        long_description="Through technology, we have the opportunity to be a part of the positive change and evolution of a growing world of possibility. We aim to give nonprofits and organizations for social good in the Chapel Hill area the tools to effectively complete their goals with the use of knowledge and programs. We partner with 2-3 organizations per semester and develop custom technology solutions for their needs. These groups include 501(c) organizations, student groups, and Ph.D. candidates.",
        website="https://csshgunc.org/",
        instagram="https://www.instagram.com/unc_csshg/",
        linked_in="csshg",
        youtube="csshg",
        heel_life="csshg",
        email="csshg@unc.edu",
        public=True,
        application_required=False,
    )
    # next we pass in the above org
    organization.update(root_user_entity, org)
    # and finally we check if the service method did its job and changed the values
    assert organization.get_by_slug("csshg").shorthand == "this is a test"


def test_edit_organization_invalid(organization: OrganizationService):
    # try to use the service method without supplying it an organization
    with pytest.raises(Exception) as e:
        org: Organization = Organization()
        organization.update(org)


# the test below further test user permissions


def test_member_cannot_create_organizaiton(organization: OrganizationService):
    # first we check the default number of organizations
    assert len(organization.all()) == 3
    # then we try to delete one as arden and make sure it does NOT get deleted
    with pytest.raises(UserPermissionException) as E:
        organization.delete(member_user_entity, "1789")
    assert len(organization.all()) == 3


def test_leader_can_delete_organization(organization: OrganizationService):
    # first we check the default number of organizations
    assert len(organization.all()) == 3
    # then we delete one as a member and check the length to make sure its gone down by one
    organization.delete(leader_user_entity, "1789")
    assert len(organization.all()) == 2


def test_leader_can_edit_organization(organization: OrganizationService):
    # first check to make sure the normal overview is there
    assert organization.get_by_slug("cssg").name == "CS+Social Good"
    # then we make a "new org" with the desired values to be passed into the service method
    org: Organization = Organization(
        id=1,
        name="CS+Social Hella Good",
        overview="this is a test",
        description="Mission Statement: ",
        slug="csshg",
        shorthand="this is a test",
        logo="https://se-images.campuslabs.com/clink/images/ee0bc303-002e-4aca-aaba-81ad270d3901c0ac95ac-7e47-4ee6-95bf-c6f9598dd2fd.jpg?preset=med-sq",
        short_description="We build apps for nonprofits and organizations for social good.",
        long_description="Through technology, we have the opportunity to be a part of the positive change and evolution of a growing world of possibility. We aim to give nonprofits and organizations for social good in the Chapel Hill area the tools to effectively complete their goals with the use of knowledge and programs. We partner with 2-3 organizations per semester and develop custom technology solutions for their needs. These groups include 501(c) organizations, student groups, and Ph.D. candidates.",
        website="https://csshgunc.org/",
        instagram="https://www.instagram.com/unc_csshg/",
        linked_in="csshg",
        youtube="csshg",
        heel_life="csshg",
        email="csshg@unc.edu",
        public=True,
        application_required=False,
    )
    # next we pass in the above org
    organization.update(leader_user_entity, org)
    # and finally we check if the service method did its job and changed the values
    assert organization.get_by_slug("csshg").shorthand == "this is a test"


def test_member_cannot_edit_organization(organization: OrganizationService):
    # first check to make sure the normal overview is there
    assert organization.get_by_slug("cssg").name == "CS+Social Good"
    # then we make a "new org" with the desired values to be passed into the service method
    org: Organization = Organization(
        id=1,
        name="CS+Social Hella Good",
        overview="this is a test",
        description="Mission Statement: ",
        slug="csshg",
        shorthand="this is a test",
        logo="https://se-images.campuslabs.com/clink/images/ee0bc303-002e-4aca-aaba-81ad270d3901c0ac95ac-7e47-4ee6-95bf-c6f9598dd2fd.jpg?preset=med-sq",
        short_description="We build apps for nonprofits and organizations for social good.",
        long_description="Through technology, we have the opportunity to be a part of the positive change and evolution of a growing world of possibility. We aim to give nonprofits and organizations for social good in the Chapel Hill area the tools to effectively complete their goals with the use of knowledge and programs. We partner with 2-3 organizations per semester and develop custom technology solutions for their needs. These groups include 501(c) organizations, student groups, and Ph.D. candidates.",
        website="https://csshgunc.org/",
        instagram="https://www.instagram.com/unc_csshg/",
        linked_in="csshg",
        youtube="csshg",
        heel_life="csshg",
        email="csshg@unc.edu",
        public=True,
        application_required=False,
    )
    # next we pass in the above org and expect an exception
    with pytest.raises(
        UserPermissionException,
        match=r"Not authorized to perform `organization.update` on `organization/csshg`",
    ):
        organization.update(member_user_entity, org)
