Signaller
=========

Signals and slots implementation with asyncio support

Slots can be functions, methods or coroutines. Weak references are used by default.
If slot is coroutine, it will be scheduled to run asynchronously with ``asyncio.async()``
(but you must run event loop by yourself).

You can also run blocking functions asynchronously by specifying ``force_async=True`` when
connecting signal to slot (it will only apply to that slot) or when creating signal (it will
apply to all connected slots). ThreadPoolExecutor with 5 worker threads is used by default,
but it can be changed when creating signal with ``executor`` argument.

Requirements
------------

- Python >= 3.4

Usage
-----

Example:

.. code-block:: python

    import logging
    from signaller import Signal, autoconnect

    # Enable verbose logging
    logging.basicConfig(level=logging.DEBUG)

    # Creating signals (you can set signal name, but it is not required,
    # signals can be anonymous):
    sig_test = Signal('sig_test')
    
    # Connecting signals to slots (uses weak references by default,
    # but you can force strong references by specifying weak=False):
    def slot(arg):
        print('slot:', arg)

    sig_test.connect(slot)
    sig_test.connect(lambda arg: print('slot_lambda:', arg), weak=False)

    # You can also use decorators for connecting signals to slots:
    @sig_test.connect
    def slot2(arg):
        print('slot2:', arg)

    # And keyword arguments can be specified when using decorators too:
    @sig_test.connect(force_async=True)
    def slot3(arg):
        print('slot3:', arg)

    # You can also use decorators on methods, then signals will be connected to instance
    # methods automatically whenever new instance is created. But you must decorate class
    # with @autoconnect decorator for autoconnection to work. Class methods and
    # static methods are not supported.
    @autoconnect
    class Cls:
        @sig_test.connect
        def slot4(self, arg):
            print('slot4:', arg)

    obj = Cls()

    # Slots are automatically disconnected from signals
    # when using weak references:
    del slot

    # Or you can disconnect slots manually:
    sig_test.disconnect(slot2)

    # Emitting signals (you can send both positional and keyword
    # arguments to connected slots):
    sig_test.emit('Hello world!')

Output::

    INFO:signaller:Connecting signal <Signal 'sig_test' at 0x7f3c468bfc50> to slot <function slot at 0x7f3c46cc6f28>
    INFO:signaller:Connecting signal <Signal 'sig_test' at 0x7f3c468bfc50> to slot <function <lambda> at 0x7f3c468c97b8>
    INFO:signaller:Connecting signal <Signal 'sig_test' at 0x7f3c468bfc50> to slot <function slot2 at 0x7f3c43c9e400>
    INFO:signaller:Connecting signal <Signal 'sig_test' at 0x7f3c468bfc50> to slot <function slot3 at 0x7f3c43c9e598>
    DEBUG:signaller:Marking instance method <function Cls.slot4 at 0x7f3c43c9e6a8> for autoconnect to signal <Signal 'sig_test' at 0x7f3c468bfc50>
    INFO:signaller:Connecting signal <Signal 'sig_test' at 0x7f3c468bfc50> to slot <bound method Cls.slot4 of <__main__.Cls object at 0x7f3c43f11d30>>
    DEBUG:signaller:Object <function slot at 0x7f3c46cc6f28> has been deleted
    INFO:signaller:Disconnecting slot <Reference (weak) to <function slot at 0x7f3c46cc6f28> (dead)> from signal <Signal 'sig_test' at 0x7f3c468bfc50>
    INFO:signaller:Disconnecting slot <function slot2 at 0x7f3c43c9e400> from signal <Signal 'sig_test' at 0x7f3c468bfc50>
    INFO:signaller:Emitting signal <Signal 'sig_test' at 0x7f3c468bfc50>
    DEBUG:signaller:Calling slot <Reference (weak) to <function slot3 at 0x7f3c43c9e598>> asynchronously (in executor <concurrent.futures.thread.ThreadPoolExecutor object at 0x7f3c468bff28>)
    slot3: Hello world!
    DEBUG:signaller:Calling slot <Reference (strong) to <function <lambda> at 0x7f3c468c97b8>>
    slot_lambda: Hello world!
    DEBUG:signaller:Calling slot <Reference (weak) to <bound method Cls.slot4 of <__main__.Cls object at 0x7f3c43f11d30>>>
    slot4: Hello world!
