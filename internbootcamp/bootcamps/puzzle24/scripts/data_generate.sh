#!/bin/bash
# 数据生成脚本 - Puzzle24
# 用法: bash scripts/data_generate.sh

# 获取脚本所在目录的绝对路径
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"

# 进入项目根目录
cd "$PROJECT_ROOT"

# 数据生成
python -m internbootcamp.utils.data_generation \
    --instruction-config internbootcamp/bootcamps/puzzle24/configs/puzzle24_instruction_config.yaml \
    --output-dir data/puzzle24/ \
    --split-samples train:0,test:10 \
    --shuffle

echo "数据生成完成！输出目录: data/puzzle24/"
