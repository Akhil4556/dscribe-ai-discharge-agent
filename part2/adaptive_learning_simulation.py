import numpy as np
import matplotlib.pyplot as plt
import random
from typing import List, Dict, Any, Tuple

# =====================================================================
# 1. THE SIMULATED REVIEWER (DOCTOR EMULATION POLICY)
# =====================================================================
class SimulatedDoctor:
    """
    Acts as the ground-truth evaluator. Applies a hidden clinical and stylistic 
    policy to agent drafts, returning a corrected version and calculating reward.
    """
    def __init__(self):
        # The doctor's hidden rule profile
        self.preferred_style = "bulleted"
        self.mandatory_flags = ["MISSING INSULIN", "THYROID OMISSION"]

    def edit_draft(self, draft: str, prompt_strategy: str) -> Tuple[str, float]:
        """Reviews the draft, applies corrections, and computes the reward signal."""
        # Baseline simulation of Levenshtein edit distance logic based on mismatching criteria
        base_error_rate = 0.45
        
        # Stylistic corrections
        if prompt_strategy == "Concise_Bulleted":
            base_error_rate -= 0.15  # Doctor has to edit less if it's already bulleted
        elif prompt_strategy == "Narrative_Heavy":
            base_error_rate += 0.20  # Heavy editing required to break up text walls
            
        # Clinical safety corrections (Hard clinical guardrail)
        if "⚠️" in draft or "CRITICAL OMISSION" in draft:
            base_error_rate -= 0.20  # Good draft caught the safety flags, less editing needed
        else:
            base_error_rate += 0.35  # Severe penalty: doctor must manually inject omissions

        # Clamp error rate between a reasonable clinical boundary [0.05, 0.95]
        error_rate = max(0.05, min(0.95, base_error_rate))
        
        # Introduce a minor stochastic noise variable to represent variation between individual doctors
        noise = random.uniform(-0.02, 0.02)
        final_error = max(0.02, min(0.98, error_rate + noise))
        
        # Reward is inversely proportional to the amount of editing required
        reward = 1.0 - final_error
        
        # Generate a simulated correction text mapping
        corrected_version = f"[Finalized Approved Chart Summary]\n{draft[:int(len(draft)*(1-final_error))]}...\n[Doctor Note: Verified Clean & Safe]"
        
        return corrected_version, reward

# =====================================================================
# 2. LEARNING AGENT (CONTEXTUAL BANDIT MECHANISM)
# =====================================================================
class AdaptiveDischargeAgent:
    """
    An agent that learns from accumulated doctor edits over time by optimizing 
    its structural generation strategy based on historically observed rewards.
    """
    def __init__(self):
        # Multi-armed prompt strategies the agent can select from
        self.strategies = ["Narrative_Heavy", "Standard_Template", "Concise_Bulleted"]
        # Initialize historical action-value estimates (Q-values) for each strategy
        self.q_values = {strategy: 0.5 for strategy in self.strategies}
        self.strategy_counts = {strategy: 0 for strategy in self.strategies}
        self.epsilon = 0.3  # Exploration rate

    def choose_strategy(self) -> str:
        """Epsilon-greedy strategy selection loop."""
        if random.random() < self.epsilon:
            return random.choice(self.strategies)  # Explore alternate templates
        else:
            return max(self.q_values, key=self.q_values.get)  # Exploit the best performer

    def update_learning_memory(self, strategy: str, reward: float):
        """Incremental update rule for action-value tracking."""
        self.strategy_counts[strategy] += 1
        n = self.strategy_counts[strategy]
        # Running average formula
        self.q_values[strategy] += (reward - self.q_values[strategy]) / n

    def generate_draft_mockup(self, strategy: str) -> str:
        """Simulates document compilation using the active strategy configuration."""
        if strategy == "Narrative_Heavy":
            return "The patient was admitted with symptoms of loose stools and fever. Fluid updates were configured. Creatinine normalized on Day 3."
        elif strategy == "Standard_Template":
            return "DIAGNOSIS: Gastroenteritis.\nHISTORY: Fever x 3 days.\nADVICE: Tab Raciper, Tab Emeset."
        elif strategy == "Concise_Bulleted":
            return "* **Diagnoses:** Gastroenteritis, Acute DKA, Pyelonephritis\n* **Safety Flag:** ⚠️ CRITICAL OMISSION: No home insulin prescribed on discharge."

