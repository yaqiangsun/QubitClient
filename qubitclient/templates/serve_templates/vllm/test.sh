curl http://localhost:9091/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nv-community/Ising-Calibration-1-35B-A3B",
    "prompt": "Hello, what is your name?",
    "max_tokens": 50
  }'