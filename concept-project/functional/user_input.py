from typing import Dict, List  # Ensure List is imported

def get_user_input_for_transaction() -> Dict:
    """Get input from the user for a new transaction."""
    amount = float(input("Enter the transaction amount: "))
    category = input("Enter the category (e.g., Food, Rent, Entertainment): ")
    date = input("Enter the transaction date (YYYY-MM-DD): ")
    transaction_type = input("Enter the transaction type (income/expense): ").strip().lower()
    
    if transaction_type not in ['income', 'expense']:
        raise ValueError("Transaction type must be either 'income' or 'expense'.")
    
    return {'amount': amount, 'category': category, 'date': date, 'type': transaction_type}

def get_user_input_for_budget() -> Dict:
    """Get input from the user for a new budget."""
    category = input("Enter the budget category (e.g., Food, Rent): ")
    amount = float(input(f"Enter the budget amount for {category}: "))
    return category, amount

def get_user_input_for_savings_goal() -> Dict:
    """Get input from the user for a new savings goal."""
    target = float(input("Enter your savings goal target: "))
    months = int(input("Enter the number of months to reach the target: "))
    return target, months

def get_user_input_for_file_import(file_type: str, files: List[str]) -> str:
    """Get the file path and format for importing transactions."""
    print(f"Select a {file_type.upper()} file to import:")

    def list_files(files, index=1):
        if index > len(files):
            return
        print(f"{index}. {files[index - 1]}")
        list_files(files, index + 1)

    list_files(files)

    file_choice = int(input(f"Enter the number of the {file_type.upper()} file: "))
    
    if 1 <= file_choice <= len(files):
        return files[file_choice - 1]  # return the selected file path
    else:
        print("Invalid choice. Please select a valid file number.")
        return None
