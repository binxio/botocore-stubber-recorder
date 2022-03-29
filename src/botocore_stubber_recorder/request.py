import json
from copy import deepcopy
from io import TextIOBase
from typing import Union
from uuid import uuid4

import botocore
from botocore.model import OperationModel


class BotoRequest:
    def __init__(self, model: OperationModel, request: Union[dict, bytes]):
        self.uuid: str = str(uuid4())
        self._response: dict = {}
        self._request: dict = {}
        self.model: botocore.model.OperationModel = model
        self.request = request

    @property
    def request(self) -> dict:
        return self._request

    @request.setter
    def request(self, request: Union[dict, bytes]):
        if isinstance(request, dict):
            self._request = deepcopy(request if request else {})
        else:
            self._request = json.loads(request)

    @property
    def cleaned_request(self):
        """
        returns the request without the added Version and Action items.
        """
        result = deepcopy(self._request)
        result.pop("Version", None)
        result.pop("Action", None)
        return result

    @property
    def response(self) -> dict:
        return self._response

    @response.setter
    def response(self, response: dict):
        self._response = deepcopy(response) if response else {}

    @property
    def operation(self):
        """
        returns the python function name for the API method `self.model.name`
        """
        return botocore.xform_name(self.model.name)

    @property
    def service_name(self):
        """
        returns the AWS service name.
        """
        return self.model.service_model.service_name

    def generate_add_response_function(self, stream: TextIOBase):
        """
        returns python code for the function adding the `request` and `response` for the `operation`
        add_response to a passedin in stub.
        :return:
        """
        operation = botocore.xform_name(self.model.name)
        stream.truncate(0)
        stream.writelines(
            [
                "import botocore\n",
                "import datetime\n",
                "from dateutil.tz import tzutc, tzlocal\n",
                "\n\n",
                f"request = {self.cleaned_request}\n",
                f"response = {self.response}\n",
            ]
        )
