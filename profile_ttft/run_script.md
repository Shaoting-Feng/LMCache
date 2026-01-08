For prefill:
```
vllm serve <model> --no-enable-prefix-caching
vllm serve "lmsys/longchat-7b-v1.5-32k" --no-enable-prefix-caching  --max-model-len 119344
```

For CPU:
```
vllm serve <model> --no-enable-prefix-caching --kv-transfer-config '{"kv_connector":"LMCacheConnectorV1", "kv_role":"kv_both"}'
```

For disk:
```
LMCACHE_CONFIG_FILE="disk.yaml" vllm serve <model> --no-enable-prefix-caching --kv-transfer-config '{"kv_connector":"LMCacheConnectorV1", "kv_role":"kv_both"}'
```

For remote disk:
```
LMCACHE_CONFIG_FILE="mock.yaml" vllm serve <model> --no-enable-prefix-caching --kv-transfer-config '{"kv_connector":"LMCacheConnectorV1", "kv_role":"kv_both"}'
```

Need to disable the non-prefix caching and specific location storage in LMCache.
