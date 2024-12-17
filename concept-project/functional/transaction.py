# transaction.py
import csv
import json
from typing import List, Dict

def record_transaction(transactions: List[Dict], amount: float, category: str, date: str) -> List[Dict]:
    """Record a new transaction."""
    new_transaction = {'amount': amount, 'category': category, 'date': date}
    return transactions + [new_transaction]

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
        # Ensure each transaction is processed correctly
        return [{**transaction, 'amount': float(transaction['amount'])} for transaction in transactions if isinstance(transaction, dict)]


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
