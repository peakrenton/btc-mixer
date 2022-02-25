#!/usr/bin/env python
import pytest
import re
from project.jobcoin.jobcoin_network import JobcoinAPINetwork

def is_close(amount1: str, amount2: str) -> bool:
    return True

def transaction_contains(xacts: dict, fromAddress: str, toAddress: str, amount: str) -> bool:
    list_of_xact = xacts["transactions"]
    for xact in list_of_xact:
        if (fromAddress == None or xact["fromAddress"]==fromAddress) and xact["toAddress"]==toAddress and is_close(xact["amount"], amount):
            return True
    
    return False


@pytest.fixture
def before_all():
    network = JobcoinAPINetwork()
    deposit_1 = network.add_addresses(["0x4g7z", "0x8a54"])
    amount = '100.0'
    network.send(JobcoinAPINetwork.MINTED, deposit_1, amount)
    return network, deposit_1, amount

def test_address_created(before_all):
    network, deposit_1, amount = before_all
    address_create_output = network.add_addresses(["0xp45", "0x8a45"])
    output_re = re.compile(
        r'[0-9a-zA-Z]{32}'
    )
    assert output_re.search(address_create_output) is not None

def test_minting(before_all):
    network, deposit_1, amount = before_all
    my_transactions = network.get_transactions(deposit_1)
    output_str = '"toAddress":"{}","amount":"{}"'.format(deposit_1, amount)

    assert output_str in my_transactions

def test_simple_send(before_all):
    network, deposit_1, amount_1 = before_all

    deposit_2 = network.add_addresses(["0xf001", "0x200d"])
    amount_2 = "90.0"
    network.send(deposit_1, deposit_2, amount_2)

    account_1_transactions = network.get_transactions(deposit_1)
    account_2_transactions = network.get_transactions(deposit_2)

    output_string_2 = '"fromAddress":"{}","toAddress":"{}","amount":"{}"'.format(deposit_1, deposit_2, amount_2)

    assert transaction_contains(account_1_transactions, None, deposit_1, amount_1)
    assert transaction_contains(account_2_transactions, deposit_1, deposit_2, amount_2)

    assert account_1_transactions['balance'] == "10.0"
    assert account_2_transactions['balance'] == "90.0"


# def test_insufficient_balance(before_all):
#     network, deposit_1, amount_1 = before_all

#     deposit_2 = network.add_addresses(["0xf001", "0x200d"])
#     amount_2 = "200.0"

#     with pytest.raises(InsufficientBalanceException):
#         network.send(deposit_1, deposit_2, amount_2)

# def test_sender_address_no_exists():
#     network = JobcoinNetwork()
#     sender_address = "0x90y6"
#     receiver_address = "0xf712"

#     with pytest.raises(DepositAddressDoesntExistException):
#         network.send(sender_address, receiver_address, '200.0')

# def test_receiver_address_no_exists(before_all):
#     network, sender_address, amount = before_all
#     receiver_address = "0xd7fe"

#     with pytest.raises(DepositAddressDoesntExistException):
#         network.send(sender_address, receiver_address, '200.0')

# def test_balance(before_all):
#     network, deposit_1, amount = before_all
#     deposit_2 = network.add_addresses(["0xf001", "0x200d"])
#     amount_2 = "50.0"
#     network.send(deposit_1, deposit_2, amount_2)
#     deposit_3 = network.add_addresses(["0x7j4f", "0x20a"])
#     amount_3 = "30.0"
#     network.send(deposit_1, deposit_3, amount_3)

#     assert "balance: 18" in network.get_transactions(deposit_1)
#     assert "balance: 49" in network.get_transactions(deposit_2)
#     assert "balance: 29.4" in network.get_transactions(deposit_3)
#     assert network.get_fees_collected() == pytest.approx((float(amount) + float(amount_2) + float(amount_3)) * 0.02)