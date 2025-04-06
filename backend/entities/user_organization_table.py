"""Join table of membership between User and Organization entities.""" ""

from sqlalchemy import Table, Column, ForeignKey
from .entity_base import EntityBase


__authors__ = ["Dan Peng"]
__copyright__ = "Copyright 2024"
__license__ = "MIT"

# Define the user_organization table to be used as a join table to persist a
# many-to-many relationship between the users and organizations.
user_organization_table = Table(
    "user_organization",
    EntityBase.metadata,
    Column("user_id", ForeignKey("user.id"), primary_key=True),
    Column("organization_id", ForeignKey("organization.id"), primary_key=True),
)
