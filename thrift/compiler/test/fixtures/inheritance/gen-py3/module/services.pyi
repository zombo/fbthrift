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

_MyRootInterfaceT = _typing.TypeVar('_MyRootInterfaceT', bound='MyRootInterface')


class MyRootInterface(
    ServiceInterface
):

    @staticmethod
    def pass_context_do_root(
        fn: _typing.Callable[[_MyRootInterfaceT, RequestContext],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_MyRootInterfaceT],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def do_root(
        self
    ) -> None: ...


_MyNodeInterfaceT = _typing.TypeVar('_MyNodeInterfaceT', bound='MyNodeInterface')


class MyNodeInterface(
    _module_services.MyRootInterface
):

    @staticmethod
    def pass_context_do_mid(
        fn: _typing.Callable[[_MyNodeInterfaceT, RequestContext],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_MyNodeInterfaceT],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def do_mid(
        self
    ) -> None: ...


_MyLeafInterfaceT = _typing.TypeVar('_MyLeafInterfaceT', bound='MyLeafInterface')


class MyLeafInterface(
    _module_services.MyNodeInterface
):

    @staticmethod
    def pass_context_do_leaf(
        fn: _typing.Callable[[_MyLeafInterfaceT, RequestContext],_typing.Awaitable[None]]
    ) -> _typing.Callable[[_MyLeafInterfaceT],_typing.Awaitable[None]]: ...

    @abstractmethod
    async def do_leaf(
        self
    ) -> None: ...


