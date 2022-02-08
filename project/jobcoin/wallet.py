from typing import List

from project.jobcoin.transaction import Transaction

class Wallet:
    """
    A wallet is owned by a user, who provides a list of unique private addresses.
    """
    def __init__(self, private_addresses: List[str], deposit_address: str):
        self.private_addresses = private_addresses
        self.deposit_address = deposit_address
        self.balance = 0.0
        self.transactions = []

    def get_num_addresses(self) -> int:
        """
        Get number of private addresses associated with wallet.

        Returns:
            int: Number of addresses.
        """        
        return len(self.private_addresses)

    def get_balance(self) -> float:
        """
        Get balance of wallet.

        Returns:
            float: Wallet balance as float.
        """        
        return self.balance
    
    def increase_balance(self, amount: float) -> None:
        """
        Add amount to wallet balance.

        Args:
            amount (float): Amount to be deposited in wallet.
        """        
        self.balance += amount

    def decrease_balance(self, amount: float):
        """
        Deduct amount from wallet balance.

        Args:
            amount (float): Amount to be withdrawn from wallet.
        """        
        self.balance -= amount
    
    def add_transaction(self, transaction: Transaction) -> None:
        """
        Add transaction to list of transactions associated with wallet.

        Args:
            transaction (Transaction): Valid transaction.
        """        
        self.transactions.append(transaction)
    
    def get_transaction_history(self):
        """
        Returns a human readable summary of wallet, with balance and summary of associated transactions.

        Returns:
            str: Summary of wallet including current balance and a list of transaction summaries.
            example: "balance: 88.2, ["{'timestamp': '2022-02-08T05:04:06.631305+00:00', 'fromAddress': '65..34', 'toAddress': '1e..1b', 'amount': '90.0'"
        """           
        return "balance: {}, {}".format(self.balance, [xact.return_transaction() for xact in self.transactions])