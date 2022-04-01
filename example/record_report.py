import boto3
from report import report
from botocore_stubber_recorder import BotoRecorderUnitTestGenerator

session = boto3.session.Session()
with BotoRecorderUnitTestGenerator("report", session, anonimize=True) as generator:
    report(session)
