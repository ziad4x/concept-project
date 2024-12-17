import csv
import json
from typing import List, Dict, Tuple
import os

# 1. Expense Tracking

def record_transaction(transactions: List[Dict], amount: float, category: str, date: str) -> List[Dict]:
    """Record a new transaction."""
    new_transaction = {'amount': amount, 'category': category, 'date': date}
    return transactions + [new_transaction]

def categorize_transactions(transactions: List[Dict], category: str) -> List[Dict]:
    """Filter transactions by category."""
    return [transaction for transaction in transactions if transaction['category'] == category]

# 2. Budgeting

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

# 3. Savings Goals

def set_savings_goal(goals: List[Dict], target: float, months: int) -> List[Dict]:
    """Define a savings goal."""
    monthly_savings = target / months
    goal = {'target': target, 'monthly_savings': monthly_savings, 'months_remaining': months}
    return goals + [goal]

def track_savings(goals: List[Dict], current_savings: float) -> List[str]:
    """Check progress towards savings goals."""
    return [f"${goal['target'] - current_savings} remaining for your goal of ${goal['target']}." for goal in goals]

# 4. Financial Analytics

def spending_summary(transactions: List[Dict]) -> Dict[str, float]:
    """Generate a spending summary by category."""
    summary = {}
    for transaction in transactions:
        category = transaction['category']
        summary[category] = summary.get(category, 0) + transaction['amount']
    return summary

def spending_trends(transactions: List[Dict], previous_month: List[Dict]) -> Dict[str, float]:
    """Compare spending trends between the current and previous month."""
    current_summary = spending_summary(transactions)
    previous_summary = spending_summary(previous_month)
    trends = {category: current_summary.get(category, 0) - previous_summary.get(category, 0)
              for category in current_summary}
    return trends

# 5. Data Import/Export

def import_transactions(file_path: str) -> List[Dict]:
    """Import transactions from a file (CSV or JSON)."""
    if file_path.endswith('.csv'):
        return import_transactions_from_csv(file_path)
    elif file_path.endswith('.json'):
        return import_transactions_from_json(file_path)
    else:
        raise ValueError("Unsupported file type. Please use CSV or JSON.")

def import_transactions_from_csv(file_path: str) -> List[Dict]:
    """Import transactions from a CSV file."""
    with open(file_path, newline='', mode='r') as file:
        reader = csv.DictReader(file)
        return [{**row, 'amount': float(row['amount'])} for row in reader]

def import_transactions_from_json(file_path: str) -> List[Dict]:
    """Import transactions from a JSON file."""
    with open(file_path, mode='r') as file:
        transactions = json.load(file)
        return [{**transaction, 'amount': float(transaction['amount'])} for transaction in transactions]

def export_transactions(file_path: str, transactions: List[Dict]) -> None:
    """Export transactions to a file (CSV or JSON)."""
    if file_path.endswith('.csv'):
        export_transactions_to_csv(file_path, transactions)
    elif file_path.endswith('.json'):
        export_transactions_to_json(file_path, transactions)
    else:
        raise ValueError("Unsupported file type. Please use CSV or JSON.")

def export_transactions_to_csv(file_path: str, transactions: List[Dict]) -> None:
    """Export transactions to a CSV file."""
    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=transactions[0].keys())
        writer.writeheader()
        writer.writerows(transactions)

def export_transactions_to_json(file_path: str, transactions: List[Dict]) -> None:
    """Export transactions to a JSON file."""
    with open(file_path, mode='w') as file:
        json.dump(transactions, file, indent=4)

# 6. Interactive User Input Functions

def get_user_input_for_transaction() -> Dict:
    """Get input from the user for a new transaction."""
    amount = float(input("Enter the transaction amount: "))
    category = input("Enter the category (e.g., Food, Rent, Entertainment): ")
    date = input("Enter the transaction date (YYYY-MM-DD): ")
    return {'amount': amount, 'category': category, 'date': date}

def get_user_input_for_budget() -> Tuple[str, float]:
    """Get input from the user for a new budget."""
    category = input("Enter the budget category (e.g., Food, Rent): ")
    amount = float(input(f"Enter the budget amount for {category}: "))
    return category, amount

def get_user_input_for_savings_goal() -> Tuple[float, int]:
    """Get input from the user for a new savings goal."""
    target = float(input("Enter your savings goal target: "))
    months = int(input("Enter the number of months to reach the target: "))
    return target, months

