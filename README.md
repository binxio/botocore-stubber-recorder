# botocore stubber recorder
This library will allow you to record all the AWS API calls in a session, and generate a unittest.

Within the botocore library a [Stubber](https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html) is provided. 
The stubber allows you to create unittest for pieces of code which call AWS APIs. The stub will
act as an endpoint, returning the appropriate response to each request in order.

However, using the stubs in your unittest is quite laborious. You have to record the requests and
responses, configure the stub and run the test. This library makes it pretty simple. 

## getting started
To start, type:

```
$ botocore-stubber-recorder --test-name show_me_how
INFO:root:sketelon test sts_get_caller written in ./tests
```

This generates the following files:
```
$ tree tests 
tests
├── __init__.py
└── show_me_how
    ├── __init__.py
    ├── base.py
    ├── call_00001_get_caller_identity
    │   └── __init__.py
    └── test_show_me_how.py
```

You can now start writing your unit test in `test_sts_get_caller.py`. By running
the unit test with `self.record = True` or the environment variable
`RECORD_UNITTEST_STUBS=true` it will re-record the stubs for you.


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
generator.generate(recorder, anonimize=True, unflatten=True)
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
to contain the actual test. The generated test just tests that the generated stub: you
have to replace the method `test_my_example` with a functional test.

## Run the generated test
You can now run, the generated test:
```shell
cd tests
python -munittest ./my_example/test_my_example.py
```
```
WARNING:root:TODO: replace MyExampleUnitTest.test_my_example with the actual test. This just tests the generated code.
.
----------------------------------------------------------------------
Ran 1 test in 0.092s

OK
```
Now, edit the test in `tests/my_example/test_my_example.py` to implement the actual unittest.

## recording the responses
If you want to re-record the AWS API stubs, set the environment variable RECORD_UNITTEST_STUBS to `true`.

```
RECORD_UNITTEST_STUBS=true python -munittest ./my_example/test_my_example.py
```
This will allow you to change the implementation of the unit test, and easily record
the calls.

## all at once
To record and generated the unittest in a single command, use:

```python
import boto3
from botocore_stubber_recorder import BotoRecorderUnitTestGenerator

session = boto3.session.Session()

with BotoRecorderUnitTestGenerator("my_example", session) as generator:
    ## do your thing with the session
```

## generated code format
The generated code is formatted using black, if [black](https://black.readthedocs.io/) is on the path.
