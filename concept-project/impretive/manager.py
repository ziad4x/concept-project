
import json
from collections import defaultdict
from transaction import Transaction
from datetime import datetime

class FinanceManager:
    def __init__(self):
        self.transactions = []
        self.savings_goals = []
        self.budgets = []  # To track budgets for different categories

    def add_transaction(self, amount, category, date, transaction_type):
        """Add a new transaction."""
        transaction = Transaction(amount, category, date, transaction_type)
        self.transactions.append(transaction)
        print(f"Added transaction: {transaction.amount} | {transaction.category} | {transaction.date} | {transaction.transaction_type}")

    def generate_report(self):
        report = defaultdict(float)
        for transaction in self.transactions:
            if transaction.transaction_type == 'expense':  # Only sum expenses
                report[transaction.category] += transaction.amount
        return report

    def generate_monthly_report(self):
        monthly_report = defaultdict(float)
        for transaction in self.transactions:
            month = datetime.strptime(transaction.date, "%Y-%m-%d").month
            if transaction.transaction_type == 'expense':  # Only sum expenses
                monthly_report[month] += transaction.amount
        return monthly_report

    def spending_insights(self):
        insights = []
        current_month = datetime.now().month
        current_year = datetime.now().year

        # Get current month's spending
        current_month_spending = self.generate_monthly_report().get(current_month, 0)
        
        # Get previous month's spending
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_month_spending = self.generate_monthly_report().get(previous_month, 0)

        # Overall spending trend
        if previous_month_spending > 0:
            overall_percentage_change = ((current_month_spending - previous_month_spending) / previous_month_spending) * 100
            insights.append(f"You spent {'{:.2f}'.format(abs(overall_percentage_change))}% {'more' if overall_percentage_change > 0 else 'less'} this month compared to last month.")

        # Category-wise spending insights
        category_spending = self.generate_report()
        for category in category_spending.keys():
            # Get current and previous month's spending for the category
            current_category_spending = category_spending[category]
            previous_category_spending = self.get_previous_month_category_spending(category, current_month)

            if previous_category_spending > 0:
                category_percentage_change = ((current_category_spending - previous_category_spending) / previous_category_spending) * 100
                insights.append(f"You spent {'{:.2f}'.format(abs(category_percentage_change))}% {'more' if category_percentage_change > 0 else 'less'} on {category} this month.")
            elif previous_category_spending == 0 and current_category_spending > 0:
                insights.append(f"You spent ${current_category_spending:.2f} on {category} this month, which is a new expense category for you.")
            else:
                insights.append(f"You did not spend on {category} this month.")

        return insights


    def get_previous_month_category_spending(self, category, current_month):
        """Get spending for a specific category from the previous month."""
        previous_month = current_month - 1 if current_month > 1 else 12
        previous_month_spending = sum(t.amount for t in self.transactions if 
                                    t.category == category and 
                                    datetime.strptime(t.date, "%Y-%m-%d").month == previous_month and 
                                    datetime.strptime(t.date, "%Y-%m-%d").year == datetime.now().year and 
                                    t.transaction_type == 'expense')
        return previous_month_spending



    def add_savings_goal(self, amount, target_date):
        self.savings_goals.append({
            'amount': amount,
            'target_date': target_date
        })

    def set_budget(self, category, limit):
        self.budgets.append({
            'category': category,
            'limit': limit
        })

    def import_data(self, file_path):
        try:
            with open(file_path, 'r') as file:
                if file_path.endswith('.csv'):
                    reader = csv.reader(file)
                    next(reader)  # Skip the header row
                    for row in reader:
                        if len(row) != 4:
                            print(f"Skipping invalid row: {row}")
                            continue
                        try:
                            amount, category, date, transaction_type = row
                            amount = float(amount.strip())
                            category = category.strip()
                            self.add_transaction(amount, category, date.strip(), transaction_type.strip())
                        except ValueError:
                            print(f"Error converting row: {row}")
                        except Exception as e:
                            print(f"Error importing row: {row}. Error: {e}")

                elif file_path.endswith('.json'):
                    data = json.load(file)
                    for entry in data['transactions']:
                        try:
                            amount = entry.get('Amount')
                            category = entry.get('Category')
                            date = entry.get('Date')
                            transaction_type = entry.get('Type')
                            if amount is None or category is None or date is None or transaction_type is None:
                                print(f"Skipping invalid entry: {entry}")
                                continue
                            self.add_transaction(amount, category, date, transaction_type)
                        except KeyError as e:
                            print(f"Missing key {e} in entry: {entry}")
                        except Exception as e:
                            print(f"Error importing entry: {entry}. Error: {e}")
        except Exception as e:
            print(f"Failed to open or read file: {file_path}. Error: {e}")

    def export_report(self, file_path):
        try:
            with open(file_path, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['Amount', 'Category', 'Date', 'Type'])  # Include all transaction details
                for transaction in self.transactions:
                    writer.writerow([transaction.amount, transaction.category, transaction.date, transaction.transaction_type])
            print(f"Report exported successfully to {file_path}")
        except Exception as e:
            print(f"Failed to export report: {e}")

    def track_budget(self):
        budget_status = {}
        for budget in self.budgets:
            category = budget['category']
            limit = budget['limit']
            total_spent = sum(t.amount for t in self.transactions if t.category == category and t.transaction_type == 'expense')
            remaining = limit - total_spent
            status = "Under Budget" if remaining >= 0 else "Over Budget"
            budget_status[category] = {
                'total_spent': total_spent,
                'remaining': remaining,
                'status': status
            }
        return budget_status
