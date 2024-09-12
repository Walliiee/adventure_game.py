class BankAccount:
    def __init__(self, first_name, last_name, account_id, account_type, pin, balance):
        self.first_name = first_name
        self.last_name = last_name
        self.account_id = account_id
        self.account_type = account_type
        self.pin = pin
        self.balance = balance

    def deposit(self, amount):
      if self.pin == 1234 and self.account_id == 3456789:
        self.balance += amount
        print(f'You have deposited: ${amount} to your account and your balance is: {self.balance}')

    def withdraw(self, amount):
      if self.pin == 1234 and self.account_id == 3456789 and self.balance > amount:
        self.balance -= amount
        print(f'You have withdrawn: ${amount} from your account and your balance is: {self.balance}')
      else:
        print('Insufficient funds')


    def display_balance(self):
      print('Dear ' + self.last_name + 'your total balance is: ' + self.balance)


Mikes_account = BankAccount('Mike', 'Krohn', 3456789, 'Credit', 1234, 1036.55)

Mikes_account.deposit(300)
Mikes_account.withdraw(25)

print(vars(Mikes_account))