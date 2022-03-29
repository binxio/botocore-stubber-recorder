import botocore
import re, os
from typing import Dict
from botocore_stubber_recorder.request import BotoRequest


class BotoRecorder:
    def __init__(self, session: botocore.session.Session):
        self.requests: [BotoRequest] = []
        self.session = session
        self.session.events.register(
            event_name="before-call.*", handler=self.before_call_handler
        )
        self.session.events.register(
            event_name="after-call.*", handler=self.after_call_handler
        )

    @property
    def invoked_service_names(self) -> set:
        """
        returns the set of AWS service names invoked in the recording
        """
        return set(map(lambda r: r.service_name, self.requests))

    def before_call_handler(self, *args, **kwargs):
        model = kwargs["model"]
        body = kwargs["params"].get("body")
        self.requests.append(BotoRequest(model, body))

    def after_call_handler(self, *args, **kwargs):
        request = self.requests[-1] if self.requests else None
        if not request or request.model != kwargs["model"]:
            logging.warn("received a response no matching a request")
            return
        request.response = kwargs["parsed"]
