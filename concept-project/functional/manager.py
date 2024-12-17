# import csv
# import json
# from typing import List, Dict, Tuple

# # Data types
# Transaction = Dict[str, float]
# CategorySummary = Dict[str, float]
# Budget = Dict[str, float]
# SavingsGoal = Dict[str, float]
# Summary = Dict[str, float]
# Trend = Dict[str, str]

# # Functions
# # Record daily transactions
# def add_transaction(transactions: List[Transaction], category: str, amount: float, is_income: bool) -> List[Transaction]:
#     return transactions + [{"category": category, "amount": amount if is_income else -amount}]

# # Categorize transactions
# def categorize_transactions(transactions: List[Transaction]) -> CategorySummary:
#     summary = {}
#     for t in transactions:
#         category = t["category"]
#         summary[category] = summary.get(category, 0) + t["amount"]
#     return summary

# # Set budgets
# def set_budget(budgets: Budget, category: str, amount: float) -> Budget:
#     return {**budgets, category: amount}

# # Track budget utilization and alert
# def budget_alert(transactions: List[Transaction], budgets: Budget) -> List[str]:
#     alerts = []
#     categorized = categorize_transactions(transactions)
#     for category, actual in categorized.items():
#         if category in budgets and actual > budgets[category]:
#             alerts.append(f"Alert: You've exceeded your budget for {category} by ${actual - budgets[category]:.2f}")
#     return alerts

# # Define savings goals
# def set_savings_goal(goals: SavingsGoal, name: str, target: float) -> SavingsGoal:
#     return {**goals, name: target}

# # Recommend monthly savings
# def calculate_savings_recommendation(goals: SavingsGoal, months: int) -> Dict[str, float]:
#     return {goal: target / months for goal, target in goals.items()}

# # Generate spending summary
# def generate_summary(transactions: List[Transaction]) -> Summary:
#     total_spending = sum(-t["amount"] for t in transactions if t["amount"] < 0)
#     total_income = sum(t["amount"] for t in transactions if t["amount"] > 0)
#     return {"Total Income": total_income, "Total Spending": total_spending}

# # Spending trends
# def spending_trends(transactions: List[Transaction]) -> Trend:
#     categorized = categorize_transactions(transactions)
#     total = sum(categorized.values())
#     return {cat: f"{(amount / total) * 100:.2f}%" for cat, amount in categorized.items()}

# # Import data
# def import_transactions(file_path: str, file_type: str) -> List[Transaction]:
#     transactions = []
#     if file_type == "csv":
#         with open(file_path, "r") as f:
#             reader = csv.DictReader(f)
#             transactions = [{"category": row["category"], "amount": float(row["amount"])} for row in reader]
#     elif file_type == "json":
#         with open(file_path, "r") as f:
#             transactions = json.load(f)
#     return transactions

# # Export report
# def export_report(report: Summary, file_path: str) -> None:
#     with open(file_path, "w") as f:
#         json.dump(report, f, indent=4)
