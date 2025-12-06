#!/bin/bash
# Puzzle24 评估脚本
# 用法: bash scripts/run_eval.sh

# 评估模型
python -m internbootcamp.utils.run_evaluation \
  --dataset-path data/puzzle24/puzzle24_20251203072550_test.jsonl \
  --output-dir outputs/puzzle24/ \
  --api-key "null" \
  --api-url "http://127.0.0.1:30010/v1" \
  --api-model "/inspire/hdd/project/multimodal-machine-learning-and-generative-model/public/models/Qwen/Qwen3-VL-2B-Instruct" \
  --reward-calculator-class "internbootcamp.bootcamps.puzzle24.puzzle24_reward_calculator.Puzzle24RewardCalculator" \
  --max-concurrent 5 \
  --verbose
