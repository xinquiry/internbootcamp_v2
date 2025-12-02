#!/bin/bash
# Puzzle24 评估脚本
# 用法: bash scripts/run_eval.sh

# 评估模型
python -m internbootcamp.utils.run_evaluation \
  --dataset-path data/puzzle24/puzzle24_20251127040049_test.jsonl \
  --output-dir outputs/puzzle24/ \
  --api-key "$API_KEY" \
  --api-url "$API_URL" \
  --api-model "$API_MODEL" \
  --reward-calculator-class "internbootcamp.bootcamps.puzzle24.puzzle24_reward_calculator.Puzzle24RewardCalculator" \
  --max-concurrent 5 \
  --verbose
