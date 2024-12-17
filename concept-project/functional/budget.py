from typing import Dict, List

def set_budget(budgets: Dict[str, float], category: str, amount: float) -> Dict[str, float]:
    """Set a budget for a specific category."""
    new_budgets = budgets.copy()
    new_budgets[category] = amount
    return new_budgets

def track_budget_usage(budgets: Dict[str, float], transactions: List[Dict]) -> Dict[str, float]:
    """Track the spending for each category against the budget."""
    def calculate_usage(categories, usage):
        if not categories:
            return usage
        category = categories[0]
        usage[category] = sum(transaction['amount'] for transaction in transactions if transaction['category'] == category and transaction['type'] == 'expense')
        return calculate_usage(categories[1:], usage)

    return calculate_usage(list(budgets.keys()), {})
    
def budget_alert(budgets: Dict[str, float], usage: Dict[str, float]) -> List[str]:
    """Generate alerts when the budget for a category is exceeded or close to it."""
    def generate_alerts(categories, alerts):
        if not categories:
            return alerts
        category = categories[0]
        used = usage[category]
        if used > budgets.get(category, 0):
            alerts.append(f"Budget exceeded for {category}. Used: ${used}, Budget: ${budgets[category]}")
        elif used > 0.9 * budgets.get(category, 0):
            alerts.append(f"Warning: You are close to exceeding the budget for {category}. Used: ${used}, Budget: ${budgets[category]}")
        return generate_alerts(categories[1:], alerts)

    return generate_alerts(list(budgets.keys()), [])
