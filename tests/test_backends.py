import pytest
import torch
import random
import string

from lmcache.storage_backend import CreateStorageBackend
from lmcache.storage_backend.local_backend import LMCLocalBackend
from lmcache.storage_backend.remote_backend import LMCRemoteBackend
from lmcache.storage_backend.hybrid_backend import LMCHybridBackend
from lmcache.config import LMCacheEngineConfig, LMCacheEngineMetadata
from lmcache.utils import CacheEngineKey

LMSEVER_URL = "lm://localhost:65432"
REDIS_URL = "redis://localhost:6379"

def random_string(N):
    return ''.join(random.choices(string.ascii_uppercase +
                             string.digits, k=N))

def generate_random_key() -> CacheEngineKey:
    fmt = random.choice(["vllm", "huggingface"])
    model_name = random_string(10).replace("@", "")
    world_size = 3
    worker_id = random.randint(0, 100)
    chunk_hash = random_string(64)
    return CacheEngineKey(fmt, model_name, world_size, worker_id, chunk_hash)

def get_config(t):
    match t:
        case "local":
            return LMCacheEngineConfig.from_defaults(local_device = "cuda", remote_url = None)
        case "remote":
            return LMCacheEngineConfig.from_defaults(local_device = None, remote_url="lm://localhost:65432")
        case "hybrid":
            return LMCacheEngineConfig.from_defaults(local_device = "cuda", remote_url="lm://localhost:65432")
        case _:
            raise ValueError(f"Testbed internal error: Unknown config type: {t}")

def get_metadata():
    return LMCacheEngineMetadata("test-model", 1, -1, "vllm")
            

def test_creation():
    config_local = LMCacheEngineConfig.from_defaults(local_device = "cuda", remote_url = None)
    config_remote = LMCacheEngineConfig.from_defaults(local_device = None, remote_url="lm://localhost:65432")
    config_hybrid = LMCacheEngineConfig.from_defaults(local_device = "cuda", remote_url="lm://localhost:65432")
    metadata = get_metadata()
    
    backend_local = CreateStorageBackend(config_local, get_metadata())
    backend_remote = CreateStorageBackend(config_remote, get_metadata())
    backend_hybrid = CreateStorageBackend(config_hybrid, get_metadata())

    assert isinstance(backend_local, LMCLocalBackend)
    assert isinstance(backend_remote, LMCRemoteBackend)
    assert isinstance(backend_hybrid, LMCHybridBackend)

    config_fail = LMCacheEngineConfig.from_defaults(local_device = None, remote_url = None)
    with pytest.raises(ValueError):
        backend_fail = CreateStorageBackend(config_fail, get_metadata())

@pytest.mark.parametrize("backend_type", ["local", "remote", "hybrid"])
def test_local_backend(backend_type):
    config = get_config(backend_type) #LMCacheEngineConfig.from_defaults(local_device = "cuda", remote_url = None)
    metadata = get_metadata()
    backend = CreateStorageBackend(config, metadata)
    
    N = 10
    keys = [generate_random_key() for i in range(N)]
    random_tensors = [torch.rand((1000, 1000)) for i in range(N)]
    for key, value in zip(keys, random_tensors):
        backend.put(key, value)

    for key, value in zip(keys, random_tensors):
        assert backend.contains(key)
        retrived = backend.get(key)
        assert (value == retrived).all()

def test_restart():
    config = get_config("hybrid") #LMCacheEngineConfig.from_defaults(local_device = "cuda", remote_url = None)
    metadata = get_metadata()
    backend = CreateStorageBackend(config, metadata)
    
    N = 10
    keys = [generate_random_key() for i in range(N)]
    random_tensors = [torch.rand((1000, 1000)) for i in range(N)]
    for key, value in zip(keys, random_tensors):
        backend.put(key, value)


    new_backend = CreateStorageBackend(config, metadata)
    # it should be able to automatically fetch existing keys
    for key, value in zip(keys, random_tensors):
        assert backend.contains(key)
        retrived = backend.get(key)
        assert (value == retrived).all()
