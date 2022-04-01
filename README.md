# botocore stubber recorder
This library will allow you to record all the AWS API calls in a session, and generate a unittest.

Within the botocore library a [Stubber](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html) is provided. 
The stubber allows you to create unittest for pieces of code which call AWS APIs. The stub will
act as an endpoint, returning the appropriate response to each request in order.

However, using the stubs in your unittest is quite laborious. You have to record the requests and
responses, configure the stub and run the test. This library makes it pretty simple. 

## how to record all AWS API calls?
To record all AWS API calls is really simple. Just add the following snippet:

```python
import boto3
from botocore_stubber_recorder import BotoRecorder

session = boto3.session.Session()
recorder = BotoRecorder(session)
# ... do your thing with the session
for index, call in enumerate(recorder.calls):
   print(f"call {index +1}: {call.service_name}:{call.operation}")
```

## Generating a unittest
To generate a unittest, add the following snippet:

```python
from botocore_stubber_recorder import UnitTestGenerator

generator = UnitTestGenerator(name="my_example",directory="./tests")
generator.generate(recorder, anonimize=True)
```

This will generate the following file structure:
```text
tests
└── my_example
    ├── __init__.py
    ├── base.py
    ├── call_00001_describe_regions
    │   └── __init__.py
    ├── call_00002_describe_parameters
    │   └── __init__.py
    ├── call_00003_...
    │   └── __init__.py
    └── test_my_example.py
```
The `base.py` contains a base unittest class which initializes the stub with all the recorded
calls. Note that the `base.py` and the call directories are overwritten on each generate request. 
The `test_my_example.py` contains an example unittest implementation, which needs to be changed
to contain the actual test. The generated test, just tests that the stub is operational.

## formatting generated code
The generated code is formatted using black, if black is on the path.
## Run the generated test
You can now run, the generated test:
```shell
cd tests
python -munittest tests/my_example/test_my_example.py
```
```
WARNING:root:TODO: replace MyExampleUnitTest.test_my_example with the actual test. This just tests the generated code.
.
----------------------------------------------------------------------
Ran 1 test in 0.092s

OK
```