# =====================================================================
# 3. CLOSED-LOOP SIMULATION & EVALUATION PIPELINE
# =====================================================================
def run_feedback_loop_simulation(total_iterations: int = 150):
    agent = AdaptiveDischargeAgent()
    doctor = SimulatedDoctor()
    
    reward_history = []
    edit_burden_history = []
    strategy_tracking = []
    
    print("Beginning Agent Optimization Cycle...")
    print(f"Initial Baseline Expected Rewards: {agent.q_values}")
    
    for i in range(total_iterations):
        # 1. Agent plans and selects a formatting strategy
        chosen_strategy = agent.choose_strategy()
        draft = agent.generate_draft_mockup(chosen_strategy)
        
        # 2. Simulated Doctor edits the draft and provides feedback
        _, reward = doctor.edit_draft(draft, chosen_strategy)
        
        # 3. Agent updates its parameters based on the feedback
        agent.update_learning_memory(chosen_strategy, reward)
        
        # Decay exploration rate (epsilon) over time to consolidate learning gains
        if i > 50:
            agent.epsilon = max(0.05, 0.3 * (1.0 - i / total_iterations))
            
        reward_history.append(reward)
        edit_burden_history.append(1.0 - reward)  # Edit burden is the inverse of the match reward
        strategy_tracking.append(chosen_strategy)

    print("\nOptimization Complete.")
    print(f"Final Optimized Strategy Q-Values: {agent.q_values}")
    
    # Calculate before/after performance averages
    initial_avg_edit = np.mean(edit_burden_history[:15]) * 100
    final_avg_edit = np.mean(edit_burden_history[-15:]) * 100
    print(f"-> Initial Doctor Edit Burden: {initial_avg_edit:.2f}%")
    print(f"-> Post-Learning Doctor Edit Burden: {final_avg_edit:.2f}%")
    print(f"-> Net Reduction in Manual Clinical Re-writing: {initial_avg_edit - final_avg_edit:.2f}%")
    
    # Generate Performance Plotting Curves
    generate_metrics_chart(reward_history, edit_burden_history)

def generate_metrics_chart(rewards: List[float], edits: List[float]):
    """Generates and displays the system's learning and improvement curves."""
    # Compute running rolling averages to smoothly illustrate trends
    window = 10
    rolling_rewards = np.convolve(rewards, np.ones(window)/window, mode='valid')
    rolling_edits = np.convolve(edits, np.ones(window)/window, mode='valid')
    
    plt.figure(figsize=(12, 5))
    
    # Plot 1: Reward Curve (Match Accuracy)
    plt.subplot(1, 2, 1)
    plt.plot(rewards, alpha=0.2, color='g', label='Raw Iteration Reward')
    plt.plot(rolling_rewards, color='g', linewidth=2, label='Rolling Match Rate (Accuracy)')
    plt.title('Agent Match Rate Over Time')
    plt.xlabel('Patient Case Iterations')
    plt.ylabel('Normalized Match Score (0.0 - 1.0)')
    plt.grid(True, linestyle='--')
    plt.legend()
    
    # Plot 2: Doctor Edit Distance Burden (Inverse Reward Decline Curve)
    plt.subplot(1, 2, 2)
    plt.plot(edits, alpha=0.2, color='r', label='Raw Edit Distance')
    plt.plot(rolling_edits, color='r', linewidth=2, label='Rolling Edit Burden')
    plt.title('Doctor Edit Burden Optimization Curve')
    plt.xlabel('Patient Case Iterations')
    plt.ylabel('Normalized Edit Distance')
    plt.grid(True, linestyle='--')
    plt.legend()
    
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    run_feedback_loop_simulation()
