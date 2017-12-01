#
# Autogenerated by Thrift
#
# DO NOT EDIT UNLESS YOU ARE SURE THAT YOU KNOW WHAT YOU ARE DOING
#  @generated
#

import typing as _typing
from thrift.py3.server import RequestContext, ServiceInterface
from abc import abstractmethod

import module.types as _module_types
import includes.types as _includes_types

_EmptyServiceInterfaceT = _typing.TypeVar('_EmptyServiceInterfaceT', bound='EmptyServiceInterface')


class EmptyServiceInterface(
    ServiceInterface
):


_ReturnServiceInterfaceT = _typing.TypeVar('_ReturnServiceInterfaceT', bound='ReturnServiceInterface')


class ReturnServiceInterface(
    ServiceInterface
):

    @staticmethod
    def pass_context_noReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def noReturn(
        self
    ) -> None: ...

    @staticmethod
    def pass_context_boolReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[bool]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[bool]]: ...

    @abstractmethod
    async def boolReturn(
        self
    ) -> bool: ...

    @staticmethod
    def pass_context_i16Return(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def i16Return(
        self
    ) -> int: ...

    @staticmethod
    def pass_context_i32Return(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def i32Return(
        self
    ) -> int: ...

    @staticmethod
    def pass_context_i64Return(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def i64Return(
        self
    ) -> int: ...

    @staticmethod
    def pass_context_floatReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[float]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[float]]: ...

    @abstractmethod
    async def floatReturn(
        self
    ) -> float: ...

    @staticmethod
    def pass_context_doubleReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[float]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[float]]: ...

    @abstractmethod
    async def doubleReturn(
        self
    ) -> float: ...

    @staticmethod
    def pass_context_stringReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[str]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[str]]: ...

    @abstractmethod
    async def stringReturn(
        self
    ) -> str: ...

    @staticmethod
    def pass_context_binaryReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[bytes]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[bytes]]: ...

    @abstractmethod
    async def binaryReturn(
        self
    ) -> bytes: ...

    @staticmethod
    def pass_context_mapReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_typing.Mapping[str, int]]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_typing.Mapping[str, int]]]: ...

    @abstractmethod
    async def mapReturn(
        self
    ) -> _typing.Mapping[str, int]: ...

    @staticmethod
    def pass_context_simpleTypedefReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def simpleTypedefReturn(
        self
    ) -> int: ...

    @staticmethod
    def pass_context_complexTypedefReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]: ...

    @abstractmethod
    async def complexTypedefReturn(
        self
    ) -> _typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]: ...

    @staticmethod
    def pass_context_list_mostComplexTypedefReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_typing.Sequence[_typing.Sequence[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_typing.Sequence[_typing.Sequence[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]]]: ...

    @abstractmethod
    async def list_mostComplexTypedefReturn(
        self
    ) -> _typing.Sequence[_typing.Sequence[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]: ...

    @staticmethod
    def pass_context_enumReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_module_types.MyEnumA]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_module_types.MyEnumA]]: ...

    @abstractmethod
    async def enumReturn(
        self
    ) -> _module_types.MyEnumA: ...

    @staticmethod
    def pass_context_list_EnumReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_typing.Sequence[_module_types.MyEnumA]]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_typing.Sequence[_module_types.MyEnumA]]]: ...

    @abstractmethod
    async def list_EnumReturn(
        self
    ) -> _typing.Sequence[_module_types.MyEnumA]: ...

    @staticmethod
    def pass_context_structReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_module_types.MyStruct]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_module_types.MyStruct]]: ...

    @abstractmethod
    async def structReturn(
        self
    ) -> _module_types.MyStruct: ...

    @staticmethod
    def pass_context_set_StructReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_typing.AbstractSet[_module_types.MyStruct]]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_typing.AbstractSet[_module_types.MyStruct]]]: ...

    @abstractmethod
    async def set_StructReturn(
        self
    ) -> _typing.AbstractSet[_module_types.MyStruct]: ...

    @staticmethod
    def pass_context_unionReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_module_types.ComplexUnion]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_module_types.ComplexUnion]]: ...

    @abstractmethod
    async def unionReturn(
        self
    ) -> _module_types.ComplexUnion: ...

    @staticmethod
    def pass_context_list_UnionReturn(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext],_typing.Awaitable[_typing.Sequence[_module_types.ComplexUnion]]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT],_typing.Awaitable[_typing.Sequence[_module_types.ComplexUnion]]]: ...

    @abstractmethod
    async def list_UnionReturn(
        self
    ) -> _typing.Sequence[_module_types.ComplexUnion]: ...

    @staticmethod
    def pass_context_readDataEb(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext, int],_typing.Awaitable[bytes]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT, int],_typing.Awaitable[bytes]]: ...

    @abstractmethod
    async def readDataEb(
        self,
        size: int
    ) -> bytes: ...

    @staticmethod
    def pass_context_readData(
        fn: _typing.Callable[[_ReturnServiceInterfaceT, RequestContext, int],_typing.Awaitable[bytes]]
    ) -> _typing.Callable[[_ReturnServiceInterfaceT, int],_typing.Awaitable[bytes]]: ...

    @abstractmethod
    async def readData(
        self,
        size: int
    ) -> bytes: ...


