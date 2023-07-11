from datetime import datetime, timezone

from opack.exceptions import InvalidTypeError
from opack.opack import dumps, loads


def do_test_dumps_loads(loaded_value, expected_dumped_value):
    dumped_value = dumps(loaded_value)
    assert dumped_value == expected_dumped_value
    assert loads(dumped_value) == loaded_value


def test_bool():
    do_test_dumps_loads(True, b'\x01')
    do_test_dumps_loads(False, b'\x02')


def test_datetime():
    do_test_dumps_loads(datetime(year=1970, month=1, day=1, tzinfo=timezone.utc), b'\x06\x00\x00\x00 l\t\xdfA')


def test_string():
    do_test_dumps_loads('a', b'Aa'),
    do_test_dumps_loads('a' * 33, b'a!' + b'a' * 33),
    do_test_dumps_loads('a' * 2 ** 8, b'b\x01\x00' + b'a' * 2 ** 8),


def test_number():
    do_test_dumps_loads(1, b'\t'),
    do_test_dumps_loads(40, b'0('),
    do_test_dumps_loads(2 ** 8, b'2\x00\x01\x00\x00'),
    do_test_dumps_loads(2 ** 32, b'3\x00\x00\x00\x00\x01\x00\x00\x00'),
    do_test_dumps_loads(2 ** 53, b'3\x00\x00\x00\x00\x00\x00 \x00'),
    do_test_dumps_loads(-1, b'5\x00\x00\x80\xbf'),
    do_test_dumps_loads(1.2, b'6333333\xf3?'),


def test_bytes():
    do_test_dumps_loads(b'\x01', b'q\x01'),
    do_test_dumps_loads(b'\x01' * 33, b'\x91!' + b'\x01' * 33),
    do_test_dumps_loads(b'\x01' * 2 ** 8, b'\x92\x01\x00' + b'\x01' * 2 ** 8),
    do_test_dumps_loads(b'\x01' * 2 ** 16, b'\x93\x00\x01\x00\x00' + b'\x01' * 2 ** 16),


def test_list():
    do_test_dumps_loads([1], b'\xd1\t'),
    do_test_dumps_loads([1] * 15, b'\xdf\t\t\t\t\t\t\t\t\t\t\t\t\t\t\t\x03'),
    do_test_dumps_loads([True, False, 1, -1, [1], {5: 5}, b'a', 2 ** 8, True, -100, False, True, 0.3, 'hello', 'world'],
                        b'\xdf\x01\x02\t5\x00\x00\x80\xbf\xd1\t\xe1\r\rqa2\x00\x01\x00\x00\x015\x00\x00\xc8\xc2\x02'
                        b'\x016333333\xd3?EhelloEworld\x03')


def test_dict():
    do_test_dumps_loads({1: 1}, b'\xe1\t\t'),
    do_test_dumps_loads({1: 1, 'a': 'b', 2: {2: 3}, 3: b'hello', 4: b'a' * 20, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 10,
                         11: ['a', True, b'a'],
                         12: False, 13: True, 14: -1, 15: 0.1},
                        b'\xef\t\tAaAb\n\xe1\n\x0b\x0buhello\x0c\x84aaaaaaaaaaaaaaaaaaaa\r\r\x0e\x0e\x0f\x0f\x10\x10'
                        b'\x11\x11\x12\x12\x13\xd3Aa\x01qa\x14\x02\x15\x01\x165\x00\x00\x80\xbf\x176\x9a\x99\x99\x99'
                        b'\x99\x99\xb9?\x03\x03')


def test_invalid_input():
    try:
        loads(b'\x04\x04')
        assert False
    except InvalidTypeError:
        pass