def get_user_input_for_file_import(file_type: str, files: List[str]) -> str:
    """Get the file path and format for importing transactions."""
    print(f"Select a {file_type.upper()} file to import:")

    for index, file in enumerate(files, start=1):
        print(f"{index}. {file}")

    file_choice = int(input(f"Enter the number of the {file_type.upper()} file: "))
    
    if 1 <= file_choice <= len(files):
        return files[file_choice - 1]  # return the selected file path
    else:
        print("Invalid choice. Please select a valid file number.")
        return None

# Example Usage

def main():
    # Predefined files in a directory
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    json_files = [f for f in os.listdir() if f.endswith('.json')]

    transactions = []
    budgets = {}
    goals = []

    while True:
        print("\n--- Personal Finance Management ---")
        print("1. Record a Transaction")
        print("2. Set a Budget")
        print("3. Track Budget Usage")
        print("4. Set a Savings Goal")
        print("5. View Spending Summary")
        print("6. View Spending Trends")
        print("7. View Budget Alerts")
        print("8. Import Transactions")
        print("9. Export Transactions")
        print("10. Exit")
        
        choice = input("Choose an option (1-10): ")

        if choice == '1':
            transaction = get_user_input_for_transaction()
            transactions = record_transaction(transactions, transaction['amount'], transaction['category'], transaction['date'])
            print(f"Transaction added: {transaction}")

        elif choice == '2':
            category, amount = get_user_input_for_budget()
            budgets = set_budget(budgets, category, amount)
            print(f"Budget set for {category}: ${amount}")

        elif choice == '3':
            usage = track_budget_usage(budgets, transactions)
            print("Budget Usage:")
            for category, amount in usage.items():
                print(f"{category}: ${amount}")

        elif choice == '4':
            target, months = get_user_input_for_savings_goal()
            goals = set_savings_goal(goals, target, months)
            print(f"Savings goal set: Target ${target} in {months} months")

        elif choice == '5':
            summary = spending_summary(transactions)
            print("Spending Summary:")
            for category, amount in summary.items():
                print(f"{category}: ${amount}")

        elif choice == '6':
            previous_month = []  # Placeholder for previous month's transactions
            trends = spending_trends(transactions, previous_month)
            print("Spending Trends (current vs previous month):")
            for category, trend in trends.items():
                print(f"{category}: ${trend}")

        elif choice == '7':
            usage = track_budget_usage(budgets, transactions)
            alerts = budget_alert(budgets, usage)
            print("Budget Alerts:")
            for alert in alerts:
                print(alert)

        elif choice == '8':
            # Ask user to choose file type first (CSV or JSON)
            print("Select the file type to import:")
            print("1. CSV")
            print("2. JSON")
            file_type_choice = input("Enter the number for the file type (1 or 2): ").strip()

            if file_type_choice == '1':
                if csv_files:
                    selected_file = get_user_input_for_file_import('csv', csv_files)
                    if selected_file:
                        try:
                            transactions = import_transactions(selected_file)
                            print(f"Transactions imported successfully from CSV file: {selected_file}")
                        except Exception as e:
                            print(f"Failed to import CSV file: {e}")
                    else:
                        print("Failed to import CSV file.")
                else:
                    print("No CSV files found in the current directory.")

            elif file_type_choice == '2':
                if json_files:
                    selected_file = get_user_input_for_file_import('json', json_files)
                    if selected_file:
                        try:
                            transactions = import_transactions(selected_file)
                            print(f"Transactions imported successfully from JSON file: {selected_file}")
                        except Exception as e:
                            print(f"Failed to import JSON file: {e}")
                    else:
                        print("Failed to import JSON file.")
                else:
                    print("No JSON files found in the current directory.")

            else:
                print("Invalid choice. Please enter either '1' or '2'.")

        elif choice == '9':
            # Export transactions
            file_type_choice = input("Enter the file type to export (CSV/JSON): ").strip().lower()
            if file_type_choice in ['csv', 'json']:
                file_name = input(f"Enter the name of the file to export (e.g., transactions.{file_type_choice}): ").strip()
                
                # Ensure the file name has the correct extension
                if not file_name.endswith(f".{file_type_choice}"):
                    file_name += f".{file_type_choice}"

                try:
                    export_transactions(file_name, transactions)
                    print(f"Transactions exported successfully to {file_name}.")
                except Exception as e:
                    print(f"Failed to export transactions: {e}")
            else:
                print("Invalid file type. Please enter 'CSV' or 'JSON'.")

        elif choice == '10':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
