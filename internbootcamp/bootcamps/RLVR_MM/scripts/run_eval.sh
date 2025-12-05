#!/bin/bash
#  评估脚本
# 用法: bash scripts/run_eval.sh

# 评估模型
python -m internbootcamp.utils.run_evaluation \
  --dataset-path data/binairo/binairo_20251203073257_test.jsonl \
  --output-dir outputs/binauro/ \
  --api-key "null" \
  --api-url "http://127.0.0.1:30010/v1" \
  --api-model "/inspire/hdd/project/multimodal-machine-learning-and-generative-model/public/models/Qwen/Qwen3-4B-Thinking-2507" \
  --reward-calculator-class "internbootcamp.bootcamps.RLVR_MM.reward_calculator.binairoRewardCalculator" \
  --max-concurrent 5 \
  --verbose
