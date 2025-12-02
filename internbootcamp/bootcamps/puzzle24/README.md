# Puzzle24 - 24点游戏推理任务

## 任务说明

24点游戏：给定4个数字（1-10），使用 `+`、`-`、`*`、`/` 运算，每个数字使用一次，使结果等于24。

## 安装部署

将 `puzzle24` 文件夹放置在 `internbootcamp_v2/internbootcamp/bootcamps/` 目录下。

## 依赖安装

```bash
pip install verl starlette openai transformers tenacity jsonlines
```

## 快速开始

**注意**：所有命令需在项目根目录 `/path/to/internbootcamp_v2` 下运行。

### 1. 生成数据

```bash
bash internbootcamp/bootcamps/puzzle24/scripts/data_generate.sh
```

生成的数据在 `data/puzzle24/` 目录。

### 2. 运行评测

修改 `internbootcamp/bootcamps/puzzle24/scripts/run_eval.sh` 中的 API 配置，然后：

```bash
bash internbootcamp/bootcamps/puzzle24/scripts/run_eval.sh
```

评测结果保存在 `outputs/puzzle24/[model_name]/` 目录。

## 任务格式

**输入提示**：
```
Make 24 using 3, 8, 3, 8. You can only use each number once. 
You can use the operators +, -, *, /.

Final answer format instructions:
1. Provide your final answer as a arithmetic expression (no '=' sign).
2. Do not include the target number in the expression.
3. Use '*' for multiplication.
4. Use '/' for division.
5. End your response with: Answer: YOUR_EXPRESSION
```

**期望输出**：
```
Answer: 8/(3-8/3)
```

## 评分规则

二值评分（沿用 reasoning-gym 原始逻辑）：
- **1.0**：正确（使用4个数字，结果=24，数字在范围内）
- **0.01**：错误

## 难度配置

编辑 `internbootcamp/bootcamps/puzzle24/configs/puzzle24_instruction_config.yaml`：

```yaml
instruction_generators:
  easy:
    config:
      min_value: 1
      max_value: 10     # 数字范围 1-10（reasoning-gym 定义为 easy）
    generation_ratio: 5
  
  hard:
    config:
      min_value: 1
      max_value: 6      # 数字范围 1-6（reasoning-gym 定义为 hard）
    generation_ratio: 5
```

**难度说明**：
- **easy (1-10)**：数字范围更大，但题目实际更容易（遵循 reasoning-gym 定义）
- **hard (1-6)**：数字范围更小，但题目实际更难（较少的数字组合，有解的情况更少）
- `generation_ratio` 控制该难度占总数据的比例（会自动归一化）


## 参考

- [reasoning-gym/puzzle24](https://github.com/reasoning-gym/reasoning-gym) - 原始实现
- InternBootcamp 框架文档
