# main.py
import os
from transaction import record_transaction, import_transactions, export_transactions
from budget import set_budget, track_budget_usage, budget_alert
from savings import set_savings_goal, display_savings_goal_details
from analytics import spending_summary, overall_spending, spending_trends, spending_insights
from user_input import (get_user_input_for_transaction, get_user_input_for_budget,
                        get_user_input_for_savings_goal, get_user_input_for_file_import)

def main():
    csv_files = [f for f in os.listdir() if f.endswith('.csv')]
    json_files = [f for f in os.listdir() if f.endswith('.json')]

    transactions = []
    budgets = {}
    goals = []
    previous_month_transactions = []

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
            try:
                goals = set_savings_goal(goals, target, months)
                print(display_savings_goal_details(goals[-1]))
            except ValueError as e:
                print(e)

        elif choice == '5':
            summary = spending_summary(transactions)
            total_spending = overall_spending(transactions)
            print("Spending Summary:")
            for category, amount in summary.items():
                print(f"{category}: ${amount}")
            print(f"Total Spending: ${total_spending}")

        elif choice == '6':
            trends = spending_trends(transactions, previous_month_transactions)
            print("Spending Trends (current vs previous month):")
            for category, trend in trends.items():
                print(f"{category}: ${trend}")
            
            current_summary = spending_summary(transactions)
            insights = spending_insights(trends, current_summary)
            print("Spending Insights:")
            for insight in insights:
                print(insight)

        elif choice == '7':
            usage = track_budget_usage(budgets, transactions)
            alerts = budget_alert(budgets, usage)
            print("Budget Alerts:")
            for alert in alerts:
                print(alert)

        elif choice == '8':
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
                    print("No JSON files found in the current directory.")

            else:
                print("Invalid choice. Please enter either '1' or '2'.")

        elif choice == '9':
            print("Select the file type to export:")
            print("1. CSV")
            print("2. JSON")
            
            file_type_choice = input("Enter the number for the file type (1 or 2): ").strip()

            if file_type_choice == '1':
                file_name = input("Enter the name of the file to export (e.g., transactions.csv): ").strip()
                if not file_name.endswith('.csv'):
                    file_name += '.csv'
                try:
                    export_transactions(file_name, transactions)
                    print(f"Transactions exported successfully to {file_name}.")
                except Exception as e:
                    print(f"Failed to export transactions: {e}")

            elif file_type_choice == '2':
                file_name = input("Enter the name of the file to export (e.g., transactions.json): ").strip()
                if not file_name.endswith('.json'):
                    file_name += '.json'
                try:
                    export_transactions(file_name, transactions)
                    print(f"Transactions exported successfully to {file_name}.")
                except Exception as e:
                    print(f"Failed to export transactions: {e}")

            else:
                print("Invalid choice. Please enter either '1' (CSV) or '2' (JSON).")

        elif choice == '10':
            print("Exiting the program.")
            break
        
        else:
            print("Invalid choice, please try again.")

if __name__ == "__main__":
    main()
