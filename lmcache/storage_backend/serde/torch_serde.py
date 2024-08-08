import torch
import io
import time

from lmcache.storage_backend.serde.serde import Serializer, Deserializer
from lmcache.logging import init_logger
from lmcache.config import GlobalConfig

logger = init_logger(__name__)

class TorchSerializer(Serializer):
    def __init__(self):
        super().__init__()

    def to_bytes(self, t: torch.Tensor) -> bytes:
        with io.BytesIO() as f:
            torch.save(t.clone().detach(), f)
            return f.getvalue()

class TorchDeserializer(Deserializer):
    def __init__(self):
        super().__init__()
        self.debug = GlobalConfig.is_debug()

    def from_bytes_debug(self, b: bytes) -> torch.Tensor:
        start = time.perf_counter()
        with io.BytesIO(b) as f:
            t = torch.load(f)
            end = time.perf_counter()
            logger.debug("Deserialization took: %.2f", (end - start) * 1000)
            return t

    def from_bytes_normal(self, b: bytes) -> torch.Tensor:
        with io.BytesIO(b) as f:
            return torch.load(f)

    def from_bytes(self, b: bytes) -> torch.Tensor:
        if self.debug:
            return self.from_bytes_debug(b)
        else:
            return self.from_bytes_normal(b)
