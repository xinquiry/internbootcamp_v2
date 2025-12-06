#!/usr/bin/env bash

# Qwen2.5-VL-72B-Instruct-AWQ    Qwen3-235B-A22B-Thinking-2507     Qwen3-VL-235B-A22B-Instruct  Qwen3-VL-4B-Instruct
#                                           Qwen3-VL-2B-Instruct               

# Finished
# Qwen3-0.6B Qwen3-4B
# Qwen3-14B Qwen3-32B Qwen3-8B
# Qwen3-VL-8B-Instruct
# Qwen3-VL-30B-A3B-Instruct
# Qwen3-VL-32B-Instruct
# Qwen3-4B-Thinking-2507
# Qwen3-30B-A3B-Thinking-2507

set -e

MODEL="Qwen3-1.7B"

PORT="30010"

# bfloat16  → 原始 bf16 模型（显存最多，精度最高）
# float16   → fp16 模型
# auto      → AWQ/GPTQ 量化模型用这个
DTYPE="auto"

BASE_DIR="/inspire/hdd/project/multimodal-machine-learning-and-generative-model/public/models/Qwen"
MODEL_PATH="$BASE_DIR/$MODEL"

EXTRA_ARGS=""
if [[ $MODEL == *"VL"* ]]; then
    # 所有 VL 模型自动加上多模态参数
    # EXTRA_ARGS="--limit-mm-per-prompt· image=10,video=10 --max-model-len 32768"
    EXTRA_ARGS="--max-model-len 27440 --tensor-parallel-size 2"
elif [[ $MODEL == *"235B"* ]] || [[ $MODEL == *"72B"* ]]; then
    DTYPE="auto"
    EXTRA_ARGS="--quantization awq --tensor-parallel-size 8 --max-model-len 16384"
elif [[ $MODEL == *"32B"* ]]; then
    EXTRA_ARGS="--tensor-parallel-size 2 --max-model-len 32768"
elif [[ $MODEL == *"14B"* ]]; then
    EXTRA_ARGS="--tensor-parallel-size 2 --max-model-len 32768"
else
    EXTRA_ARGS="--tensor-parallel-size 2 --max-model-len 32768"
fi

echo "=================================================="
echo "即将启动模型：$MODEL"
echo "路径：$MODEL_PATH"
echo "端口：$PORT"
echo "dtype：$DTYPE"
echo "额外参数：$EXTRA_ARGS"
echo "=================================================="

vllm serve "$MODEL_PATH" \
    --host 0.0.0.0 \
    --port "$PORT" \
    --dtype "$DTYPE" \
    $EXTRA_ARGS
