from django.core.management.base import BaseCommand, CommandError
from django.conf import settings

from dynamodb_mapper.model import DynamoDBModel
from boto.exception import DynamoDBResponseError
from dynamodb_mapper.model import ConnectionBorg
from core.ddb_schema import (
        Contributor,
        Album,
        Mobject,
        Sessions,
        ContributorAlbum,
    )


class Command(BaseCommand):
    args = ''
    help = 'Evaluate rules realted to heater status. The result will start or stop the heater'

    def handle(self, *args, **options):
        conn = ConnectionBorg()
        conn.set_credentials(aws_access_key_id=settings.DYNAMODB_SESSIONS_AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.DYNAMODB_SESSIONS_AWS_SECRET_ACCESS_KEY,)
        try:
            conn.create_table(Contributor, 10, 10, wait_for_active=False)
            self.stdout.write("Contributor table created")
        except DynamoDBResponseError, er:
            print(er)
        try:
            conn.create_table(Album, 10, 10, wait_for_active=False)
            self.stdout.write("Album table created")
        except DynamoDBResponseError, er:
            print(er)
        try:
            conn.create_table(Mobject, 10, 10, wait_for_active=False)
            self.stdout.write("Mobject table created")
        except DynamoDBResponseError, er:
            print(er)
        try:
            conn.create_table(Sessions, 10, 10, wait_for_active=False)
            self.stdout.write("Sessions table created")
        except DynamoDBResponseError, er:
            print(er)
        try:
            conn.create_table(ContributorAlbum, 10, 10, wait_for_active=False)
            self.stdout.write("ContributorAlbum table created")
        except DynamoDBResponseError, er:
            print(er)
        self.stdout.write("DynamoDB created")
