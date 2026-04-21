export VLLM_LOGGING_LEVEL=INFO
CUDA_VISIBLE_DEVICES=0,1,2,3,4,5,6,7 SAFETENSORS_FAST_GPU=1 vllm serve \
    MiniMaxAI/MiniMax-M2.5 --trust-remote-code \
    --enable_expert_parallel --tensor-parallel-size 8 \
    --enable-auto-tool-choice --tool-call-parser minimax_m2 \
    --port 9090 \
    --api-key "xxxxxxxxxxxx" \
    --reasoning-parser minimax_m2_append_think 