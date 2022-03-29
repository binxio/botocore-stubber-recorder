import os
import re
import logging
import botocore
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from botocore_stubber_recorder.recorder import BotoRecorder
from botocore_stubber_recorder.request import BotoRequest

env = Environment(
    loader=PackageLoader("botocore_stubber_recorder"), autoescape=select_autoescape()
)


class UnitTestGenerator:
    def __init__(self, name: str, directory: str):
        self.directory = directory
        self.name = name
        self.aws_account = "123456789012"

    @property
    def unittest_base_template(self) -> Template:
        return env.get_template("unittest_base.j2")

    @property
    def unittest_template(self) -> Template:
        return env.get_template("unittest.j2")

    @property
    def name_in_camel_case(self):
        return "".join(w.capitalize() or "_" for w in self.name.split("_"))

    def generate(self, recorder: BotoRecorder):
        test_directory = os.path.join(self.directory, self.name)
        os.makedirs(test_directory, exist_ok=True)

        filename = os.path.join(test_directory, "__init__.py")
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                pass

        filename = os.path.join(test_directory, "base.py")
        with open(filename, "w") as file:
            self.unittest_base_template.stream(generator=self, recorder=recorder).dump(
                file
            )

        filename = os.path.join(test_directory, f"test_{self.name}.py")
        if not os.path.exists(filename):
            with open(filename, "w") as file:
                self.unittest_template.stream(generator=self, recorder=recorder).dump(
                    file
                )
        else:
            logging.info("%s already exists, not overwritten", filename)

        for n, request in enumerate(recorder.requests):
            operation = botocore.xform_name(request.model.name)
            directory = os.path.join(test_directory, f"call_{n+1:05d}_{operation}")
            filename = os.path.join(directory, "__init__.py")
            os.makedirs(directory, exist_ok=True)
            if os.path.exists(filename):
                os.chmod(filename, 0o600)
            with os.fdopen(
                os.open(filename, os.O_WRONLY | os.O_CREAT, 0o600), "w"
            ) as file:
                request.generate_add_response_function(file)


_arn_regex = re.compile(
    r"arn:aws:(?P<service>[^:]*):(?P<region>[^:]*):(?P<account>[^:]*)"
)


def anonimize_aws_account(output: str) -> str:
    return _arn_regex.sub(
        lambda m: f'arn:aws:{m.group("service")}:{m.group("region")}:123456789012',
        output,
    )
