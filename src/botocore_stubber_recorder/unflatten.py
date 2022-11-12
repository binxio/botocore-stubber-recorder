import re


def unflattener(data: dict) -> dict:
    """
    an attempt to unflatten the botocore flattened request dictionaries. AFAICS, there is
    no deserialize available in the botocore library and the event emitters do not provide
    access to the original request parameters.

    if the value of the attribute is a list, the name of the attribute will be put in plural
    form.

    adapted from https://github.com/simonw/json-flatten

    >>> unflattener({"a.0": 1, "a.1": 2, "b": "no"})
    {'as': [1, 2], 'b': 'no'}
    >>> unflattener({'Filter.1.Name': 'name', 'Filter.1.Value.1': 'Windows_Server-2016-English-Full-Base-*', 'Filter.2.Name': 'state', 'Filter.2.Value.1': 'available', 'Filter.3.Name': 'virtualization-type', 'Filter.3.Value.1': 'hvm', 'Filter.4.Name': 'root-device-type', 'Filter.4.Value.1': 'ebs'})
    {'Filters': [{'Name': 'name', 'Values': ['Windows_Server-2016-English-Full-Base-*']}, {'Name': 'state', 'Values': ['available']}, {'Name': 'virtualization-type', 'Values': ['hvm']}, {'Name': 'root-device-type', 'Values': ['ebs']}]}
    """
    obj = {}
    for key, value in data.items():
        current = obj
        bits = key.split(".")
        path, lastkey = bits[:-1], bits[-1]
        for bit in path:
            current[bit] = current.get(bit) or {}
            current = current[bit]
        # Now deal with $type suffixes:
        if _types_re.match(lastkey):
            lastkey, lasttype = lastkey.rsplit("$", 2)
            value = {
                "int": int,
                "float": float,
                "empty": lambda v: {},
                "bool": lambda v: v.lower() == "true",
                "none": lambda v: None,
            }.get(lasttype, lambda v: v)(value)
        current[lastkey] = value

    # We handle foo.0.one, foo.1.two syntax in a second pass,
    # by iterating through our structure looking for dictionaries
    # where all of the keys are stringified integers
    def replace_integer_keyed_dicts_with_lists(obj):
        if isinstance(obj, dict):
            if obj and all(k.isdigit() for k in obj):
                return [
                    i[1]
                    for i in sorted(
                        [
                            (int(k), replace_integer_keyed_dicts_with_lists(v))
                            for k, v in obj.items()
                        ]
                    )
                ]
            else:
                return dict(
                    (k, replace_integer_keyed_dicts_with_lists(v))
                    for k, v in obj.items()
                )
        elif isinstance(obj, list):
            return [replace_integer_keyed_dicts_with_lists(v) for v in obj]
        else:
            return obj

    def replace_key_of_list_with_plurar(obj) -> object:
        if isinstance(obj, dict):
            result = {}
            for key, value in obj.items():
                name = f"{key}s" if isinstance(value, list) else key
                result[name] = replace_key_of_list_with_plurar(value)
            return result
        elif isinstance(obj, list):
            return [replace_key_of_list_with_plurar(o) for o in obj]
        else:
            return obj

    obj = replace_key_of_list_with_plurar(replace_integer_keyed_dicts_with_lists(obj))

    # Handle root units only, e.g. {'$empty': '{}'}
    if list(obj.keys()) == [""]:
        return obj.values()[0]
    return obj


_types_re = re.compile(r".*\$(none|bool|int|float|empty)$")
