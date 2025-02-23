import logging
import os
import re
import sqlite3
from datetime import datetime

import pandas as pd
from dateutil.parser import parse
from django.conf import settings

from file_scheduler.celery import app


SUB_REGEX = "[\s\W_-]+"
XLSX_FILENAME_REGEX = re.compile(r"^(?P<filename>.*)\.xlsx$")

logger = logging.getLogger("celery")


def _escape(str) -> str:
    return re.sub(SUB_REGEX, "_", str).lower()


@app.task
def read_file_task():
    conn = sqlite3.connect(settings.DATABASES["default"]["NAME"])

    files_location = settings.FILES_LOCATION

    for file in os.listdir(files_location):
        match = XLSX_FILENAME_REGEX.match(file)
        if not match:
            logger.error(f"file: \"{file}\" is not a valid xlsx file")
            continue

        try:
            data = pd.read_excel(files_location / file)
        except ValueError:
            logger.error(f"file \"{file}\" is broken or can't be read")
            continue

        data.columns = [_escape(column) for column in data.columns]

        for column in data.columns:
            try:
                data[column] = data[column].apply(parse)
            except:
                continue

        filename = match.group('filename')

        table_name = "{}_{}".format(_escape(filename),
                                    datetime.now().strftime("%Y%m%d_%H%M"))
        try:
            data.to_sql(table_name, con=conn, if_exists='replace', index=False)
            logger.info(
                f"File \"{file}\" successfully saved to database as \"{table_name}\""
            )
        except Exception as e:
            logger.error(f"Error during save file \"{file}\" to database: {e}")
        else:
            os.remove(files_location / file)
    return
