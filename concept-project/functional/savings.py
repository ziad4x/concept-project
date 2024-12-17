from typing import List, Dict

def set_savings_goal(goals: List[Dict], target: float, months: int) -> List[Dict]:
    """Define a savings goal and calculate monthly savings."""
    if months <= 0:
        raise ValueError("Months must be greater than 0.")
    
    monthly_savings = target / months
    goal = {
        'target': target,
        'monthly_savings': monthly_savings,
        'months_remaining': months
    }
    
    return goals + [goal]

def display_savings_goal_details(goal: Dict) -> str:
    """Display the detailed savings goal information."""
    return (f"Savings Goal Details:\n"
            f" - Target Amount: ${goal['target']:.2f}\n"
            f" - Monthly Savings Needed: ${goal['monthly_savings']:.2f}\n"
            f" - Months Remaining: {goal['months_remaining']}")
