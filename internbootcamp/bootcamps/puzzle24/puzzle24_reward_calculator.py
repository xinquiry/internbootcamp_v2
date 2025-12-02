import re

from sympy.parsing.sympy_parser import parse_expr

from internbootcamp.src.base_reward_calculator import BaseRewardCalculator


class Puzzle24RewardCalculator(BaseRewardCalculator):
    """
    24点任务奖励计算器，使用 reasoning-gym puzzle24.py 的 score_answer 逻辑
    适配 InternBootcamp 框架
    """
    
    @staticmethod
    def extract_output(output_str: str) -> str:
        """
        从模型输出中提取表达式
        
        查找 "Answer:" 关键词并提取表达式（参考 NP_MM 方式）
        
        注意：为了符合原 puzzle24.py 的评分逻辑（失败时返回 0.01 而非 0.0），
        此方法始终返回字符串（可能为空），而不是 None
        
        Args:
            output_str (str): 模型的原始输出
            
        Returns:
            str: 提取的表达式字符串，如果提取失败返回空字符串
        """
        if not output_str or "Answer:" not in output_str:
            return ""  # 返回空字符串而非 None，确保 _verify_correction 被调用
        
        # 提取 "Answer:" 后的内容
        expr_str = output_str.split("Answer:")[-1].strip()
        
        # 取第一行（避免多余内容）
        expr_str = expr_str.split('\n')[0].strip()
        
        return expr_str if expr_str else ""
    
    @classmethod
    def _verify_correction(cls, answer: str, identity: dict, **kwargs) -> float:
        """
        验证表达式正确性并计算得分，使用原 puzzle24.py 的 score_answer 逻辑
        
        Args:
            answer: 提取的表达式（由 extract_output 返回，可能为空字符串）
            identity (dict): 任务信息，包含 difficulty
            **kwargs: 额外参数
            
        Returns:
            float: 得分，1.0 表示完全正确，0.01 表示错误
        """
        # 获取配置参数（从 difficulty 中读取，对应原代码的 self.config）
        min_value, max_value = identity.get('difficulty', {}).get('value', (1, 10))
        
        # 以下是原 puzzle24.py 的 score_answer 逻辑
        reward = 0.01
        if answer:  # 检查是否为非空字符串
            try:
                answer = answer.strip()
                user_answer = int(parse_expr(answer))
                solved = user_answer == 24
                used_numbers = [int(num) for num in re.findall(r"\b\d+\b", answer)]
                if len(used_numbers) != 4:
                    reward = 0.01
                elif any(num > max_value or num < min_value for num in used_numbers):
                    reward = 0.01
                elif not solved:
                    reward = 0.01
                else:
                    reward = 1.0
            except Exception:
                reward = 0.01
        return reward
