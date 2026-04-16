CUDA_VISIBLE_DEVICES=1 vllm serve \
    google/gemma-4-E4B-it --trust-remote-code \
    # --enable_expert_parallel \
    # --tensor-parallel-size 1 \
    --port 9090
