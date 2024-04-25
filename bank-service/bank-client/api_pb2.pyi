from google.protobuf import timestamp_pb2 as _timestamp_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Action(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ACTION_UNSPECIFIED: _ClassVar[Action]
    ACTION_DEPOSIT: _ClassVar[Action]
    ACTION_WITHDRAWAL: _ClassVar[Action]
ACTION_UNSPECIFIED: Action
ACTION_DEPOSIT: Action
ACTION_WITHDRAWAL: Action

class Transaction(_message.Message):
    __slots__ = ("id", "amount", "time")
    ID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    TIME_FIELD_NUMBER: _ClassVar[int]
    id: str
    amount: float
    time: _timestamp_pb2.Timestamp
    def __init__(self, id: _Optional[str] = ..., amount: _Optional[float] = ..., time: _Optional[_Union[_timestamp_pb2.Timestamp, _Mapping]] = ...) -> None: ...

class CreateAccountRequest(_message.Message):
    __slots__ = ("name", "password")
    NAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    name: str
    password: str
    def __init__(self, name: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class CreateAccountResponse(_message.Message):
    __slots__ = ("accountId", "name")
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    accountId: str
    name: str
    def __init__(self, accountId: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class TransactionRequest(_message.Message):
    __slots__ = ("action", "accountId", "amount")
    ACTION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    action: Action
    accountId: str
    amount: float
    def __init__(self, action: _Optional[_Union[Action, str]] = ..., accountId: _Optional[str] = ..., amount: _Optional[float] = ...) -> None: ...

class TransactionResponse(_message.Message):
    __slots__ = ("transaction", "accountBalance")
    TRANSACTION_FIELD_NUMBER: _ClassVar[int]
    ACCOUNTBALANCE_FIELD_NUMBER: _ClassVar[int]
    transaction: Transaction
    accountBalance: float
    def __init__(self, transaction: _Optional[_Union[Transaction, _Mapping]] = ..., accountBalance: _Optional[float] = ...) -> None: ...

class TransferRequest(_message.Message):
    __slots__ = ("sourceAccountId", "targetAccountId", "value", "password")
    SOURCEACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    TARGETACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    sourceAccountId: str
    targetAccountId: str
    value: float
    password: str
    def __init__(self, sourceAccountId: _Optional[str] = ..., targetAccountId: _Optional[str] = ..., value: _Optional[float] = ..., password: _Optional[str] = ...) -> None: ...

class BankStatementRequest(_message.Message):
    __slots__ = ("accountId", "password")
    ACCOUNTID_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    accountId: str
    password: str
    def __init__(self, accountId: _Optional[str] = ..., password: _Optional[str] = ...) -> None: ...

class BankStatementResponse(_message.Message):
    __slots__ = ("transactions", "amount")
    TRANSACTIONS_FIELD_NUMBER: _ClassVar[int]
    AMOUNT_FIELD_NUMBER: _ClassVar[int]
    transactions: _containers.RepeatedCompositeFieldContainer[Transaction]
    amount: float
    def __init__(self, transactions: _Optional[_Iterable[_Union[Transaction, _Mapping]]] = ..., amount: _Optional[float] = ...) -> None: ...
