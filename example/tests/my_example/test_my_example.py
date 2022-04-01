"""
my_example unit test.
This file is generated once, but never overwritten.
Implement the actual test in test_my_example
"""
import logging
import unittest
from my_example.base import MyExampleUnitTestBase


class MyExampleUnitTest(MyExampleUnitTestBase):
    def test_my_example(self) -> None:
        """
        test my_example. Stubbed clients will be returned for:
            - self.session.client("ec2")
            - self.session.client("ssm")
            - self.session.client("rds").
        """
        logging.warning(
            "TODO: replace MyExampleUnitTest.test_my_example with the actual test. This just tests the generated code."
        )
        from my_example import call_00001_describe_regions

        response = self.session.client("ec2").describe_regions(
            **call_00001_describe_regions.request
        )
        self.assertEqual(call_00001_describe_regions.response, response)

        from my_example import call_00002_describe_parameters

        response = self.session.client("ssm").describe_parameters(
            **call_00002_describe_parameters.request
        )
        self.assertEqual(call_00002_describe_parameters.response, response)

        from my_example import call_00003_describe_db_clusters

        response = self.session.client("rds").describe_db_clusters(
            **call_00003_describe_db_clusters.request
        )
        self.assertEqual(call_00003_describe_db_clusters.response, response)

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()


if __name__ == "__main__":
    unittest.main()
