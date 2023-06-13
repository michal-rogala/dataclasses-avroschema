import datetime
import typing

from dataclasses_avroschema.avrodantic import AvroBaseModel


def test_one_to_one_relationship():
    """
    Test schema relationship one-to-one serialization
    """

    class Address(AvroBaseModel):
        "An Address"
        street: str
        street_number: int

    class User(AvroBaseModel):
        "An User with Address"
        name: str
        age: int
        address: Address

    address_data = {
        "street": "test",
        "street_number": 10,
    }

    address = Address(**address_data)

    data_user = {
        "name": "john",
        "age": 20,
        "address": address,
    }

    user = User(**data_user)

    avro_binary = b"\x08john(\x08test\x14"
    avro_json_binary = b'{"name": "john", "age": 20, "address": {"street": "test", "street_number": 10}}'
    expected = {"name": "john", "age": 20, "address": {"street": "test", "street_number": 10}}

    assert user.serialize() == avro_binary
    assert user.serialize(serialization_type="avro-json") == avro_json_binary

    assert User.deserialize(avro_binary, create_instance=False) == expected
    assert User.deserialize(avro_json_binary, serialization_type="avro-json", create_instance=False) == expected

    assert User.deserialize(avro_binary) == user
    assert User.deserialize(avro_json_binary, serialization_type="avro-json") == user

    assert user.to_dict() == expected


def test_one_to_many_relationship():
    """
    Test schema relationship one-to-many serialization
    """

    class Address(AvroBaseModel):
        "An Address"
        street: str
        street_number: int
        created_at: datetime.datetime

    class User(AvroBaseModel):
        "User with multiple Address"
        name: str
        age: int
        addresses: typing.List[Address]
        addresses_as_tuple: typing.Tuple[Address, ...]

    created_at = datetime.datetime(2019, 10, 12, 17, 57, 42, tzinfo=datetime.timezone.utc)
    address_data = {"street": "test", "street_number": 10, "created_at": created_at}

    address = Address(**address_data)
    second_address = Address(**address_data)

    data_user = {
        "name": "john",
        "age": 20,
        "addresses": [address],
        "addresses_as_tuple": (
            address,
            second_address,
        ),
    }

    user = User(**data_user)

    avro_binary = b"\x08john(\x02\x08test\x14\xe0\xd7\xf3\x91\xb8[\x00\x04\x08test\x14\xe0\xd7\xf3\x91\xb8[\x08test\x14\xe0\xd7\xf3\x91\xb8[\x00"  # noqa
    avro_json_binary = b'{"name": "john", "age": 20, "addresses": [{"street": "test", "street_number": 10, "created_at": 1570903062000}], "addresses_as_tuple": [{"street": "test", "street_number": 10, "created_at": 1570903062000}, {"street": "test", "street_number": 10, "created_at": 1570903062000}]}'  # noqa
    expected = {
        "name": "john",
        "age": 20,
        "addresses": [{"street": "test", "street_number": 10, "created_at": created_at}],
        "addresses_as_tuple": (
            {"street": "test", "street_number": 10, "created_at": created_at},
            {"street": "test", "street_number": 10, "created_at": created_at},
        ),
    }

    assert user.serialize() == avro_binary

    # Bug in fastavro
    assert user.serialize(serialization_type="avro-json") == avro_json_binary

    assert User.deserialize(avro_binary, create_instance=False) == expected
    assert User.deserialize(avro_json_binary, serialization_type="avro-json", create_instance=False) == expected

    assert User.deserialize(avro_binary) == user
    assert User.deserialize(avro_json_binary, serialization_type="avro-json") == user

    assert user.to_dict() == expected
    assert user.to_json()


