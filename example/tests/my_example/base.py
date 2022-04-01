"""
Generated base class for the my_example unit test. The setup will provide stubbed
responses for all recorded requests.

** generated code - do not edit **
"""
import unittest
import botocore.session
from botocore.stub import Stubber

from my_example import call_00001_describe_regions

from my_example import call_00002_describe_parameters

from my_example import call_00003_describe_db_clusters


class MyExampleUnitTestBase(unittest.TestCase):
    def setUp(self) -> None:
        """
        add stubs for all AWS API calls
        """
        self.session = botocore.session.get_session()
        self.clients = {
            service: self.session.create_client(service)
            for service in ["ssm", "ec2", "rds"]
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
        self.session.client = lambda x: self.clients[x]

    def tearDown(self) -> None:
        """
        check all api calls were executed
        """
        for service, stub in self.stubs.items():
            stub.assert_no_pending_responses()
            stub.deactivate()
