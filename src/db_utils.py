import json
import os

import pandas as pd
from sqlalchemy import create_engine, text
from config import DB_CONNECTION_URI


engine = create_engine(DB_CONNECTION_URI)


def create_required_tables():
    """Create required tables if they do not exist"""
    with engine.connect() as connection:
        connection.execute(text("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='job_applications' AND xtype='U')
        CREATE TABLE job_applications (
            id INT PRIMARY KEY IDENTITY(1,1),
            url NVARCHAR(MAX),
            status NVARCHAR(50),
            message NVARCHAR(MAX)
        )
        """))
        connection.commit()


def read_jobs():
    """Read jobs from the database"""
    with engine.connect() as connection:
        jobs = pd.read_sql("SELECT url, status, message FROM job_applications where status is null or status = ''", connection)
        return jobs


def update_job_status(url, status, message="NA"):
    """Update job status and message in the database"""
    with engine.connect() as connection:
        connection.execute(
            text(
                f"update job_applications set status = '{status}', message = '{message}' where url = '{url}'"
            )
        )
        connection.commit()
