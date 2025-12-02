import os
import json
from internbootcamp.bootcamps.RLVR_MM.instruction_generator import binairoInstructionGenerator
from internbootcamp.bootcamps.RLVR_MM.reward_calculator import binairoRewardCalculator

def main():
    # 1. Initialize Generator
    print("Initializing Generator...")
    # Create output directory if it doesn't exist
    os.makedirs("data/binairo", exist_ok=True)
    generator = binairoInstructionGenerator(output_folder="data/binairo")
    
    # 2. Generate Case
    print("Generating Case...")
    case = generator.case_generator()
    print(f"Generated Case Index: {case['index']}")
    print(f"Question: {case['question']}")
    print(f"Image Path: {case['image']}")
    print(f"Ground Truth Answer:\n{case['answer']}")
    
    # 3. Generate Prompt
    print("\nGenerating Prompt...")
    prompt = generator.prompt_func(case)
    print(f"Prompt (Multimodal): {prompt}")
    
    # Extract text prompt for simulation (assuming the second element is text)
    if isinstance(prompt, list) and len(prompt) > 1:
        text_prompt = prompt[1]
    else:
        text_prompt = str(prompt)
    
    # 4. Simulate Model Output (Correct)
    print("\nSimulating Correct Model Output...")
    # Parse the answer string back to list of lists to simulate model output
    answer_str = case['answer']
    correct_solution = [[int(x) for x in row.split()] for row in answer_str.strip().split('\n')]
    correct_output = json.dumps(correct_solution)
    print(f"Simulated Output: {correct_output}")
    
    # 5. Calculate Reward (Correct)
    print("Calculating Reward (Correct)...")
    extracted_solution = binairoRewardCalculator.extract_output(correct_output)
    reward = binairoRewardCalculator._verify_correction(extracted_solution, case)
    print(f"Reward: {reward}")
    
    # 6. Simulate Model Output (Incorrect)
    print("\nSimulating Incorrect Model Output...")
    incorrect_solution = [row[:] for row in correct_solution]
    if incorrect_solution:
        incorrect_solution[0][0] = 1 - incorrect_solution[0][0] # Flip one bit
    incorrect_output = json.dumps(incorrect_solution)
    print(f"Simulated Output: {incorrect_output}")
    
    # 7. Calculate Reward (Incorrect)
    print("Calculating Reward (Incorrect)...")
    extracted_solution_incorrect = binairoRewardCalculator.extract_output(incorrect_output)
    reward_incorrect = binairoRewardCalculator._verify_correction(extracted_solution_incorrect, case)
    print(f"Reward: {reward_incorrect}")

if __name__ == "__main__":
    main()
