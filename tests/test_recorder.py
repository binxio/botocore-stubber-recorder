import boto3
import unittest
from uuid import uuid4
from tempfile import TemporaryDirectory
from botocore_stubber_recorder import BotoRecorder, UnitTestGenerator


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
        self.assertEqual(1, len(recorder.requests))

        request = recorder.requests[0]
        self.assertEqual("DescribeRegions", request.model.name)
        self.assertEqual(request.request, {'Action': 'DescribeRegions', 'Version': '2016-11-15'})
        self.assertEqual(response, request.response)

        self.assertSetEqual({"ec2"}, recorder.invoked_service_names)

        generator = UnitTestGenerator("describe_regions", "generated")
        generator.generate(recorder)

    def test_record_multiple_calls(self):
        session = boto3.session.Session(profile_name="integration-test")
        recorder = BotoRecorder(session)

        client = session.client("ec2")
        client.describe_regions()

        client = session.client("ssm")
        client.describe_parameters(Filters=[{"Key": "Name", "Values": ["ALPHA_"]}], MaxResults=50)

        client = session.client("rds")
        client.describe_db_clusters()

        self.assertEqual(3, len(recorder.requests))
        self.assertSetEqual({"ec2",  "rds", "ssm"}, recorder.invoked_service_names)

        generator = UnitTestGenerator("multiple_calls", "generated")
        generator.generate(recorder)


if __name__ == '__main__':
    unittest.main()
