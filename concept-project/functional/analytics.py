from typing import List, Dict

def spending_summary(transactions: List[Dict]) -> Dict[str, float]:
    """Generate a spending summary by category."""
    def summarize(transactions, summary):
        if not transactions:
            return summary
        transaction = transactions[0]
        if transaction['type'] == 'expense':
            category = transaction['category']
            summary[category] = summary.get(category, 0) + transaction['amount']
        return summarize(transactions[1:], summary)
    
    return summarize(transactions, {})

def overall_spending(transactions: List[Dict]) -> float:
    """Calculate total spending (only expenses)."""
    def sum_spending(transactions):
        if not transactions:
            return 0
        if transactions[0]['type'] == 'expense':
            return transactions[0]['amount'] + sum_spending(transactions[1:])
        else:
            return sum_spending(transactions[1:])
    
    return sum_spending(transactions)

def spending_trends(transactions: List[Dict], previous_month: List[Dict]) -> Dict[str, float]:
    """Compare spending trends between the current and previous month."""
    current_summary = spending_summary(transactions)
    previous_summary = spending_summary(previous_month)
    
    def calculate_trends(categories, trends):
        if not categories:
            return trends
        category = categories[0]
        trends[category] = current_summary.get(category, 0) - previous_summary.get(category, 0)
        return calculate_trends(categories[1:], trends)
    
    return calculate_trends(list(current_summary.keys()), {})

def spending_insights(trends: Dict[str, float], current_summary: Dict[str, float]) -> List[str]:
    """Provide insights into spending trends."""
    def generate_insights(categories, insights):
        if not categories:
            return insights
        category = categories[0]
        change = trends[category]
        current_amount = current_summary.get(category, 0)
        
        if current_amount == 0 and change == 0:
            insights.append(f"No change in spending for {category}.")
        elif current_amount == 0:
            insights.append(f"New spending on {category}: ${change:.2f}.")
        else:
            if current_amount - change != 0:
                if change > 0:
                    percentage_increase = (change / (current_amount - change)) * 100
                    insights.append(f"You spent {percentage_increase:.2f}% more on {category} this month.")
                elif change < 0:
                    percentage_decrease = (abs(change) / (current_amount + change)) * 100
                    insights.append(f"You spent {percentage_decrease:.2f}% less on {category} this month.")
            else:
                insights.append(f"Spending on {category} is unchanged, cannot calculate percentage.")
        
        return generate_insights(categories[1:], insights)
    
    return generate_insights(list(trends.keys()), [])
