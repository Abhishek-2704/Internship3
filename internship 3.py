import json
from datetime import datetime

class ExpenseTracker:
    def __init__(self):
        self.expenses = []
        self.categories = ["Food", "Transportation", "Entertainment", "Bills", "Miscellaneous"]
        self.load_data()

    def load_data(self):
        """Load expense data from a file."""
        try:
            with open('expenses.json', 'r') as file:
                self.expenses = json.load(file)
        except FileNotFoundError:
            self.expenses = []
        except json.JSONDecodeError:
            print("Error: Unable to decode the expense data.")
            self.expenses = []

    def save_data(self):
        """Save expense data to a file."""
        try:
            with open('expenses.json', 'w') as file:
                json.dump(self.expenses, file, indent=4)
        except IOError:
            print("Error: Unable to save the expense data.")

    def add_expense(self):
        """Prompt user to add a new expense to the tracker."""
        try:
            amount = float(input("Enter the amount spent: "))
            description = input("Enter a brief description of the expense: ")

            # Display the available categories
            print("\nAvailable Categories:")
            for idx, category in enumerate(self.categories, 1):
                print(f"{idx}. {category}")

            # Prompt user to enter a category by selecting the number
            category_choice = input("Enter the category number or type the category name: ")
            
            # Determine the category based on user input
            if category_choice.isdigit():
                category_index = int(category_choice) - 1
                if 0 <= category_index < len(self.categories):
                    category = self.categories[category_index]
                else:
                    print("Error: Invalid category number.")
                    return
            elif category_choice in self.categories:
                category = category_choice
            else:
                print("Error: Invalid category name.")
                return

            expense = {
                "amount": amount,
                "description": description,
                "category": category,
                "date": datetime.now().strftime("%Y-%m-%d")
            }
            self.expenses.append(expense)
            print("Expense added successfully!")
            self.save_data()

        except ValueError:
            print("Error: Please enter a valid number for the amount.")

    def view_expenses(self):
        """Display all expenses."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        print("Date\t\tAmount\tCategory\tDescription")
        print("-" * 50)
        for expense in self.expenses:
            print(f"{expense['date']}\t{expense['amount']}\t{expense['category']}\t{expense['description']}")

    def view_summary(self):
        """Provide a summary of expenses by category and month."""
        if not self.expenses:
            print("No expenses recorded yet.")
            return

        summary = {}
        for expense in self.expenses:
            category = expense['category']
            month = expense['date'][:7]  # Extract the 'YYYY-MM' part
            if month not in summary:
                summary[month] = {cat: 0 for cat in self.categories}

            summary[month][category] += expense['amount']

        print("Monthly Expense Summary:")
        for month, data in summary.items():
            print(f"\nMonth: {month}")
            for category, total in data.items():
                print(f"{category}: {total:.2f}")

def main():
    tracker = ExpenseTracker()
    while True:
        print("\nExpense Tracker Menu:")
        print("1. Add Expense")
        print("2. View All Expenses")
        print("3. View Expense Summary")
        print("4. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            tracker.add_expense()
        elif choice == '2':
            tracker.view_expenses()
        elif choice == '3':
            tracker.view_summary()
        elif choice == '4':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please choose a valid option.")

if __name__ == "__main__":
    main()