def test_one_to_many_relationship_pydantic():
    """
    Test schema relationship one-to-many serialization
    """

    class Address(AvroBaseModel):
        "An Address"
        street: str
        street_number: int
        created_at: datetime.datetime

    class User(AvroBaseModel):
        "User with multiple Address"
        name: str
        age: int
        addresses: typing.List[Address]
        addresses_as_tuple: typing.Tuple[Address, ...]

    created_at = datetime.datetime(2019, 10, 12, 17, 57, 42, tzinfo=datetime.timezone.utc)
    address_data = {"street": "test", "street_number": 10, "created_at": created_at}

    address = Address(**address_data)
    second_address = Address(**address_data)

    data_user = {
        "name": "john",
        "age": 20,
        "addresses": [address],
        "addresses_as_tuple": (
            address,
            second_address,
        ),
    }

    user = User(**data_user)

    avro_binary = b"\x08john(\x02\x08test\x14\xe0\xd7\xf3\x91\xb8[\x00\x04\x08test\x14\xe0\xd7\xf3\x91\xb8[\x08test\x14\xe0\xd7\xf3\x91\xb8[\x00"  # noqa
    avro_json_binary = b'{"name": "john", "age": 20, "addresses": [{"street": "test", "street_number": 10, "created_at": 1570903062000}], "addresses_as_tuple": [{"street": "test", "street_number": 10, "created_at": 1570903062000}, {"street": "test", "street_number": 10, "created_at": 1570903062000}]}'  # noqa
    expected = {
        "name": "john",
        "age": 20,
        "addresses": [{"street": "test", "street_number": 10, "created_at": created_at}],
        "addresses_as_tuple": (
            {"street": "test", "street_number": 10, "created_at": created_at},
            {"street": "test", "street_number": 10, "created_at": created_at},
        ),
    }

    assert user.serialize() == avro_binary

    # Bug in fastavro
    assert user.serialize(serialization_type="avro-json") == avro_json_binary

    assert User.deserialize(avro_binary, create_instance=False) == expected
    assert User.deserialize(avro_json_binary, serialization_type="avro-json", create_instance=False) == expected

    assert User.deserialize(avro_binary) == user
    assert User.deserialize(avro_json_binary, serialization_type="avro-json") == user

    assert user.to_dict() == expected
    assert user.to_json()


def test_one_to_many_map_relationship():
    """
    Test schema relationship one-to-many using a map serialization
    """

    class Address(AvroBaseModel):
        "An Address"
        street: str
        street_number: int

    class User(AvroBaseModel):
        "User with multiple Address"
        name: str
        age: int
        addresses: typing.Dict[str, Address]

    address_data = {
        "street": "test",
        "street_number": 10,
    }

    address = Address(**address_data)

    data_user = {
        "name": "john",
        "age": 20,
        "addresses": {"main_residence": address},
    }

    user = User(**data_user)

    avro_binary = b"\x08john(\x02\x1cmain_residence\x08test\x14\x00"
    avro_json_binary = (
        b'{"name": "john", "age": 20, "addresses": {"main_residence": {"street": "test", "street_number": 10}}}'
    )
    expected = {"name": "john", "age": 20, "addresses": {"main_residence": {"street": "test", "street_number": 10}}}

    assert user.serialize() == avro_binary
    assert user.serialize(serialization_type="avro-json") == avro_json_binary

    # seems that there is a bug in fastavro and raises KeyError
    assert User.deserialize(avro_binary, create_instance=False) == expected
    assert User.deserialize(avro_json_binary, serialization_type="avro-json", create_instance=False) == expected

    assert User.deserialize(avro_binary) == user
    # assert User.deserialize(avro_json_binary) == user

    assert user.to_dict() == expected


def test_nested_schemas_splitted() -> None:
    """
    This test will cover the cases when nested schemas are
    used in a separate way.
    """

    class A(AvroBaseModel):
        class Meta:
            namespace = "namespace"

    class B(AvroBaseModel):
        a: A

    class C(AvroBaseModel):
        b: B
        a: A

    b = B(a=A())
    c = C(b=B(a=A()), a=A())

    assert b.serialize() == b""
    assert c.serialize() == b""


def test_nested_schemas_splitted_with_unions() -> None:
    """
    This test will cover the cases when nested schemas with Unions that are
    used in a separate way.
    """

    class S1(AvroBaseModel):
        pass

    class S2(AvroBaseModel):
        pass

    class A(AvroBaseModel):
        s: typing.Union[S1, S2]

        class Meta:
            namespace = "namespace"

    class B(AvroBaseModel):
        a: A

    class C(AvroBaseModel):
        b: B
        a: A

    b = B(a=A(s=S1()))
    c = C(b=B(a=A(s=S1())), a=A(s=S1()))

    assert b.serialize() == b"\x00"
    assert c.serialize() == b"\x00\x00"


def test_nested_scheamas_splitted_with_intermediates() -> None:
    class A(AvroBaseModel):
        class Meta:
            namespace = "namespace"

    class B(AvroBaseModel):
        a: A

    class C(AvroBaseModel):
        a: A

    class D(AvroBaseModel):
        b: B
        c: C

    a = A()
    b = B(a=a)
    c = C(a=a)
    d = D(b=b, c=c)

    assert d.serialize() == b""
    assert c.serialize() == b""


def test_nested_several_layers():
    class Friend(AvroBaseModel):
        name: str
        hobbies: typing.List[str]

    class User(AvroBaseModel):
        name: str
        friends: typing.List[Friend]

    user = User(name="Alex", friends=[Friend(name="Mr. Robot", hobbies=["fishing", "codding"])])

    assert User.deserialize(user.serialize()) == user
