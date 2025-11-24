# backend/db/demo_accounts.py

"""
Demo account storage for BlindTrust.
Used only for simulation purposes (no real money).
"""

# Dictionary of demo users and their balances
demo_balance = {
    "user": 10000,        # default user starting balance
    "john": 5000,
    "alice": 7000,
}

# List of valid beneficiaries for demo transfers
beneficiaries = ["john", "alice"]
