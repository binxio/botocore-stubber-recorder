import re
import json
from copy import deepcopy
from io import TextIOBase
from typing import Union
from uuid import uuid4

import botocore
from botocore.model import OperationModel
from botocore_stubber_recorder.unflatten import unflattener


class APICall:
    """
    represents an AWS API call.
    """

    def __init__(self, model: OperationModel, request: Union[dict, bytes]):
        self.uuid: str = str(uuid4())
        self._response: dict = {}
        self._request: dict = {}
        self.model: botocore.model.OperationModel = model
        self.request = request

    @property
    def request(self) -> dict:
        """
        the request of the call
        """
        return self._request

    @request.setter
    def request(self, request: Union[dict, bytes]):
        """
        Sets the `request`. if the request is a byte array, it is assumed to be a JSON
        representation of a dictionary.
        """
        if isinstance(request, dict):
            self._request = deepcopy(request if request else {})
        else:
            self._request = json.loads(request)

    @property
    def cleaned_request(self):
        """
        returns the request without the added Version and Action items. If
        it is a flattened request, it will be unflattened.
        """
        result = deepcopy(self._request)
        result.pop("Version", None)
        result.pop("Action", None)

        return result

    @property
    def is_flattened(self):
        """
        returns true if the keys contains a . suggesting a flattened request parameter
        """
        return any(filter(lambda k: "." in k, self._request.keys()))

    @property
    def unflattened(self):
        """
        returns and unflattened, cleaned request.
        """
        result = unflattener(self._request)
        result.pop("Version", None)
        result.pop("Action", None)
        return result

    @property
    def response(self) -> dict:
        """
        response associated to the request
        """
        return self._response

    @response.setter
    def response(self, response: dict):
        """
        sets the response for this `request`
        """
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

    def generate_add_response_function(
        self, stream: TextIOBase, anonimize: bool = False, unflatten: bool = False
    ):
        """
        returns python code for the function adding the `request` and `response` for the `operation`
        add_response to a passedin in stub. If anonimize is set to true, the AWS account number
        is replaced by a generic account number.
        If unflatten is set to true, we will try to unflatten the botocore request that was
        received by the event handler.
        """
        operation = botocore.xform_name(self.model.name)
        stream.truncate(0)
        original_request = (
            self.unflattened
            if unflatten and self.is_flattened
            else self.cleaned_request
        )
        request = (
            anonimize_aws_account(str(original_request))
            if anonimize
            else str(original_request)
        )
        response = (
            anonimize_aws_account(str(self.response))
            if anonimize
            else str(self.response)
        )
        stream.writelines(
            [
                "import botocore\n",
                "import datetime\n",
                "from dateutil.tz import tzutc, tzlocal\n",
                "\n\n",
                f"request = {request}\n",
                f"response = {response}\n",
            ]
        )


_arn_regex = re.compile(
    r"arn:aws:(?P<service>[^:]*):(?P<region>[^:]*):(?P<account>[^:]*)"
)


def anonimize_aws_account(output: str) -> str:
    return _arn_regex.sub(
        lambda m: f'arn:aws:{m.group("service")}:{m.group("region")}:123456789012',
        output,
    )
