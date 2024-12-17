# budget.py
from typing import Dict, List

def set_budget(budgets: Dict[str, float], category: str, amount: float) -> Dict[str, float]:
    """Set a budget for a specific category."""
    new_budgets = budgets.copy()
    new_budgets[category] = amount
    return new_budgets

def track_budget_usage(budgets: Dict[str, float], transactions: List[Dict]) -> Dict[str, float]:
    """Track the spending for each category against the budget."""
    usage = {category: sum(transaction['amount'] for transaction in transactions if transaction['category'] == category)
             for category in budgets}
    return usage

def budget_alert(budgets: Dict[str, float], usage: Dict[str, float]) -> List[str]:
    """Generate alerts when the budget for a category is exceeded or close to it."""
    alerts = []
    for category, used in usage.items():
        if used > budgets.get(category, 0):
            alerts.append(f"Budget exceeded for {category}. Used: ${used}, Budget: ${budgets[category]}")
        elif used > 0.9 * budgets.get(category, 0):
            alerts.append(f"Warning: You are close to exceeding the budget for {category}. Used: ${used}, Budget: ${budgets[category]}")
    return alerts

