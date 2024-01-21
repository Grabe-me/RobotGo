from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class Motion(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    ERROR: _ClassVar[Motion]
    RIGHT: _ClassVar[Motion]
    DOWN: _ClassVar[Motion]
    LEFT: _ClassVar[Motion]
    UP: _ClassVar[Motion]
    FINISH: _ClassVar[Motion]
ERROR: Motion
RIGHT: Motion
DOWN: Motion
LEFT: Motion
UP: Motion
FINISH: Motion

class Empty(_message.Message):
    __slots__ = ()
    def __init__(self) -> None: ...

class Point(_message.Message):
    __slots__ = ("i", "j")
    I_FIELD_NUMBER: _ClassVar[int]
    J_FIELD_NUMBER: _ClassVar[int]
    i: int
    j: int
    def __init__(self, i: _Optional[int] = ..., j: _Optional[int] = ...) -> None: ...

class Field(_message.Message):
    __slots__ = ("N", "M", "grid", "source")
    N_FIELD_NUMBER: _ClassVar[int]
    M_FIELD_NUMBER: _ClassVar[int]
    GRID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_FIELD_NUMBER: _ClassVar[int]
    N: int
    M: int
    grid: str
    source: Point
    def __init__(self, N: _Optional[int] = ..., M: _Optional[int] = ..., grid: _Optional[str] = ..., source: _Optional[_Union[Point, _Mapping]] = ...) -> None: ...

class MoveRequest(_message.Message):
    __slots__ = ("targets",)
    TARGETS_FIELD_NUMBER: _ClassVar[int]
    targets: _containers.RepeatedCompositeFieldContainer[Point]
    def __init__(self, targets: _Optional[_Iterable[_Union[Point, _Mapping]]] = ...) -> None: ...

class MoveResponse(_message.Message):
    __slots__ = ("direction",)
    DIRECTION_FIELD_NUMBER: _ClassVar[int]
    direction: Motion
    def __init__(self, direction: _Optional[_Union[Motion, str]] = ...) -> None: ...
