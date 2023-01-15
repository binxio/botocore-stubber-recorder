"""
Generated base class for the my_example unit test. The setup will provide stubbed
responses for all recorded requests.

** generated code - do not edit **
"""
import unittest
import boto3
import botocore.session
from botocore.stub import Stubber
from botocore_stubber_recorder import BotoRecorder, UnitTestGenerator
from pathlib import Path


from my_example import call_00001_describe_regions

from my_example import call_00002_describe_parameters

from my_example import call_00003_describe_db_clusters


class MyExampleUnitTestBase(unittest.TestCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.default_session_configuration = {
            "profile_name": "integration-test",
            "region_name": "eu-west-1",
        }
        self.record = False
        self.anonimize = False
        self.unflatten = False

    def setUp(self) -> None:
        if self.record:
            self.start_recorder()
        else:
            self.activate_stubs()

    def activate_stubs(self) -> None:
        """
        add stubs for all AWS API calls
        """
        boto3.DEFAULT_SESSION = None
        self.botocore_session = botocore.session.get_session()
        boto3.setup_default_session(botocore_session=self.botocore_session)
        self.session = boto3.DEFAULT_SESSION
        self.session.client = lambda x: self.clients[x]

        self.clients = {
            service: self.botocore_session.create_client(service)
            for service in ["ec2", "rds", "ssm"]
        }
        self.stubs = {
            service: Stubber(client) for service, client in self.clients.items()
        }

        self.stubs["ec2"].add_response(
            "describe_regions",
            call_00001_describe_regions.response,
            call_00001_describe_regions.request,
        )

        self.stubs["ssm"].add_response(
            "describe_parameters",
            call_00002_describe_parameters.response,
            call_00002_describe_parameters.request,
        )

        self.stubs["rds"].add_response(
            "describe_db_clusters",
            call_00003_describe_db_clusters.response,
            call_00003_describe_db_clusters.request,
        )

        for _, stub in self.stubs.items():
            stub.activate()

    def tearDown(self) -> None:
        boto3.DEFAULT_SESSION = None
        if self.record:
            self.write_stubs()
        else:
            self.deactivate_stubs()

    def deactivate_stubs(self) -> None:
        """
        check all api calls were executed
        """
        for service, stub in self.stubs.items():
            stub.assert_no_pending_responses()
            stub.deactivate()

    def start_recorder(self):
        boto3.DEFAULT_SESSION = None
        boto3.setup_default_session(**self.default_session_configuration)
        self.recorder = BotoRecorder(boto3.DEFAULT_SESSION)
        self.session = self.recorder.session

    def write_stubs(self):
        test_name = "my_example"
        directory = "./tests"
        generator = UnitTestGenerator(test_name, directory, "")
        generator.generate(self.recorder, False, True)
