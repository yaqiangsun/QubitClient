curl https://llm.deepvectories.top/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H 'Authorization: Bearer vllm_xxxxxxxx' \
  -d '{
    "model": "moonshotai/Kimi-K2.6",
    "messages": [
      {"role": "user", "content": "你是谁"}
    ],
    "max_tokens": 100,
    "temperature": 0.7
  }'