from typing import Optional, Tuple

from lmcache.experimental.config import LMCacheEngineConfig
from lmcache.experimental.memory_management import MemoryAllocatorInterface
from lmcache.experimental.storage_backend.naive_serde.kivi_serde import (
    KIVIDeserializer, KIVISerializer)
from lmcache.experimental.storage_backend.naive_serde.naive_serde import (
    NaiveDeserializer, NaiveSerializer)
from lmcache.experimental.storage_backend.naive_serde.serde import (
    Deserializer, Serializer)


def CreateSerde(
    serde_type: str,
    memory_allocator: MemoryAllocatorInterface,
    config: LMCacheEngineConfig,
) -> Tuple[Serializer, Deserializer]:
    s: Optional[Serializer] = None
    d: Optional[Deserializer] = None

    if serde_type == "naive":
        s, d = NaiveSerializer(), NaiveDeserializer()
    elif serde_type == "kivi":
        s, d = KIVISerializer(memory_allocator), \
            KIVIDeserializer(memory_allocator)
    else:
        raise ValueError(f"Invalid serde type: {serde_type}")

    return s, d


__all__ = [
    "Serializer",
    "Deserializer",
    "KIVISerializer",
    "KIVIDeserializer",
    "CreateSerde",
]
