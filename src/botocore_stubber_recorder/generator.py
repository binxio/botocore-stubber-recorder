import os
import re
from contextlib import contextmanager
import logging
import botocore
from typing import Optional
from jinja2 import Template, Environment, PackageLoader, select_autoescape
from botocore_stubber_recorder.recorder import BotoRecorder
from botocore_stubber_recorder.request import BotoRequest

env = Environment(
    loader=PackageLoader("botocore_stubber_recorder"), autoescape=select_autoescape()
)


class UnitTestGenerator:
    def __init__(self, name: str, directory: str, package: str = None):
        if not re.match(r"[a-z_]+", name):
            raise ValueError(f'only snake case allowed for the name, not "{name}"')
        if package and not re.match(r"[a-z_\.]+", package):
            raise ValueError(
                f'only snake case and dots allowed for the package, not "{package}"'
            )

        self.directory = directory
        self.name = name
        self.package = f"{package}." if package else ""

    @property
    def unittest_base_template(self) -> Template:
        return env.get_template("unittest_base.j2")

    @property
    def unittest_template(self) -> Template:
        return env.get_template("unittest.j2")

    @property
    def name_in_camel_case(self):
        return "".join(w.capitalize() or "_" for w in self.name.split("_"))

    def _remove(self, path: str, type: Optional[str] = None):
        logging.info("removing generated %s %s", type, path)
        os.remove(path) if type == "file" else os.rmdir(path)

    def remove_all_call_directories(self, root: str):
        for call_directory in map(lambda e: os.path.join(root, e), os.listdir(root)):
            if re.match(r"^call_[0-9]{5,}_", os.path.basename(call_directory)):
                for (child, directories, files) in os.walk(
                    call_directory, topdown=False
                ):
                    for file in files:
                        self._remove(os.path.join(child, file), "file")
                    for directory in directories:
                        self._remove(os.path.join(child, directory))
                self._remove(call_directory)

    def generate(self, recorder: BotoRecorder, anonimize: bool = False):
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

        self.remove_all_call_directories(test_directory)
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
                request.generate_add_response_function(file, anonimize)


class BotoRecorderUnitTestGenerator:
    """
    a context manager which combines BotoRecorder and UnitTest generator, so you can write:

    with BotoRecorderUnitTestGenerator("describe_regions", session) as generator:
        response = session.client("ec2").describe_regions()

    this will generate
    """
    def __init__(
            self,
            name: str,
            session: botocore.session.Session,
            directory: str = "./tests",
            package: str = "",
            anonimize=True,
    ):
        self.session = session
        self.generator = UnitTestGenerator(name, directory, package)
        self.recorder: BotoRecorder = None
        self.anonimize = anonimize

    def __enter__(self):
        self.recorder = BotoRecorder(self.session)
        return self

    def __exit__(self, type, value, tb):
        self.generator.generate(self.recorder, self.anonimize)
