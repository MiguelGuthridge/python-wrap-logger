"""
Tests for the "logginess" of WrapLogger
"""
from jestspectation import Equals, StringContaining
import pytest
from pytest import CaptureFixture
from wrap_logger import wrap
from .helpers import Simple


def test_capture_read(capsys: CaptureFixture):
    """Are basic property accesses logged"""
    wrapped = wrap(Simple())
    wrapped.value

    capture = capsys.readouterr()

    assert capture.out.strip() == '\n'.join([
        "[WRAP LOG] > Get  simple.value",
        "[WRAP LOG] < Get  simple.value: gave 42",
    ])


def test_capture_non_existent_read(capsys: CaptureFixture):
    """Are exceptions logged for invalid reads"""
    wrapped = wrap(Simple())

    with pytest.raises(AttributeError):
        wrapped.invalid  # type: ignore

    capture = capsys.readouterr()
    assert capture.out.strip() == '\n'.join([
        "[WRAP LOG] > Get  simple.invalid",
        "[WRAP LOG] < Get  simple.invalid: raised "
        """AttributeError("'Simple' object has no attribute 'invalid'")""",
    ])


def test_capture_write(capsys: CaptureFixture):
    """Are basic writes logged?"""
    wrapped = wrap(Simple())
    wrapped.value = 43

    capture = capsys.readouterr()
    assert capture.out.strip() == '\n'.join([
        "[WRAP LOG] > Set  simple.value: 42 -> 43",
        "[WRAP LOG] < Set  simple.value",
    ])


def test_capture_non_existent_write(capsys: CaptureFixture):
    """Are basic writes logged for properties that didn't exist before?"""
    wrapped = wrap(Simple())
    wrapped.new = 43  # type: ignore

    capture = capsys.readouterr()
    assert capture.out.strip() == '\n'.join([
        "[WRAP LOG] > Set  simple.new: [unassigned] -> 43",
        "[WRAP LOG] < Set  simple.new",
    ])


def test_capture_call(capsys: CaptureFixture):
    """Are object calls logged?"""
    wrapped = wrap(Simple())

    wrapped(1, 2, a=3, b=4)

    capture = capsys.readouterr()
    assert capture.out.strip() == '\n'.join([
        '[WRAP LOG] > Call simple(1, 2, a=3, b=4)',
        '[WRAP LOG] < Call simple(1, 2, a=3, b=4): returned 10',
    ])


def test_capture_call_method(capsys: CaptureFixture):
    """Are object calls logged?"""
    wrapped = wrap(Simple())

    wrapped.echo("hi")

    capture = capsys.readouterr()
    assert capture.out.strip() == '\n'.join([
        "[WRAP LOG] > Get  simple.echo",
        "[WRAP LOG] < Get  simple.echo: gave "
        "<bound method Simple.echo of simple>",
        "[WRAP LOG] > Call simple.echo('hi')",
        "[WRAP LOG] < Call simple.echo('hi'): returned 'hi'",
    ])


def test_capture_module_function(capsys: CaptureFixture):
    """Are function calls from wrapped modules logged?"""
    from . import example_module
    wrapped = wrap(example_module)

    wrapped.foo()

    capture = capsys.readouterr()
    assert capture.out.strip().splitlines() == Equals([
        "[WRAP LOG] > Get  tests.example_module.foo",
        StringContaining(
            "[WRAP LOG] < Get  tests.example_module.foo: gave "
            "<function foo at 0x"
        ),
        "[WRAP LOG] > Call tests.example_module.foo()",
        "[WRAP LOG] < Call tests.example_module.foo(): returned 42",
    ])
