import asyncio
from abc import ABCMeta, abstractmethod
from typing import Literal, Union, Any, Iterable, Callable


class AbstractParser(metaclass=ABCMeta):
    @abstractmethod
    def parse(self):
        pass

    @abstractmethod
    def parse_new(self):
        pass


class AsyncAbstractParser(metaclass=ABCMeta):
    @abstractmethod
    async def parse(self):
        pass

    @abstractmethod
    async def parse_new(self):
        pass


class ParserList:
    def __init__(self, *items: Union[AbstractParser, AsyncAbstractParser, "ParserList"],
                 mode: Literal['new'] | Literal['union'] = 'new'):
        match mode:
            case 'new':
                parsers = items
            case 'union':
                parsers = []
                for plist in items:
                    parsers.extend(plist.async_parsers)
                    parsers.extend(plist.sync_parsers)
            case _:
                ValueError('mode must be either "new" or "union"')

        self.__sort_parsers(parsers)  # it will create self.sync_parsers and self.async_parsers

    def __sort_parsers(self, parsers: Iterable[AbstractParser | AsyncAbstractParser]) -> None:
        """
        Creates self.sync_parsers and self.async_parsers
        It's vital for self._run_tasks_async.
        Sorting is performed depending on the base class: AbstractParser or AsyncAbstractParser.

        :param parsers: iterable of parsers
        """

        self.sync_parsers = []
        self.async_parsers = []
        for p in parsers:
            if isinstance(p, AsyncAbstractParser):
                self.async_parsers.append(p)
            elif isinstance(p, AbstractParser):
                self.sync_parsers.append(p)
            else:
                raise ValueError(f'parser base type {type(p)} not supported')

    def parse(self) -> list[Any]:
        """
        Use the parse() method from all parsers.
        :return: One-dimensional list of parsed posts
        """
        async_tasks = [p.parse for p in self.async_parsers]
        sync_tasks = [p.parse for p in self.sync_parsers]

        return asyncio.run(self._run_tasks_async(async_tasks, sync_tasks))

    def parse_new(self) -> list[Any]:
        """
        Use the parse_new() method from all parsers.
        :return: One-dimensional list of parsed posts
        """
        async_tasks = [p.parse_new for p in self.async_parsers]
        sync_tasks = [p.parse_new for p in self.sync_parsers]

        return asyncio.run(self._run_tasks_async(async_tasks, sync_tasks))

    async def _run_tasks_async(self, async_tasks: list[Callable], sync_tasks: list[Callable]) -> list[Any]:
        """
        Runs all tasks. Synchronous parsers are ran while asynchronous are being awaited.

        :param async_tasks: list of parse asynchronous functions
        :param sync_tasks: list of parse synchronous functions
        :return: results of parsing
        """
        sync_tasks = map(self._wrap_sync, sync_tasks)
        async_tasks = [task() for task in async_tasks]  # create coroutines

        posts = await asyncio.gather(*async_tasks, *sync_tasks)
        res = []
        for p in posts:  # make res a list of posts instead of a list of lists of posts
            res.extend(p)

        return res

    async def _wrap_sync(self, func):
        return func()
