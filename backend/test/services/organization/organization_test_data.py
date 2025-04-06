"""Contains mock data for to run tests on the organization feature."""

import pytest
from sqlalchemy.orm import Session
from ....models.organization import Organization
from ....entities.organization_entity import OrganizationEntity

from ..reset_table_id_seq import reset_table_id_seq

__authors__ = ["Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Sample Data Objects

appteam = Organization(
    id=1,
    name="App Team Carolina",
    shorthand="App Team",
    slug="app-team",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/appteam.jpg",
    short_description="UNC Chapel Hill's iOS development team.",
    long_description="The mission of App Team Carolina is to create a collaborative space for UNC students to design, build, and release apps for Apple platforms. App Team Carolina's multi-faceted development process aims to leverage its individual skillsets while encouraging cooperation among team members with different levels of experience.",
    website="",
    email="",
    instagram="https://www.instagram.com/appteamcarolina/",
    linked_in="https://www.linkedin.com/company/appteamcarolina",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/appteamcarolina",
    public="request",
    application_required=True,
)

acm = Organization(
    id=2,
    name="ACM at Carolina",
    shorthand="ACM",
    slug="acm",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/acm.jpg",
    short_description="Largest community and professional society for Tar Heels who study computing.",
    long_description="We are a professional community of Tar Heels who study computing; we are dedicated to exploring our field, defining our interests, engaging with each other, discovering our strengths, and improving our skills.",
    website="https://linktr.ee/unc_acm",
    email="uncacm@unc.edu",
    instagram="https://www.instagram.com/unc_acm/",
    linked_in="",
    youtube="https://www.youtube.com/channel/UCkgDDL-DKsFJKpld2SosbxA",
    heel_life="https://heellife.unc.edu/organization/acm-at-carolina",
    public="request",
    application_required=True,
)

bit = Organization(
    id=3,
    name="Black in Technology",
    shorthand="BIT",
    slug="bit",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/bit.jpg",
    short_description="Increasing Black and other ethnic participation in the fields of technology and Computer Science.",
    long_description="Black in Technology (BiT) is a student and technology-based organization, that dedicates itself to the development of intensive programs for increasing Black and other ethnic participation in the field of technology and Computer Science. BiT aims to increase the representation of Black students pursuing degrees in technology at the University of North Carolina at Chapel Hill. The primary mission of BiT is to voice the concerns of members and work to create an inclusive ecosystem for Black technology majors to thrive within the University.",
    website="https://linktr.ee/BiTunc",
    email="blackintechunc@gmail.com",
    instagram="https://www.instagram.com/uncbit/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/bit",
    public="request",
    application_required=True,
)

cads = Organization(
    id=4,
    name="Carolina Analytics & Data Science Club",
    shorthand="CADS",
    slug="cads",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
    short_description="Provides students interested in Data Science opportunities to grow.",
    long_description="CADS provides students interested in Data Science opportunities to grow personally, intellectually, professionally, and socially among a support network of students, professors, and career professionals. This mission is to be accomplished through events, including a speaker series from industry professionals, data case competition, workshops, and investigating and analyzing University and community data to drive community-based projects and solutions.",
    website="https://carolinadata.unc.edu/",
    email="carolinadatascience@gmail.com",
    instagram="https://www.instagram.com/carolinadatascience/",
    linked_in="https://www.linkedin.com/company/carolina-data/",
    youtube="https://www.youtube.com/channel/UCO44Yjhjuo5-TLUCAaP0-cQ",
    heel_life="https://heellife.unc.edu/organization/carolinadatascience",
    public="open",
    application_required=True,
)

carvr = Organization(
    id=5,
    name="Carolina Augmented and Virtual Reality",
    shorthand="CARVR",
    slug="carvr",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/arvr.png",
    short_description="Students explore XR technologies and connect to clients to create real-world applications.",
    long_description="CARVR is a student organization at UNC Chapel Hill that promotes student development in XR technologies. Students explore XR technologies, learn XR development, work on XR projects and connect to clients to create real-world applications. All students â€“ graduate or undergraduate, in any discipline â€“ are welcome to join!",
    website="https://arvr.web.unc.edu/",
    email="",
    instagram="https://www.instagram.com/uncarvr/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/carvr",
    public="request",
    application_required=True,
)

cssg = Organization(
    id=6,
    name="CS+Social Good",
    shorthand="CSSG",
    slug="cssg",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cssg.png",
    short_description="We build apps for nonprofits and organizations for social good.",
    long_description="Through technology, we have the opportunity to be a part of the positive change and evolution of a growing world of possibility. We aim to give nonprofits and organizations for social good in the Chapel Hill area the tools to effectively complete their goals with the use of knowledge and programs. We partner with 2-3 organizations per semester and develop custom technology solutions for their needs. These groups include 501(c) organizations, student groups, and Ph.D. candidates.",
    website="https://cssgunc.org/",
    email="cssgunc@gmail.com",
    instagram="https://www.instagram.com/unc_cssg/",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/cssg",
    public="request",
    application_required=True,
)

ctf = Organization(
    id=7,
    name="Cybersecurity CTF Club",
    shorthand="CTF",
    slug="ctf",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/ctf.jpg",
    short_description="Hands-on computer security club, developing practical technical abilities through workshops and competitions.",
    long_description="We primarily communicate through discord, invite link atÂ <https://discord.gg/GSdrVQ7>\nUNC-CH's hands-on computer security club, developing practical technical abilities in students and members of the local enthusiast community through lecture, workshops, and participation in competition against teams of practitioners across the world.\n\nCTF stands for Capture The Flag, a form of competitive computer security competition with a typical focus in offensive or defensive operations, or solving a wide array of challenges in a variety of categories.\n\nWe regularly practice skills in reverse engineering, system exploitation, web app auditing, forensics, and cryptography.",
    website="https://ntropy-unc.github.io/",
    email="ntropy.unc@gmail.com",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="https://heellife.unc.edu/organization/ntropy-unc",
    public="closed",
    application_required=True,
)

organizations = [appteam, acm, bit, cads, carvr, cssg, ctf]
organization_names = [org.name for org in organizations]

to_add = Organization(
    name="Android Development Club",
    shorthand="Android Club",
    slug="android-club",
    logo="https://1000logos.net/wp-content/uploads/2016/10/Android-Logo.png",
    short_description="UNC Chapel Hill's Android development team.",
    long_description="We make super cool Android apps for the UNC CS department.",
    website="",
    email="",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="",
    public="request",
    application_required=True,
)

to_add_conflicting_id = Organization(
    id=2,
    name="Android Development Club",
    shorthand="Android Club",
    slug="android-club",
    logo="https://1000logos.net/wp-content/uploads/2016/10/Android-Logo.png",
    short_description="UNC Chapel Hill's Android development team.",
    long_description="We make super cool Android apps for the UNC CS department.",
    website="",
    email="",
    instagram="",
    linked_in="",
    youtube="",
    heel_life="",
    public="request",
    application_required=True,
)

new_cads = Organization(
    id=4,
    name="Carolina Analytics & Data Science Club",
    shorthand="CADS",
    slug="cads",
    logo="https://raw.githubusercontent.com/briannata/comp423_a3_starter/main/logos/cads.png",
    short_description="Provides students interested in Data Science opportunities to grow.",
    long_description="CADS provides students interested in Data Science opportunities to grow personally, intellectually, professionally, and socially among a support network of students, professors, and career professionals. This mission is to be accomplished through events, including a speaker series from industry professionals, data case competition, workshops, and investigating and analyzing University and community data to drive community-based projects and solutions.",
    website="https://cads.cs.unc.edu/",
    email="carolinadatascience@gmail.com",
    instagram="https://www.instagram.com/carolinadatascience/",
    linked_in="https://www.linkedin.com/company/carolina-data/",
    youtube="https://www.youtube.com/channel/UCO44Yjhjuo5-TLUCAaP0-cQ",
    heel_life="https://heellife.unc.edu/organization/carolinadatascience",
    public="request",
    application_required=True,
)

# Data Functions


def insert_fake_data(session: Session):
    """Inserts fake organization data into the test session."""

    global organizations
    print("Inserting organizations into session...")
    # Create entities for test organization data
    entities = []
    for org in organizations:
        entity = OrganizationEntity.from_model(org)
        session.add(entity)
        entities.append(entity)
        print(f"Adding organization: {entity.name} (id={entity.id})")

    # Reset table IDs to prevent ID conflicts
    reset_table_id_seq(
        session, OrganizationEntity, OrganizationEntity.id, len(organizations) + 1
    )

    session.commit()
    print("Organizations (test) committed to database.")
    print("======================================")
    # organizatio = session.query().all()
    # print(f"Inserted organizations: {[org.id for org in organizatio]}")


@pytest.fixture(autouse=True)
def fake_data_fixture(session: Session):
    """Insert fake data the session automatically when test is run.
    Note:
        This function runs automatically due to the fixture property `autouse=True`.
    """
    insert_fake_data(session)
    session.commit()
    yield
