# analytics.py
from typing import List, Dict

def spending_summary(transactions: List[Dict]) -> Dict[str, float]:
    """Generate a spending summary by category."""
    summary = {}
    for transaction in transactions:
        category = transaction['category']
        summary[category] = summary.get(category, 0) + transaction['amount']
    return summary

def overall_spending(transactions: List[Dict]) -> float:
    """Calculate total spending."""
    return sum(transaction['amount'] for transaction in transactions)

def spending_trends(transactions: List[Dict], previous_month: List[Dict]) -> Dict[str, float]:
    """Compare spending trends between the current and previous month."""
    current_summary = spending_summary(transactions)
    previous_summary = spending_summary(previous_month)
    trends = {category: current_summary.get(category, 0) - previous_summary.get(category, 0)
              for category in current_summary}
    return trends

def spending_insights(trends: Dict[str, float], current_summary: Dict[str, float]) -> List[str]:
    """Provide insights into spending trends."""
    insights = []
    for category, change in trends.items():
        current_amount = current_summary.get(category, 0)
        
        if current_amount == 0 and change == 0:
            insights.append(f"No change in spending for {category}.")
            continue
        if current_amount == 0:
            insights.append(f"New spending on {category}: ${change:.2f}.")
            continue
        
        if current_amount - change != 0:
            if change > 0:
                percentage_increase = (change / (current_amount - change)) * 100
                insights.append(f"You spent {percentage_increase:.2f}% more on {category} this month.")
            elif change < 0:
                percentage_decrease = (abs(change) / (current_amount + change)) * 100
                insights.append(f"You spent {percentage_decrease:.2f}% less on {category} this month.")
        else:
            insights.append(f"Spending on {category} is unchanged, cannot calculate percentage.")
    
    return insights
