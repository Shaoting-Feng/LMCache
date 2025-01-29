import struct
from dataclasses import dataclass

import torch

from lmcache.experimental.memory_management import MemoryFormat
from lmcache.utils import CacheEngineKey

MAX_KEY_LENGTH = 150


class Constants:
    CLIENT_PUT = 1
    CLIENT_GET = 2
    CLIENT_EXIST = 3
    CLIENT_LIST = 4

    SERVER_SUCCESS = 200
    SERVER_FAIL = 400


DTYPE_TO_INT = {
    torch.half: 1,
    torch.float16: 2,
    torch.bfloat16: 3,
    torch.float: 4,
    torch.float32: 4,
    torch.float64: 5,
    torch.double: 5,
    torch.uint8: 6,
    torch.float8_e4m3fn: 7,
    torch.float8_e5m2: 8,
}

INT_TO_DTYPE = {
    1: torch.half,
    2: torch.float16,
    3: torch.bfloat16,
    4: torch.float,
    5: torch.float64,
    6: torch.uint8,
    7: torch.float8_e4m3fn,
    8: torch.float8_e5m2,
}


@dataclass
class ClientMetaMessage:
    """
    Control message from LMCServerConnector to LMCacheServer
    """

    command: int
    key: CacheEngineKey
    length: int
    fmt: MemoryFormat
    dtype: torch.dtype
    shape: torch.Size

    def serialize(self) -> bytes:
        key_str = self.key.to_string()
        assert (
            len(key_str) <= MAX_KEY_LENGTH
        ), f"Key length {len(key_str)} exceeds maximum {MAX_KEY_LENGTH}"

        # NOTE(Jiayi): 4 is the maximum dimension of memory object.
        # Pass in shape [x, 0, 0, 0] if it is a bytes memory object
        assert (len(self.shape) == 4), "Shape dimension should be 4"

        packed_bytes = struct.pack(
            f"iiiiiiii{MAX_KEY_LENGTH}s",
            self.command,
            self.length,
            int(self.fmt.value),
            DTYPE_TO_INT[self.dtype],
            self.shape[0],
            self.shape[1],
            self.shape[2],
            self.shape[3],
            key_str.encode().ljust(MAX_KEY_LENGTH),
        )
        return packed_bytes

    @staticmethod
    def deserialize(s: bytes) -> "ClientMetaMessage":
        command, length, fmt, dtype, shape0, shape1, shape2, shape3, key = \
            struct.unpack(f"iiiiiiii{MAX_KEY_LENGTH}s", s)
        return ClientMetaMessage(
            command, CacheEngineKey.from_string(key.decode().strip()), length,
            MemoryFormat(fmt), INT_TO_DTYPE[dtype],
            torch.Size([shape0, shape1, shape2, shape3]))

    @staticmethod
    def packlength() -> int:
        # NOTE: 8 is the number of integers
        return 4 * 8 + MAX_KEY_LENGTH


@dataclass
class ServerMetaMessage:
    """
    Control message from LMCacheServer to LMCServerConnector
    """

    code: int
    length: int
    fmt: MemoryFormat
    dtype: torch.dtype
    shape: torch.Size

    def serialize(self) -> bytes:
        assert (len(self.shape) == 4), "Shape dimension should be 4"
        packed_bytes = struct.pack(
            "iiiiiiii",
            self.code,
            self.length,
            int(self.fmt.value),
            DTYPE_TO_INT[self.dtype],
            self.shape[0],
            self.shape[1],
            self.shape[2],
            self.shape[3],
        )
        return packed_bytes

    @staticmethod
    def packlength() -> int:
        return 4 * 8

    @staticmethod
    def deserialize(s: bytes) -> "ServerMetaMessage":
        code, length, fmt, dtype, shape0, shape1, shape2, shape3 =\
            struct.unpack("iiiiiiii", s)
        return ServerMetaMessage(code, length, MemoryFormat(fmt),
                                 INT_TO_DTYPE[dtype],
                                 torch.Size([shape0, shape1, shape2, shape3]))
