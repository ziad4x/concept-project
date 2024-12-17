
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
import csv
import json
from manager import FinanceManager

class FinanceApp:
    def __init__(self, root):
        self.manager = FinanceManager()
        self.root = root
        self.root.title("Personal Finance Manager")
        self.root.minsize(600, 500)

        # Create a canvas and a scrollbar for scrolling content
        self.canvas = tk.Canvas(self.root)
        self.scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Create a frame to hold all the content
        self.main_frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.main_frame, anchor="nw")
        self.main_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Transaction Section
        self.transaction_frame = ttk.LabelFrame(self.main_frame, text="Transactions")
        self.transaction_frame.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.amount_label = ttk.Label(self.transaction_frame, text="Amount:")
        self.amount_label.grid(row=0, column=0, padx=5, pady=5)
        self.amount_entry = ttk.Entry(self.transaction_frame)
        self.amount_entry.grid(row=0, column=1, padx=5, pady=5)

        self.category_label = ttk.Label(self.transaction_frame, text="Category:")
        self.category_label.grid(row=1, column=0, padx=5, pady=5)
        self.category_entry = ttk.Entry(self.transaction_frame)
        self.category_entry.grid(row=1, column=1, padx=5, pady=5)

        self.date_label = ttk.Label(self.transaction_frame, text="Date (YYYY-MM-DD):")
        self.date_label.grid(row=2, column=0, padx=5, pady=5)
        self.date_entry = ttk.Entry(self.transaction_frame)
        self.date_entry.grid(row=2, column=1, padx=5, pady=5)

        self.type_label = ttk.Label(self.transaction_frame, text="Type (income/expense):")
        self.type_label.grid(row=3, column=0, padx=5, pady=5)
        self.type_entry = ttk.Entry(self.transaction_frame)
        self.type_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.transaction_frame, text="Add Transaction", command=self.add_transaction)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)

        self.transaction_list = ttk.Treeview(self.transaction_frame, columns=("Amount", "Category", "Date", "Type"), show='headings')
        self.transaction_list.heading("Amount", text="Amount")
        self.transaction_list.heading("Category", text="Category")
        self.transaction_list.heading("Date", text="Date")
        self.transaction_list.heading("Type", text="Type")
        self.transaction_list.grid(row=5, column=0, columnspan=2, pady=10, sticky='nsew')

        # Insights Button
        self.insights_button = ttk.Button(self.main_frame, text="Generate Spending Insights", command=self.show_insights)
        self.insights_button.grid(row=7, column=0, padx=10, pady=10)

        # Import and Export Buttons
        self.import_export_frame = ttk.Frame(self.main_frame)
        self.import_export_frame.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')

        self.import_button = ttk.Button(self.import_export_frame, text="Import", command=self.import_data)
        self.import_button.grid(row=0, column=0, padx=5, pady=5)

        self.export_button = ttk.Button(self.import_export_frame, text="Export", command=self.export_data)
        self.export_button.grid(row=0, column=1, padx=5, pady=5)

        # Budget Section
        self.budget_frame = ttk.LabelFrame(self.main_frame, text="Budget")
        self.budget_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.budget_category_label = ttk.Label(self.budget_frame, text="Category:")
        self.budget_category_label.grid(row=0, column=0, padx=5, pady=5)
        self.budget_category_entry = ttk.Entry(self.budget_frame)
        self.budget_category_entry.grid(row=0, column=1, padx=5, pady=5)

        self.budget_limit_label = ttk.Label(self.budget_frame, text="Limit:")
        self.budget_limit_label.grid(row=1, column=0, padx=5, pady=5)
        self.budget_limit_entry = ttk.Entry(self.budget_frame)
        self.budget_limit_entry.grid(row=1, column=1, padx=5, pady=5)

        self.set_budget_button = ttk.Button(self.budget_frame, text="Set Budget", command=self.set_budget)
        self.set_budget_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.budget_summary_label = ttk.Label(self.budget_frame, text="Budget Summary:")
        self.budget_summary_label.grid(row=3, column=0, columnspan=2, pady=5)
        self.budget_summary_text = tk.Text(self.budget_frame, height=5, width=40, state='disabled')
        self.budget_summary_text.grid(row=4, column=0, columnspan=2, pady=5)

        # Analytics Section
        self.analytics_frame = ttk.LabelFrame(self.main_frame, text="Financial Analytics")
        self.analytics_frame.grid(row=2, column=0, padx=10, pady=10, sticky='nsew')

        self.generate_report_button = ttk.Button(self.analytics_frame, text="Generate Analytics Report", command=self.generate_analytics_report)
        self.generate_report_button.grid(row=0, column=0, pady=10)

        self.analytics_report_text = tk.Text(self.analytics_frame, height=8, width=50, state='disabled')
        self.analytics_report_text.grid(row=1, column=0, pady=5)

        # Savings Goal Section
        self.savings_frame = ttk.LabelFrame(self.main_frame, text="Monthly Savings Goal")
        self.savings_frame.grid(row=3, column=0, padx=10, pady=10, sticky='nsew')

        self.savings_goal_label = ttk.Label(self.savings_frame, text="Savings Goal Amount:")
        self.savings_goal_label.grid(row=0, column=0, padx=5, pady=5)
        self.savings_goal_entry = ttk.Entry(self.savings_frame)
        self.savings_goal_entry.grid(row=0, column=1, padx=5, pady=5)

        self.savings_months_label = ttk.Label(self.savings_frame, text="Months to Save:")
        self.savings_months_label.grid(row=1, column=0, padx=5, pady=5)
        self.savings_months_entry = ttk.Entry(self.savings_frame)
        self.savings_months_entry.grid(row=1, column=1, padx=5, pady=5)

        self.calculate_savings_button = ttk.Button(self.savings_frame, text="Calculate Monthly Savings", command=self.calculate_monthly_savings)
        self.calculate_savings_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.monthly_savings_label = ttk.Label(self.savings_frame, text="Monthly Savings Required:")
        self.monthly_savings_label.grid(row=3, column=0, columnspan=2, pady=5)

        self.monthly_savings_result = ttk.Label(self.savings_frame, text="N/A")
        self.monthly_savings_result.grid(row=4, column=0, columnspan=2, pady=5)

    def show_insights(self):
        insights = self.manager.spending_insights()
        insights_text = "\n".join(insights)
        if insights_text:
            messagebox.showinfo("Spending Insights", insights_text)
        else:
            messagebox.showinfo("Spending Insights", "No spending insights available.")

    def add_transaction(self):
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()
        transaction_type = self.type_entry.get().lower()  # Ensure this is captured
        if amount and category and date and transaction_type in ['income', 'expense']:
            try:
                amount = float(amount)
                self.manager.add_transaction(amount, category, date, transaction_type)  # Pass transaction_type
                self.update_transaction_list()
            except ValueError:
                messagebox.showerror("Error", "Invalid amount entered!")
        else:
            messagebox.showerror("Error", "All fields must be filled and type must be income or expense!")

    def set_budget(self):
        category = self.budget_category_entry.get()
        limit = self.budget_limit_entry.get()
        if category and limit:
            try:
                limit = float(limit)
                self.manager.set_budget(category, limit)
                self.update_budget_summary()
            except ValueError:
                messagebox.showerror("Error", "Invalid limit entered!")
        else:
            messagebox.showerror("Error", "All fields must be filled!")

    def update_transaction_list(self):
        for row in self.transaction_list.get_children():
            self.transaction_list.delete(row)

        for transaction in self.manager.transactions:
            self.transaction_list.insert("", "end", values=(transaction.amount, transaction.category, transaction.date, transaction.transaction_type))

    def update_budget_summary(self):
        budget_summary = self.manager.track_budget()
        self.budget_summary_text.config(state='normal')
        self.budget_summary_text.delete(1.0, tk.END)
        for category, status in budget_summary.items():
            self.budget_summary_text.insert(tk.END, f"Category: {category}\n")
            self.budget_summary_text.insert(tk.END, f"  Total Spent: {status['total_spent']}\n")
            self.budget_summary_text.insert(tk.END, f"  Remaining: {status['remaining']}\n")
            self.budget_summary_text.insert(tk.END, f"  Status: {status['status']}\n\n")
        self.budget_summary_text.config(state='disabled')

    def generate_analytics_report(self):
        category_spending = self.manager.generate_report()
        monthly_spending = self.manager.generate_monthly_report()

        self.analytics_report_text.config(state='normal')
        self.analytics_report_text.delete(1.0, tk.END)

        self.analytics_report_text.insert(tk.END, "Category Spending:\n")
        for category, total in category_spending.items():
            self.analytics_report_text.insert(tk.END, f"{category}: {total}\n")

        self.analytics_report_text.insert(tk.END, "\nMonthly Spending Breakdown:\n")
        for month, total in monthly_spending.items():
            self.analytics_report_text.insert(tk.END, f"Month {month}: {total}\n")

        self.analytics_report_text.config(state='disabled')

    def calculate_monthly_savings(self):
        goal = self.savings_goal_entry.get()
        months = self.savings_months_entry.get()
        if goal and months:
            try:
                goal = float(goal)
                months = int(months)
                if months > 0:
                    monthly_savings = goal / months
                    self.monthly_savings_result.config(text=f"${monthly_savings:.2f}")
                else:
                    messagebox.showerror("Error", "Months must be greater than zero!")
            except ValueError:
                messagebox.showerror("Error", "Invalid input for savings goal or months!")
        else:
            messagebox.showerror("Error", "Both fields must be filled!")

    def import_data(self):
        file_type = [("CSV Files", "*.csv"), ("JSON Files", "*.json")]
        file_path = filedialog.askopenfilename(filetypes=file_type)
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    with open(file_path, 'r') as file:
                        reader = csv.DictReader(file)
                        for row in reader:
                            amount = float(row['Amount'])
                            category = row['Category']
                            date = row['Date']
                            transaction_type = row['Type']
                            self.manager.add_transaction(amount, category, date, transaction_type)
                elif file_path.endswith('.json'):
                    with open(file_path, 'r') as file:
                        data = json.load(file)
                        for entry in data['transactions']:
                            amount = entry['Amount']
                            category = entry['Category']
                            date = entry['Date']
                            transaction_type = entry['Type']
                            self.manager.add_transaction(amount, category, date, transaction_type)
                self.update_transaction_list()
                messagebox.showinfo("Success", "Data imported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to import data: {e}")

    def export_data(self):
        file_type = [("CSV Files", "*.csv"), ("JSON Files", "*.json")]
        file_path = filedialog.asksaveasfilename(filetypes=file_type, defaultextension=".csv")
        if file_path:
            try:
                if file_path.endswith('.csv'):
                    with open(file_path, 'w', newline='') as file:
                        writer = csv.writer(file)
                        writer.writerow(['Amount', 'Category', 'Date', 'Type'])
                        for transaction in self.manager.transactions:
                            writer.writerow([transaction.amount, transaction.category, transaction.date, transaction.transaction_type])
                elif file_path.endswith('.json'):
                    with open(file_path, 'w') as file:
                        json_data = {'transactions': [{'Amount': t.amount, 'Category': t.category, 'Date': t.date, 'Type': t.transaction_type} for t in self.manager.transactions]}
                        json.dump(json_data, file, indent=4)
                messagebox.showinfo("Success", "Data exported successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to export data: {e}")

