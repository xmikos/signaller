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

    from signaller import Signal

    logging.basicConfig(level=logging.DEBUG)

    def slot(arg):
        print('slot:', arg)

    # Creating signals (you can set signal name, but it is not required,
    # signals can be anonymous):
    sig_test = Signal('sig_test')
    
    # Connecting signals to slots (uses weak references by default,
    # but you can force strong references by specifying weak=False):
    sig_test.connect(slot)
    sig_test.connect(lambda arg: print('slot_lambda:', arg), weak=False)

    # You can also use decorators for connecting signals to slots:
    @sig_test.connect
    def slot2(arg):
        print('slot2:', arg)

    # And weak=False can be specified when using decorators too:
    @sig_test.connect(weak=False)
    def slot3(arg):
        print('slot3:', arg)

    # Slots are automatically disconnected from signals
    # when using weak references:
    del slot2

    # Or you can disconnect slots manually:
    sig_test.disconnect(slot3)

    # Emitting signals (you can send positional and keyword
    # arguments to connected slots):
    sig_test.emit('Hello world!')

Output::

    INFO:__main__:Connecting signal <Signal 'sig_test' at 0x7fc31dcdef98> to slot <function slot at 0x7fc31dceeae8>
    INFO:__main__:Connecting signal <Signal 'sig_test' at 0x7fc31dcdef98> to slot <function <lambda> at 0x7fc31b03a1e0>
    INFO:__main__:Connecting signal <Signal 'sig_test' at 0x7fc31dcdef98> to slot <function slot2 at 0x7fc31b03a2f0>
    INFO:__main__:Connecting signal <Signal 'sig_test' at 0x7fc31dcdef98> to slot <function slot3 at 0x7fc31b03a488>
    DEBUG:__main__:Object <function slot2 at 0x7fc31b03a2f0> has been deleted
    INFO:__main__:Disconnecting slot <Reference (weak) to <function slot2 at 0x7fc31b03a2f0> (dead)> from signal <Signal 'sig_test' at 0x7fc31dcdef98>
    INFO:__main__:Disconnecting slot <function slot3 at 0x7fc31b03a488> from signal <Signal 'sig_test' at 0x7fc31dcdef98>
    INFO:__main__:Emitting signal <Signal 'sig_test' at 0x7fc31dcdef98>
    DEBUG:__main__:Calling slot <Reference (weak) to <function slot at 0x7fc31dceeae8>>
    slot: Hello world!
    DEBUG:__main__:Calling slot <Reference (strong) to <function <lambda> at 0x7fc31b03a1e0>>
    slot_lambda: Hello world!
