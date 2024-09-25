from _datetime import datetime, timedelta

bank_accounts = {
    1001: {
        "first_name": "Alice",
        "last_name": "Smith",
        "id_number": "123456789",
        "balance": 2500.50,
        "transactions_to_execute": [
            ("2024-08-17 14:00:00", 1001, 1002, 300), ("2024-08-17 15:00:00", 1001, 1003, 200)],
        "transaction_history": [
            ("2024-08-15 09:00:00", 1001, 1002, 500, "2024-08-15 09:30:00")]
    },
    1002: {
        "first_name": "Bob",
        "last_name": "Johnson",
        "id_number": "987654321",
        "balance": 3900.75,
        "transactions_to_execute": [],
        "transaction_history": []
    },
    1003: {
        "first_name": "Ofir",
        "last_name": "Baranes",
        "id_number": "12345677",
        "balance": 100000000,
        "transactions_to_execute": [],
        "transaction_history": [("2024-09-08 09:00:00", 1003, 1002, 500, "2024-08-15 09:30:00")]
    }
}


def create_new_account():
    try:
        first_name = input("Please enter your first name: ")
        last_name = input("Please enter your last name: ")
        id_number = int(input("Please enter your ID number: "))
        accountnums: list[int] = [accountnum for accountnum in bank_accounts.keys()]
        account_number = accountnums[-1] + 1
        bank_accounts[account_number] = {
            "first_name": first_name,
            "last_name": last_name,
            "id_number": id_number,
            "balance": 1000,
            "transactions_to_execute": [],
            "transaction_history": []
        }
        print(f"Account created successfully! Your account number is {account_number}.")
    except Exception as e:
        print(f"Error occurred while creating the account: {e}")


def view_account(a: int):
    try:
        account = bank_accounts.get(a)
        if account:
            print(f"Account number: {a}")
            print(f"First name: {account.get('first_name')}\n"
                  f"Last name: {account.get('last_name')}\n"
                  f"ID number: {account.get('id_number')}\n"
                  f"Balance: {account.get('balance')}\n"
                  f"Transactions to execute: {account.get('transactions_to_execute')}\n"
                  f"Transactions history: {account.get('transaction_history')}\n")
        else:
            print("Account not found.")
    except Exception as e:
        print(f"Error occurred while viewing the account: {e}")


def reports():
    while True:
        try:
            print("-=Welcome to the reports system=-\n"
                  "Press 1 to print all the bank accounts.\n"
                  "Press 2 to find and print a specific account.\n"
                  "Press 3 to find an account by ID.\n"
                  "Press 4 to find an account by First Name.\n"
                  "Press 5 to print all the accounts sort by balance.\n"
                  "Press 6 to print all the history transaction from all account (sorted)\n"
                  "Press 7 to print all transactions from today.\n"
                  "Press 8 to print all accounts with negative balance.\n"
                  "Press 9 to print the total balance for all existing accounts.\n"
                  "Press 10 to exit to main menu.")

            user_selection: int = int(input("Please enter your selection: "))
            accountnums: list[int] = [accountnum for accountnum in bank_accounts.keys()]

            if user_selection == 10:
                break
            if user_selection == 1:
                for i in range(len(accountnums)):
                    view_account(accountnums[i])
                break
            if user_selection == 2:
                bank_ac: int = int(input("Please enter the bank account No. :"))
                while bank_ac not in bank_accounts:
                    print(f"account number: {bank_ac} does not in the system!\n"
                          f"Try again..")
                    bank_ac: int = int(input("Please enter the bank account No. :"))
                view_account(bank_ac)
                break
            if user_selection == 3:
                id_selection: str = input("Please enter the ID number to print all the accounts connected: ")
                for i in range(len(accountnums)):
                    if id_selection == bank_accounts.get(accountnums[i]).get("id_number"):
                        print(bank_accounts.get(accountnums[i]))
            if user_selection == 4:
                first_name: str = input("Please enter the first name of the account you like to find: ").lower()
                for i in range(len(accountnums)):
                    if first_name in bank_accounts.get(accountnums[i]).get("first_name").lower():
                        print(bank_accounts.get(accountnums[i]))
            if user_selection == 5:
                sorted_accounts = sorted(bank_accounts.keys(),
                                         key=lambda account_num: bank_accounts[account_num]["balance"])
                for account_num in sorted_accounts:
                    view_account(account_num)
            if user_selection == 6:
                all_trans: list = []
                for account_num in accountnums:
                    transactions_history = bank_accounts.get(account_num).get("transaction_history")
                    if transactions_history:
                        all_trans.extend(transactions_history)
                print(sorted(all_trans, key=lambda h: h[0]))
            if user_selection == 7:
                all_trans: list = []
                for account_num in accountnums:
                    transactions_history = bank_accounts.get(account_num).get("transaction_history")
                    if transactions_history:
                        all_trans.extend(transactions_history)

                today = datetime.today().date()
                todays_transactions = [trans for trans in all_trans if
                                       datetime.strptime(trans[0], "%Y-%m-%d %H:%M:%S").date() == today]
                print(todays_transactions)

            if user_selection == 8:
                for account in bank_accounts:
                    if bank_accounts.get(account).get("balance") < 0:
                        view_account(account)

            if user_selection == 9:
                total_balance: float = 0
                for account in bank_accounts:
                    total_balance += bank_accounts.get(account).get("balance")
                print(f"the total balance for all of the existing account is: {total_balance}")
            else:
                print("Please enter a number between 1-10 !")
        except ValueError:
            print("Invalid input. Please enter a valid number between 1 and 10.")


