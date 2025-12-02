uv run python -m internbootcamp.utils.run_evaluation \
  --dataset-path data/your_bootcamp/test.jsonl \
  --output-dir outputs/ \
  --api-key "$API_KEY" \
  --api-url "$API_URL" \
  --api-model "gpt-3.5-turbo" \
  --reward-calculator-class "internbootcamp.bootcamps.example_bootcamp.example_reward_calculator.ExampleRewardCalculator" \
  --tool-config configs/your_tool_config.yaml \
  --interaction-config internbootcamp/bootcamps/example_bootcamp/configs/example_interaction_config.yaml \
  --max-tool-turns-per-interaction 5 \
  --max-interaction-turns 3
  