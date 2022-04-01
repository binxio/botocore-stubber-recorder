import boto3
from report import report
from botocore_stubber_recorder import BotoRecorder, BotoRecorderUnitTestGenerator

session = boto3.session.Session()
recorder = BotoRecorder(session)
report(session)
for index, call in enumerate(recorder.calls):
    print(f"call {index +1}: {call.service_name}:{call.operation}")

with BotoRecorderUnitTestGenerator("my_example", session, anonimize=True) as generator:
    report(session)