def add_tran() -> tuple:
    try:
        while True:
            from_b = int(input("Please enter an existing bank account to transfer from: "))
            if from_b not in bank_accounts.keys():
                print("-=bank account not in the system=-")
                continue
            break
        while True:
            to_b = int(input("Please enter an existing bank account to transfer to: "))
            if to_b not in bank_accounts.keys():
                print("-=bank account not in the system=-")
                continue
            break
        amount = float(input("Please enter the amount to transfer: "))
        if amount <= 0:
            raise ValueError("Amount must be greater than zero.")
        time_now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return time_now, from_b, to_b, amount
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An error occurred: {e}")


def ex_tran():
    try:
        while True:
            from_b = int(input("Please enter an existing bank account to execute transactions: "))
            if from_b not in bank_accounts.keys():
                print("-=bank account not in the system=-")
                continue
            break
        transactions: list = bank_accounts.get(from_b).get("transactions_to_execute")
        if not transactions:
            print("No transactions to execute.")
            return

        amount_to_reduce: float = 0
        history_note = []

        for transaction in transactions:
            from_account = bank_accounts.get(from_b)
            to_b = transaction[2]
            amount = transaction[3]

            if from_account["balance"] < amount:
                print(f"Not enough balance in account {from_b} to transfer {amount}.")
                continue

            bank_accounts.get(to_b)["balance"] += amount
            from_account["balance"] -= amount
            amount_to_reduce += amount

            for detail in transaction:
                history_note.append(detail)
            time_now: str = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            history_note.append(time_now)
            from_account["transaction_history"].append(history_note)
            history_note = []

        bank_accounts.get(from_b)["transactions_to_execute"].clear()
        view_account(from_b)
    except ValueError as ve:
        print(f"Value error: {ve}")
    except Exception as e:
        print(f"An error occurred during transaction execution: {e}")


print("-=Welcome to the Bank of Ofir=-")
while True:
    try:
        print("-Enter 1 to add transaction to specific bank account\n"
              "-Enter 2 to add all waiting transactions to all accounts\n"
              "-Enter 3 to view reports\n"
              "-Enter 4 to create a new account.\n"
              "-Enter 5 to exit the system")
        user_choice: int = int(input("Please enter your request: "))

        if user_choice == 1:
            trans: tuple = add_tran()
            if trans:
                bank_accounts.get(trans[1])["transactions_to_execute"].append(trans)
                print("Transaction added successfully!")

        elif user_choice == 2:
            ex_tran()

        elif user_choice == 3:
            reports()

        elif user_choice == 4:
            create_new_account()

        elif user_choice == 5:
            print("Thanks for using our system!\n"
                  "SEE YOU SOON!")
            break

        else:
            print("Invalid option. Please select a number between 1-5.")

    except ValueError:
        print("Invalid input. Please enter a number.")