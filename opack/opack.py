from opack.opack_construct import OPack


def loads(opack_bytes: bytes) -> dict:
    return OPack.parse(opack_bytes).value


def dumps(obj) -> bytes:
    return OPack.build(obj)
