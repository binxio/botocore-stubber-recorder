import botocore
import datetime
from dateutil.tz import tzutc, tzlocal


request = {"MaxResults": 50}
response = {
    "Parameters": [
        {
            "Name": "hello-world",
            "Type": "String",
            "LastModifiedDate": datetime.datetime(
                2022, 4, 1, 8, 44, 41, 706000, tzinfo=tzlocal()
            ),
            "LastModifiedUser": "arn:aws:iam::123456789012:user/mvanholsteijn",
            "Version": 1,
            "Tier": "Standard",
            "Policies": [],
            "DataType": "text",
        }
    ],
    "ResponseMetadata": {
        "RequestId": "f944bd7f-970c-4b63-bcaf-564df4dfbce7",
        "HTTPStatusCode": 200,
        "HTTPHeaders": {
            "server": "Server",
            "date": "Fri, 01 Apr 2022 06:45:07 GMT",
            "content-type": "application/x-amz-json-1.1",
            "content-length": "219",
            "connection": "keep-alive",
            "x-amzn-requestid": "f944bd7f-970c-4b63-bcaf-564df4dfbce7",
        },
        "RetryAttempts": 0,
    },
}
