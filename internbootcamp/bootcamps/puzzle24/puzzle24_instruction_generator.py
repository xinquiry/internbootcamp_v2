import random
from typing import Dict, Any, Optional
from random import Random

import sympy
from sympy import Symbol, symbols

from internbootcamp.src.base_instruction_generator import BaseInstructionGenerator


QUESTION_TEMPLATE = """Make 24 using {numbers}. You can only use each number once. You can use the operators {operators}.

Final answer format instructions:
1. Provide your final answer as a arithmetic expression (no '=' sign).
2. Do not include the target number in the expression.
3. Use '*' for multiplication.
4. Use '/' for division.
5. End your response with: Answer: YOUR_EXPRESSION
"""


class Puzzle24InstructionGenerator(BaseInstructionGenerator):
    """
    24点题目生成器，根据 reasoning-gym 的 puzzle24.py 改编
    保持原始生成逻辑，适配 InternBootcamp 框架
    """
    
    def __init__(self, 
                 operators: tuple = ("+", "-", "*", "/"),
                 min_value: int = 1,
                 max_value: int = 10,
                 seed: Optional[int] = None):
        """
        初始化 Puzzle24 指令生成器
        
        Args:
            operators (tuple): 允许的运算符
            min_value (int): 数字最小值
            max_value (int): 数字最大值
            seed (Optional[int]): 随机种子
        """
        super().__init__()
        self.operators = operators
        self.min_value = min_value
        self.max_value = max_value
        self.seed = seed
        
        # 验证参数
        assert len(self.operators) > 0, "At least one operator is required"
        assert self.min_value <= self.max_value, "Minimum value must be less than or equal to maximum value"
        assert self.min_value >= 1, "Minimum value must be at least 1"
        assert self.max_value <= 10, "Maximum value must be at most 10"
    
    def _generate_candidate_expression(self, rng: Random, num_terms: int = 4) -> tuple:
        """
        生成候选表达式（保留原 puzzle24.py 的核心算法）
        
        Args:
            rng: 随机数生成器
            num_terms: 数字个数，默认4
            
        Returns:
            Tuple of (sympy expression, list of numbers, list of symbols)
        """
        # 生成随机数字
        numbers = [rng.randint(self.min_value, self.max_value) for _ in range(num_terms)]
        
        # 创建符号变量
        syms = symbols(f"x:{num_terms}")
        
        # 构建随机表达式
        expr = syms[0]
        
        for i in range(1, num_terms):
            op = rng.choice(self.operators)
            if op == "+":
                expr = expr + syms[i]
            elif op == "-":
                expr = expr - syms[i]
            elif op == "*":
                expr = expr * syms[i]
            else:  # op == "/"
                # 除法特殊处理，避免小数
                if numbers[i] != 0:
                    current = int(expr.subs({sym: num for sym, num in zip(syms[:i], numbers[:i])}))
                    remaining = [n for n in numbers[i:] if n != 0]
                    rng.shuffle(remaining)
                    found_divisor = False
                    for div in remaining:
                        if current % div == 0:
                            numbers[i] = div
                            expr = expr / syms[i]
                            found_divisor = True
                            break
                    if not found_divisor:
                        expr = expr - syms[i]
                else:
                    expr = expr + syms[i]
        
        return expr, numbers, syms
    
    def case_generator(self) -> Dict[str, Any]:
        """
        生成一个24点题目案例
        
        Returns:
            Dict[str, Any]: 包含题目信息的字典
        """
        # 使用随机种子
        if self.seed is not None:
            rng = Random(self.seed)
        else:
            rng = Random()
        
        # 循环生成，直到找到结果=24的表达式
        while True:
            expr, numbers, syms = self._generate_candidate_expression(rng, 4)
            
            # 检查结果是否等于24
            result = expr.subs({sym: num for sym, num in zip(syms, numbers)})
            if result == 24:
                break
        
        # 将符号表达式转换为字符串
        expr_str = str(expr)
        for i, sym in enumerate(syms):
            expr_str = expr_str.replace(str(sym), str(numbers[i]))
        
        return {
            "numbers": numbers,
            "answer": expr_str,
            "operators": list(self.operators),
            "difficulty": {"value": (self.min_value, self.max_value)}
        }
    
    def prompt_func(self, identity: Dict[str, Any]) -> str:
        """
        根据题目信息生成提示语
        
        Args:
            identity (Dict[str, Any]): 题目信息
            
        Returns:
            str: 生成的提示语
        """
        numbers = identity['numbers']
        operators = identity.get('operators', ["+", "-", "*", "/"])
        
        prompt = QUESTION_TEMPLATE.format(
            numbers=", ".join(map(str, numbers)),
            operators=", ".join(operators)
        )
        
        return prompt
