from botocore.session import Session
import re, os
from typing import Dict
from botocore_stubber_recorder.request import APICall


class BotoRecorder:
    """
    records all AWS API calls
    """

    def __init__(self, session: Session):
        self.calls: [APICall] = []
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
        returns the set of AWS service names invoked in the calls
        """
        return set(map(lambda r: r.service_name, self.calls))

    def before_call_handler(self, *args, **kwargs):
        """
        add a call for this request.
        """
        model = kwargs["model"]
        body = kwargs["params"].get("body")
        self.calls.append(APICall(model, body))

    def after_call_handler(self, *args, **kwargs):
        """
        adds the response to the last recorded call.
        """
        call = self.calls[-1] if self.calls else None
        if not call or call.model != kwargs["model"]:
            logging.warn("received a response no matching a request")
            return
        call.response = kwargs["parsed"]
