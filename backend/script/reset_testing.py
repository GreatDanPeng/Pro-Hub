"""
This script resets the SQLAlchemy database to contain the same data that
is used when running the pytests.

Previously, we duplicated data between testing and this database reset.
Moving forward, we'll aim to have some parity between tests and dev reset.
This way, we both avoid duplication and make it easier to interact with
the state of the system we are writing tests for.

Usage: python3 -m script.reset_testing
"""

import sys
import subprocess
from sqlalchemy import text
from sqlalchemy.orm import Session
from ..database import engine
from ..env import getenv
from .. import entities

from ..test.services import role_data, user_data, permission_data, room_data
from ..test.services.organization import organization_test_data
from ..test.services.event import event_test_data
from ..test.services.coworking import seat_data, operating_hours_data, time
from ..test.services.coworking.reservation import reservation_data

__authors__ = ["Kris Jordan", "Ajay Gandecha"]
__copyright__ = "Copyright 2023"
__license__ = "MIT"

# Ensures that the script can only be run in development mode
if getenv("MODE") != "development":
    print("This script can only be run in development mode.", file=sys.stderr)
    print("Add MODE=development to your .env file in workspace's `backend/` directory")
    exit(1)

# Run Delete and Create Database Scripts
subprocess.run(["python3", "-m", "backend.script.delete_database"])
subprocess.run(["python3", "-m", "backend.script.create_database"])

# Reset Tables
print("Dropping and creating tables...")
print("Dropping and creating tables...")
entities.EntityBase.metadata.drop_all(engine)
entities.EntityBase.metadata.create_all(engine)
print("Tables recreated successfully.")
print("Tables recreated successfully.")

# Initialize the SQLAlchemy session
with Session(engine) as session:
    # Load all testing data
    print("Inserting data...")
    print("Inserting data...")
    time = time.time_data()
    role_data.insert_fake_data(session)
    organization_test_data.insert_fake_data(session)
    user_data.insert_fake_data(session)
    permission_data.insert_fake_data(session)
    event_test_data.insert_fake_data(session)
    operating_hours_data.insert_fake_data(session, time)
    room_data.insert_fake_data(session)
    seat_data.insert_fake_data(session)
    reservation_data.insert_fake_data(session, time)
    print("Data inserted and committed.")

    # Verify data
    print("Data inserted and committed.")

    # Verify data

    # Commit changes to the database
    session.commit()