_ParamServiceInterfaceT = _typing.TypeVar('_ParamServiceInterfaceT', bound='ParamServiceInterface')


class ParamServiceInterface(
    ServiceInterface
):

    @staticmethod
    def pass_context_void_ret_i16_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_i16_param(
        self,
        param1: int
    ) -> None: ...

    @staticmethod
    def pass_context_void_ret_byte_i16_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int, int],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int, int],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_byte_i16_param(
        self,
        param1: int,
        param2: int
    ) -> None: ...

    @staticmethod
    def pass_context_void_ret_map_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Mapping[str, int]],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Mapping[str, int]],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_map_param(
        self,
        param1: _typing.Mapping[str, int]
    ) -> None: ...

    @staticmethod
    def pass_context_void_ret_map_setlist_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Mapping[str, int], _typing.AbstractSet[_typing.Sequence[str]]],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Mapping[str, int], _typing.AbstractSet[_typing.Sequence[str]]],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_map_setlist_param(
        self,
        param1: _typing.Mapping[str, int],
        param2: _typing.AbstractSet[_typing.Sequence[str]]
    ) -> None: ...

    @staticmethod
    def pass_context_void_ret_map_typedef_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_map_typedef_param(
        self,
        param1: int
    ) -> None: ...

    @staticmethod
    def pass_context_void_ret_enum_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _module_types.MyEnumA],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _module_types.MyEnumA],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_enum_param(
        self,
        param1: _module_types.MyEnumA
    ) -> None: ...

    @staticmethod
    def pass_context_void_ret_struct_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _module_types.MyStruct],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _module_types.MyStruct],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_struct_param(
        self,
        param1: _module_types.MyStruct
    ) -> None: ...

    @staticmethod
    def pass_context_void_ret_listunion_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Sequence[_module_types.ComplexUnion]],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Sequence[_module_types.ComplexUnion]],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def void_ret_listunion_param(
        self,
        param1: _typing.Sequence[_module_types.ComplexUnion]
    ) -> None: ...

    @staticmethod
    def pass_context_bool_ret_i32_i64_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int, int],_typing.Awaitable[bool]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int, int],_typing.Awaitable[bool]]: ...

    @abstractmethod
    async def bool_ret_i32_i64_param(
        self,
        param1: int,
        param2: int
    ) -> bool: ...

    @staticmethod
    def pass_context_bool_ret_map_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Mapping[str, int]],_typing.Awaitable[bool]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Mapping[str, int]],_typing.Awaitable[bool]]: ...

    @abstractmethod
    async def bool_ret_map_param(
        self,
        param1: _typing.Mapping[str, int]
    ) -> bool: ...

    @staticmethod
    def pass_context_bool_ret_union_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _module_types.ComplexUnion],_typing.Awaitable[bool]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _module_types.ComplexUnion],_typing.Awaitable[bool]]: ...

    @abstractmethod
    async def bool_ret_union_param(
        self,
        param1: _module_types.ComplexUnion
    ) -> bool: ...

    @staticmethod
    def pass_context_i64_ret_float_double_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, float, float],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, float, float],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def i64_ret_float_double_param(
        self,
        param1: float,
        param2: float
    ) -> int: ...

    @staticmethod
    def pass_context_i64_ret_string_typedef_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, str, _typing.AbstractSet[_typing.Sequence[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, str, _typing.AbstractSet[_typing.Sequence[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def i64_ret_string_typedef_param(
        self,
        param1: str,
        param2: _typing.AbstractSet[_typing.Sequence[_typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]]]
    ) -> int: ...

    @staticmethod
    def pass_context_i64_ret_i32_i32_i32_i32_i32_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int, int, int, int, int],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int, int, int, int, int],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def i64_ret_i32_i32_i32_i32_i32_param(
        self,
        param1: int,
        param2: int,
        param3: int,
        param4: int,
        param5: int
    ) -> int: ...

    @staticmethod
    def pass_context_double_ret_setstruct_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.AbstractSet[_module_types.MyStruct]],_typing.Awaitable[float]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.AbstractSet[_module_types.MyStruct]],_typing.Awaitable[float]]: ...

    @abstractmethod
    async def double_ret_setstruct_param(
        self,
        param1: _typing.AbstractSet[_module_types.MyStruct]
    ) -> float: ...

    @staticmethod
    def pass_context_string_ret_string_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, str],_typing.Awaitable[str]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, str],_typing.Awaitable[str]]: ...

    @abstractmethod
    async def string_ret_string_param(
        self,
        param1: str
    ) -> str: ...

    @staticmethod
    def pass_context_binary_ret_binary_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, bytes],_typing.Awaitable[bytes]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, bytes],_typing.Awaitable[bytes]]: ...

    @abstractmethod
    async def binary_ret_binary_param(
        self,
        param1: bytes
    ) -> bytes: ...

    @staticmethod
    def pass_context_map_ret_bool_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, bool],_typing.Awaitable[_typing.Mapping[str, int]]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, bool],_typing.Awaitable[_typing.Mapping[str, int]]]: ...

    @abstractmethod
    async def map_ret_bool_param(
        self,
        param1: bool
    ) -> _typing.Mapping[str, int]: ...

    @staticmethod
    def pass_context_list_ret_map_setlist_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Mapping[int, _typing.Sequence[str]], _typing.Sequence[str]],_typing.Awaitable[_typing.Sequence[bool]]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Mapping[int, _typing.Sequence[str]], _typing.Sequence[str]],_typing.Awaitable[_typing.Sequence[bool]]]: ...

    @abstractmethod
    async def list_ret_map_setlist_param(
        self,
        param1: _typing.Mapping[int, _typing.Sequence[str]],
        param2: _typing.Sequence[str]
    ) -> _typing.Sequence[bool]: ...

    @staticmethod
    def pass_context_mapsetlistmapliststring_ret_listlistlist_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Sequence[_typing.Sequence[_typing.Sequence[_typing.Sequence[int]]]]],_typing.Awaitable[_typing.Mapping[_typing.AbstractSet[_typing.Sequence[int]], _typing.Mapping[_typing.Sequence[_typing.AbstractSet[str]], str]]]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Sequence[_typing.Sequence[_typing.Sequence[_typing.Sequence[int]]]]],_typing.Awaitable[_typing.Mapping[_typing.AbstractSet[_typing.Sequence[int]], _typing.Mapping[_typing.Sequence[_typing.AbstractSet[str]], str]]]]: ...

    @abstractmethod
    async def mapsetlistmapliststring_ret_listlistlist_param(
        self,
        param1: _typing.Sequence[_typing.Sequence[_typing.Sequence[_typing.Sequence[int]]]]
    ) -> _typing.Mapping[_typing.AbstractSet[_typing.Sequence[int]], _typing.Mapping[_typing.Sequence[_typing.AbstractSet[str]], str]]: ...

    @staticmethod
    def pass_context_typedef_ret_i32_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int],_typing.Awaitable[int]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int],_typing.Awaitable[int]]: ...

    @abstractmethod
    async def typedef_ret_i32_param(
        self,
        param1: int
    ) -> int: ...

    @staticmethod
    def pass_context_listtypedef_ret_typedef_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]],_typing.Awaitable[_typing.Sequence[int]]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]],_typing.Awaitable[_typing.Sequence[int]]]: ...

    @abstractmethod
    async def listtypedef_ret_typedef_param(
        self,
        param1: _typing.Sequence[_typing.Mapping[_module_types.Empty, _module_types.MyStruct]]
    ) -> _typing.Sequence[int]: ...

    @staticmethod
    def pass_context_enum_ret_double_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, float],_typing.Awaitable[_module_types.MyEnumA]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, float],_typing.Awaitable[_module_types.MyEnumA]]: ...

    @abstractmethod
    async def enum_ret_double_param(
        self,
        param1: float
    ) -> _module_types.MyEnumA: ...

    @staticmethod
    def pass_context_enum_ret_double_enum_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, float, _module_types.MyEnumA],_typing.Awaitable[_module_types.MyEnumA]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, float, _module_types.MyEnumA],_typing.Awaitable[_module_types.MyEnumA]]: ...

    @abstractmethod
    async def enum_ret_double_enum_param(
        self,
        param1: float,
        param2: _module_types.MyEnumA
    ) -> _module_types.MyEnumA: ...

    @staticmethod
    def pass_context_listenum_ret_map_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.Mapping[str, int]],_typing.Awaitable[_typing.Sequence[_module_types.MyEnumA]]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.Mapping[str, int]],_typing.Awaitable[_typing.Sequence[_module_types.MyEnumA]]]: ...

    @abstractmethod
    async def listenum_ret_map_param(
        self,
        param1: _typing.Mapping[str, int]
    ) -> _typing.Sequence[_module_types.MyEnumA]: ...

    @staticmethod
    def pass_context_struct_ret_i16_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int],_typing.Awaitable[_module_types.MyStruct]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int],_typing.Awaitable[_module_types.MyStruct]]: ...

    @abstractmethod
    async def struct_ret_i16_param(
        self,
        param1: int
    ) -> _module_types.MyStruct: ...

    @staticmethod
    def pass_context_setstruct_ret_set_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, _typing.AbstractSet[str]],_typing.Awaitable[_typing.AbstractSet[_module_types.MyStruct]]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, _typing.AbstractSet[str]],_typing.Awaitable[_typing.AbstractSet[_module_types.MyStruct]]]: ...

    @abstractmethod
    async def setstruct_ret_set_param(
        self,
        param1: _typing.AbstractSet[str]
    ) -> _typing.AbstractSet[_module_types.MyStruct]: ...

    @staticmethod
    def pass_context_union_ret_i32_i32_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, int, int],_typing.Awaitable[_module_types.ComplexUnion]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, int, int],_typing.Awaitable[_module_types.ComplexUnion]]: ...

    @abstractmethod
    async def union_ret_i32_i32_param(
        self,
        param1: int,
        param2: int
    ) -> _module_types.ComplexUnion: ...

    @staticmethod
    def pass_context_listunion_string_param(
        fn: _typing.Callable[[_ParamServiceInterfaceT, RequestContext, str],_typing.Awaitable[_typing.Sequence[_module_types.ComplexUnion]]]
    ) -> _typing.Callable[[_ParamServiceInterfaceT, str],_typing.Awaitable[_typing.Sequence[_module_types.ComplexUnion]]]: ...

    @abstractmethod
    async def listunion_string_param(
        self,
        param1: str
    ) -> _typing.Sequence[_module_types.ComplexUnion]: ...


