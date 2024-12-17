from typing import Dict, Tuple, List

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
