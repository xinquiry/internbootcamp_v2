from internbootcamp.src.base_instruction_generator import BaseInstructionGenerator

from typing import Dict, Any, Optional
import random
import os
from .binairo_standalone import BinairoGenerator

class binairoInstructionGenerator(BaseInstructionGenerator):
    """自定义指令生成器"""
    
    def __init__(self, **kwargs):
        super().__init__()
        # 配置data_source,基类已如下实现，计算reward时会根据此信息匹配对应的RewardCalculator
        self.data_source = f"bootcamp/{self.__class__.__name__.replace('InstructionGenerator', '').lower()}"
        # 初始化自定义参数
        for key, value in kwargs.items():
            setattr(self, key, value)
        
        self.generator = BinairoGenerator(output_folder=kwargs.get("output_folder", "."))
    
    def case_generator(self) -> Dict[str, Any]:
        """
        生成任务案例，返回包含任务信息的字典
        
        Returns:
            Dict[str, Any]: 任务信息字典，包含ground_truth等关键信息；
            这个任务信息字典将作为对应RewardCalculator的_verify_correction方法和对应Tool的create方法的identity参数传入
        """
        # 生成一个难度为1-5随机的题目
        difficulty = random.randint(1, 5)
        # generate returns a list, we take the first one
        # We set save_to_disk=True to ensure image is saved and path is valid
        cases = self.generator.generate(num_cases=1, difficulty=difficulty, save_to_disk=True)
        case = cases[0]
        
        return case

    def prompt_func(self, identity: Dict[str, Any]) -> str:
        """
        根据任务信息生成提示语
        
        Args:
            identity (Dict[str, Any]): 任务信息字典
            
        Returns:
            str: 生成的提示词
        """
        # 实现提示语生成逻辑
        # 使用identity中的信息构建输入给语言模型的prompt
        question_text = identity["question_language"]
        
        # 可以在这里添加更具体的指令，比如要求输出格式等
        text_prompt = f"{question_text}\nPlease solve this Binairo puzzle. Output your answer as a JSON list of lists."
        
        # 返回包含图片路径和文本提示的列表
        return text_prompt

    # def prompt_func(self, identity: Dict[str, Any]) -> list:
    #     """
    #     根据任务信息生成提示语
        
    #     Args:
    #         identity (Dict[str, Any]): 任务信息字典
            
    #     Returns:
    #         list: 生成的提示词列表，包含图片路径和文本提示
    #     """
    #     # 使用identity中的信息构建输入给语言模型的prompt
    #     # 根据题目要求：转化输入给VLM的输入（包含图片和文本）指令
        
    #     question_text = identity["question"]
    #     image_path = identity["image"]
        
    #     # 可以在这里添加更具体的指令，比如要求输出格式等
    #     text_prompt = f"{question_text}\nPlease solve this Binairo puzzle. Output your answer as a JSON list of lists."
        
    #     # 返回包含图片路径和文本提示的列表
    #     return [image_path, text_prompt]