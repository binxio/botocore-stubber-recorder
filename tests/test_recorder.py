import boto3
import sys
import unittest
from tempfile import TemporaryDirectory
from botocore_stubber_recorder import (
    BotoRecorder,
    UnitTestGenerator,
    BotoRecorderUnitTestGenerator,
)


class MyTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.directory = TemporaryDirectory()

    def tearDown(self) -> None:
        self.directory.cleanup()

    def test_record_single_api_call(self):
        session = boto3.session.Session(profile_name="integration-test")
        recorder = BotoRecorder(session)

        client = session.client("ec2")
        response = client.describe_regions()
        self.assertEqual(1, len(recorder.calls))

        request = recorder.calls[0]
        self.assertEqual("DescribeRegions", request.model.name)
        self.assertEqual(
            request.request, {"Action": "DescribeRegions", "Version": "2016-11-15"}
        )
        self.assertEqual(response, request.response)

        self.assertSetEqual({"ec2"}, recorder.invoked_service_names)

        generator = UnitTestGenerator("describe_regions", "generated", "generated")
        generator.generate(recorder)

    def test_record_multiple_calls(self):

        session = boto3.session.Session(profile_name="integration-test")
        recorder = BotoRecorder(session)

        client = session.client("ec2")
        client.describe_regions()

        client = session.client("ssm")
        client.describe_parameters(
            Filters=[{"Key": "Name", "Values": ["ALPHA_"]}], MaxResults=50
        )

        client = session.client("rds")
        client.describe_db_clusters()

        self.assertEqual(3, len(recorder.calls))
        self.assertSetEqual({"ec2", "rds", "ssm"}, recorder.invoked_service_names)

        generator = UnitTestGenerator("multiple_calls", "generated", "generated")
        generator.generate(recorder)

    def test_contextmanager(self):
        session = boto3.session.Session(profile_name="integration-test")
        with BotoRecorderUnitTestGenerator(
            "contextmanager", session, "generated", "generated"
        ) as generator:
            client = session.client("rds")
            client.describe_db_instances()


if __name__ == "__main__":
    unittest.main()
