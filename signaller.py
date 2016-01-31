"""Signals and slots implementation with asyncio support

Slots can be functions, methods or coroutines. Weak references are used by default.
If slot is coroutine, it will be scheduled to run asynchronously with ``asyncio.async()``
(but you must run event loop by yourself).

You can also run blocking functions asynchronously by specifying ``force_async=True`` when
connecting signal to slot (it will only apply to that slot) or when creating signal (it will
apply to all connected slots). ThreadPoolExecutor with 5 worker threads is used by default,
but it can be changed when creating signal with ``executor`` argument.
"""

import asyncio, concurrent.futures, weakref, inspect, logging

logger = logging.getLogger(__name__)


class Reference:
    """Weak or strong reference to function or method"""
    def __init__(self, obj, callback=None, weak=True, force_async=False):
        if not callable(obj):
            raise TypeError('obj has to be callable')

        self.force_async = force_async
        self._weak = weak
        self._alive = True
        self._hash = obj.__hash__()
        self._repr = obj.__repr__()

        if self.weak:
            if inspect.ismethod(obj):
                self._ref = weakref.WeakMethod(obj, self._wrap_callback(callback))
            else:
                self._ref = weakref.ref(obj, self._wrap_callback(callback))
        else:
            self._ref = obj

    def _wrap_callback(self, callback):
        """Wrap callback to be called with reference to ourselves, not underlying weakref object"""
        def wrapper(obj):
            logger.debug('Object {} has been deleted'.format(self._repr))
            self._alive = False
            if callback is not None:
                return callback(self)
        return wrapper

    @property
    def weak(self):
        """Returns True if this is weak reference"""
        return self._weak

    @property
    def alive(self):
        """Returns True if underlying weak reference is still alive"""
        return self._alive

    def getobject(self):
        """Returns underlying object"""
        return self._ref() if self.weak else self._ref

    def __call__(self, *args, **kwargs):
        return self.getobject()(*args, **kwargs)

    def __hash__(self):
        return self._hash

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __repr__(self):
        return '<Reference ({}) to {}{}>'.format(
            'weak' if self.weak else 'strong',
            self._repr,
            ' (dead)' if not self.alive else ''
        )


class Signal:
    """Signal emitter"""
    def __init__(self, name='', loop=None, force_async=False, executor=None):
        self.name = name
        self.loop = loop
        self.force_async = force_async
        self.executor = executor or concurrent.futures.ThreadPoolExecutor(max_workers=5)
        self._slots = set()

    def emit(self, *args, **kwargs):
        """Emit signal (call all connected slots)"""
        logger.info('Emitting signal {}'.format(self))
        for ref in self._slots:
            if asyncio.iscoroutinefunction(ref.getobject()):
                logger.debug('Scheduling coroutine {}'.format(ref))
                asyncio.async(ref(*args, **kwargs), loop=self.loop)
            else:
                if self.force_async or ref.force_async:
                    logger.debug('Calling slot {} asynchronously (in executor {})'.format(
                        ref, self.executor
                    ))
                    self.executor.submit(ref, *args, **kwargs)
                else:
                    logger.debug('Calling slot {}'.format(ref))
                    ref(*args, **kwargs)

    def clear(self):
        """Disconnect all slots"""
        logger.info('Disconnecting all slots from signal {}'.format(self))
        self._slots.clear()

    def connect(self, *args, weak=True, force_async=False):
        """Connect signal to slot (can be also used as decorator)"""
        def wrapper(func):
            logger.info('Connecting signal {} to slot {}'.format(self, func))
            self._slots.add(
                Reference(func, callback=self.disconnect, weak=weak, force_async=force_async)
            )
            return func

        # If there is one (and only one) positional argument and this argument is callable,
        # assume it is the decorator (without any optional keyword arguments)
        if len(args) == 1 and callable(args[0]):
            return wrapper(args[0])
        else:
            return wrapper

    def disconnect(self, slot):
        """Disconnect slot from signal"""
        try:
            logger.info('Disconnecting slot {} from signal {}'.format(slot, self))
            self._slots.remove(slot)
        except KeyError:
            logger.warning('Slot {} is not connected!'.format(slot))
            pass

    def __repr__(self):
        return '<Signal {} at {}>'.format(
            '\'{}\''.format(self.name) if self.name else '<anonymous>',
            hex(id(self))
        )
