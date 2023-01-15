import os, re
import boto3
import logging
from botocore_stubber_recorder import BotoRecorder, UnitTestGenerator
import argparse
from pathlib import Path


def main():
    """
    generates a skeleton unit test which can record and replay its own
    AWS API calls.

    After the test is generated, modify the test and set the environment
    variable RECORD_UNITTEST_STUBS to true. Instead of providing stubbed
    responses, it will record the actual AWS API call.

    When RECORD_UNITTEST_STUBS is absent or set to false, the botocore
    stubs are activated.
    """
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"))
    parser = argparse.ArgumentParser(description=main.__doc__)
    parser.add_argument(
        "--test-name", "-n", required=True, help="to generate skeleton for"
    )
    parser.add_argument(
        "--output-directory",
        "-o",
        default="./tests",
        help="directory generate to, default is ./tests",
    )
    parser.add_argument(
        "--package-name", "-p", default="", help="name of package for the test"
    )
    parser.add_argument(
        "--anonymize",
        "-a",
        help="remove account id from the recordings",
        action="store_true",
    )
    parser.add_argument(
        "--unflatten",
        "-u",
        help="unflatten flattened AWS API requests",
        action="store_true",
    )
    args = parser.parse_args()

    if args.package_name and Path(args.output_directory).name != args.package_name:
        args.output_directory = str(Path(args.output_directory).joinpath(args.package_name))

    if not re.match(r'^[A-Za-z0-9_]+$', args.test_name):
        parser.exit(1, "ERROR: test name must consists of letters, lowercase or underscores")

    if args.package_name and not re.match(r'^[A-Za-z0-9_]*$', args.package_name):
        parser.exit(1, "ERROR: package name must consists of letters, lowercase or underscores")

    test_path = Path(args.output_directory).joinpath(args.test_name)
    if test_path.exists():
        logging.error("the test %s already exists, just run the test with RECORD_UNITTEST_STUBS=true", test_path)
        exit(1)

    session = boto3.session.Session()
    recorder = BotoRecorder(session)
    try:
        session.client("sts").get_caller_identity()
    except Exception:
        logging.error("failed to call get_caller_identity, please provide AWS credentials")
        exit(1)

    try:
        generator = UnitTestGenerator(
            name=args.test_name, directory=args.output_directory, package=args.package_name
        )
        generator.generate(recorder, anonimize=args.anonymize, unflatten=args.unflatten)
        logging.info("sketelon test %s written in %s", args.test_name, args.output_directory)
    except ValueError as error:
        logging.error("%s", error)

if __name__ == "__main__":
    main()
