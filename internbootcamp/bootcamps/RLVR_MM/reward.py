try:
    from internbootcamp.src.base_reward_calculator import BaseRewardCalculator
except ImportError:
    from mock_internbootcamp import BaseRewardCalculator

import json
import re

class binairoRewardCalculator(BaseRewardCalculator):
    """自定义奖励计算器"""
    
    @staticmethod
    def extract_output(output_str: str):
        """
        从模型输出中提取关键信息用于奖励计算
        
        Args:
            output_str: 模型的最终响应字符串
        
        Returns:
            提取的信息，作为_verify_correction()的extract_solution参数
        """
        # 尝试提取JSON格式的答案
        try:
            # 寻找可能是JSON的字符串片段
            # 假设答案是一个列表的列表
            match = re.search(r'\[\s*\[.*\]\s*\]', output_str, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
            else:
                return None
        except Exception:
            return None
    
    @classmethod
    def _verify_correction(cls, extract_solution, identity: dict, **kwargs) -> float:
        """
        验证提取的解决方案并计算正确性分数
        
        Args:
            extract_solution: 从extract_output()提取的信息
            identity: 任务标准答案信息（来自InstructionGenerator.case_generator()）
            kwargs: 额外关键字参数，可在评测和训练时传递，可用于控制reward计算逻辑
        
        Returns:
            float: 正确性分数（0-1之间）
        """
        if extract_solution is None:
            return 0.0
            
        ground_truth_str = identity.get("answer")
        
        # Convert extracted solution (list of lists) to the same string format as ground_truth
        # format: rows separated by newline, cells by space
        try:
            if isinstance(extract_solution, list):
                formatted_extract = '\n'.join([' '.join(str(cell) for cell in row) for row in extract_solution])
                # Normalize both strings (strip whitespace)
                return 1.0 if formatted_extract.strip() == ground_truth_str.strip() else 0.0
            else:
                return 0.0
        except Exception:
            return 0.0