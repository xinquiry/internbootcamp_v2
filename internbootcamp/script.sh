uv run vllm serve \
  /inspire/hdd/project/multimodal-machine-learning-and-generative-model/public/models/Qwen/Qwen3-0.6B \
  --port 30001 \
  --host 0.0.0.0 \
  --dtype bfloat16


uv run python -m internbootcamp.utils.run_evaluation \
  --dataset-path data/puzzle24/puzzle24_20251202075822_test.jsonl \
  --output-dir outputs/puzzle24/ \
  --api-key "null" \
  --api-url "http://127.0.0.1:30001/v1" \
  --api-model "/inspire/hdd/project/multimodal-machine-learning-and-generative-model/public/models/Qwen/Qwen3-0.6B" \
  --reward-calculator-class "internbootcamp.bootcamps.puzzle24.puzzle24_reward_calculator.Puzzle24RewardCalculator" \
  --max-concurrent 5 \
  --verbose

  # --api-model "Qwen3-0.6B" \
  # --api-url "http://10.102.249.85:30001/v1" \