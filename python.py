
import uuid
import math

# Global dictionary to store bank data
all_loans = {} # Stores all loan details by loan_id

# --- Helper Function ---

def calculate_loan_details(principal, years, annual_rate):
    """Calculates total interest, total amount, and monthly EMI."""
    total_interest = principal * years * (annual_rate / 100)
    total_amount = principal + total_interest
    total_months = years * 12
    
    monthly_emi = 0
    if total_months > 0:
        monthly_emi = total_amount / total_months
    
    return total_interest, total_amount, monthly_emi, total_months

# --- Core Bank Functions ---

def LEND_money():
    """Handles the lending process with user input."""
    print("\n--- LEND MONEY ---")
    customer_id = input("Enter Customer ID: ").strip()
    
    try:
        loan_amount = float(input("Enter Loan Amount (P): "))
        loan_period_years = float(input("Enter Loan Period in Years (N): "))
        rate_of_interest = float(input("Enter Annual Rate of Interest (I in %): "))
    except ValueError:
        print("Invalid input. Please enter numbers for amount, period, and rate.")
        return

    if loan_amount < 0 or loan_period_years <= 0 or rate_of_interest < 0:
        print("Error: Loan amount, period, and rate must be positive numbers (rate can be zero).")
        return

    loan_interest, total_amount_to_pay, monthly_emi, original_num_emis = \
        calculate_loan_details(loan_amount, loan_period_years, rate_of_interest)

    loan_id = str(uuid.uuid4()) 

    all_loans[loan_id] = {
        "customer_id": customer_id,
        "principal_amount": loan_amount,
        "loan_period_years": loan_period_years,
        "annual_rate_of_interest": rate_of_interest,
        "total_interest": loan_interest,
        "total_amount_to_pay": total_amount_to_pay,
        "original_monthly_emi": monthly_emi,
        "current_outstanding_balance": total_amount_to_pay,
        "payments_made": [],
        "original_number_of_emis": original_num_emis
    }

    print(f"\n--- LOAN ISSUED ---")
    print(f"Loan ID: {loan_id}")
    print(f"Customer ID: {customer_id}")
    print(f"Loan Amount (P): ${loan_amount:.2f}")
    print(f"Total Amount to Pay (A): ${total_amount_to_pay:.2f}")
    print(f"Monthly EMI: ${monthly_emi:.2f}")

def MAKE_PAYMENT():
    """Handles loan payments with user input."""
    print("\n--- MAKE PAYMENT ---")
    loan_id = input("Enter Loan ID: ").strip()

    if loan_id not in all_loans:
        print(f"Error: Loan ID '{loan_id}' not found.")
        return

    try:
        payment_amount = float(input("Enter Payment Amount: "))
    except ValueError:
        print("Invalid input. Please enter a number for the payment amount.")
        return

    if payment_amount <= 0:
        print("Error: Payment amount must be positive.")
        return

    payment_type = input("Enter Payment Type (EMI or LUMP SUM): ").strip().upper()
    if payment_type not in ["EMI", "LUMP SUM"]:
        print("Error: Invalid payment type. Please enter 'EMI' or 'LUMP SUM'.")
        return

    loan = all_loans[loan_id]

    if loan["current_outstanding_balance"] <= 0:
        print(f"Loan ID '{loan_id}' is already fully paid.")
        return

    amount_to_deduct = min(payment_amount, loan["current_outstanding_balance"])
    loan["current_outstanding_balance"] -= amount_to_deduct
    
    loan["payments_made"].append({
        "type": payment_type,
        "amount": amount_to_deduct
    })

    print(f"\n--- PAYMENT PROCESSED ---")
    print(f"Loan ID: {loan_id}")
    print(f"Payment Type: {payment_type}")
    print(f"Amount Paid: ${amount_to_deduct:.2f}")
    print(f"Remaining Balance: ${loan['current_outstanding_balance']:.2f}")

def VIEW_LEDGER():
    """Displays loan transaction ledger with user input."""
    print("\n--- VIEW LOAN LEDGER ---")
    loan_id = input("Enter Loan ID: ").strip()

    if loan_id not in all_loans:
        print(f"Error: Loan ID '{loan_id}' not found.")
        return

    loan = all_loans[loan_id]

    current_balance = loan["current_outstanding_balance"]
    monthly_emi = loan["original_monthly_emi"]
    
    emis_left = 0
    if monthly_emi > 0:
        emis_left = math.ceil(current_balance / monthly_emi)

    print(f"\n--- LOAN LEDGER FOR ID: {loan_id} ---")
    print(f"Balance Amount: ${current_balance:.2f}")
    print(f"Monthly EMI: ${monthly_emi:.2f}")
    print(f"Number of EMIs Left: {emis_left}")

    print("\nTransactions:")
    if not loan["payments_made"]:
        print("  No transactions recorded yet.")
    else:
        for i, transaction in enumerate(loan["payments_made"]):
            print(f"  {i+1}. Type: {transaction['type']}, Amount: ${transaction['amount']:.2f}")

def VIEW_ACCOUNT_OVERVIEW():
    """Displays all loans for a customer with user input."""
    print("\n--- ACCOUNT OVERVIEW ---")
    customer_id = input("Enter Customer ID: ").strip()
    
    found_loans = False
    for loan_id, loan in all_loans.items():
        if loan["customer_id"] == customer_id:
            found_loans = True
            
            amount_paid_till_date = loan["total_amount_to_pay"] - loan["current_outstanding_balance"]
            
            emis_left = 0
            if loan["original_monthly_emi"] > 0:
                emis_left = math.ceil(loan["current_outstanding_balance"] / loan["original_monthly_emi"])

            print(f"\n--- Loan ID: {loan_id} ---")
            print(f"  Loan Amount (P): ${loan['principal_amount']:.2f}")
            print(f"  Total Amount (A): ${loan['total_amount_to_pay']:.2f}")
            print(f"  EMI Amount: ${loan['original_monthly_emi']:.2f}")
            print(f"  Total Interest (I): ${loan['total_interest']:.2f}")
            print(f"  Amount Paid Till Date: ${amount_paid_till_date:.2f}")
            print(f"  Number of EMIs Left: {emis_left}")
            
    if not found_loans:
        print(f"No loans found for customer ID: {customer_id}")

# --- Main Program Loop ---

def run_bank_system():
    """Runs the interactive bank system."""
    while True:
        print("\n--- BANK SYSTEM MENU ---")
        print("1. Lend Money (LEND)")
        print("2. Make Payment (PAYMENT)")
        print("3. View Loan Ledger (LEDGER)")
        print("4. View Account Overview (ACCOUNT OVERVIEW)")
        print("5. Exit")
        
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            LEND_money()
        elif choice == '2':
            MAKE_PAYMENT()
        elif choice == '3':
            VIEW_LEDGER()
        elif choice == '4':
            VIEW_ACCOUNT_OVERVIEW()
        elif choice == '5':
            print("Exiting Bank System. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 5.")

if __name__ == "__main__":
    run_bank_system()
