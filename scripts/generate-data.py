import os
from pymongo import MongoClient
from dotenv import load_dotenv
from faker import Faker
from werkzeug.security import generate_password_hash

# Load environment variables from the .env file
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# Get the MongoDB URI from environment variables
MONGO_URI = os.getenv('MONGO_URI')
print(MONGO_URI)
# Establish a connection to MongoDB
client = MongoClient(MONGO_URI)
db = client['bank-api']

fake = Faker()

# Define a common password for all users
common_password = "password123"
common_password_hash = generate_password_hash(common_password)


def get_existing_roles():
    roles = db.roles.find()
    return [role['role_name'] for role in roles]


def generate_fake_users(count=100):
    print("Generating users...")
    users = []
    existing_roles = get_existing_roles()
    for _ in range(count):
        user_roles = fake.random_elements(
            elements=existing_roles, unique=False, length=fake.random_int(min=1, max=3))
        users.append({
            "email": fake.email(),
            "password_hash": common_password_hash,
            "roles": user_roles,
            "first_name": fake.first_name(),
            "last_name": fake.last_name(),
            "address": fake.address(),
            "created_at": fake.date_time_this_year()
        })
    return users


def generate_fake_accounts(users):
    accounts = []
    for user in users:
        account_count = fake.random_int(min=1, max=3)
        for _ in range(account_count):
            balance = fake.random_int(min=-600, max=10000)
            account = {
                "user_id": user["_id"],
                "account_number": fake.iban(),
                "balance": balance,
                "currency": fake.random_element(elements=("EUR", "USD")),
                "status": "active",
                "created_at": fake.date_time_this_year()
            }
            accounts.append(account)
    return accounts


def generate_fake_transactions(accounts, min_transactions_per_account=5):
    transactions = []
    for account in accounts:
        for _ in range(min_transactions_per_account):
            from_account = account
            to_account = fake.random_element(elements=accounts)
            while to_account == from_account:
                to_account = fake.random_element(elements=accounts)
            transaction = {
                "from_account": from_account["account_number"],
                "to_account": to_account["account_number"],
                "amount": fake.random_int(min=-500, max=500),
                "currency": from_account["currency"],
                "timestamp": fake.date_time_this_year()
            }
            transactions.append(transaction)
    return transactions


def generate_fake_logs(count=10000):
    logs = []
    for _ in range(count):
        log = {
            "timestamp": fake.date_time_this_year(),
            "level": fake.random_element(elements=["INFO", "WARNING", "ERROR"]),
            "message": fake.sentence(),
            "context": {
                "user_id": fake.uuid4(),
                "ip_address": fake.ipv4()
            }
        }
        logs.append(log)
    return logs


def generate_fake_analytics(count=10000):
    analytics = []
    for _ in range(count):
        analytic = {
            "timestamp": fake.date_time_this_year(),
            "metric": fake.random_element(elements=["page_views", "clicks", "signups"]),
            "value": fake.random_int(min=1, max=1000),
            "user_id": fake.uuid4()
        }
        analytics.append(analytic)
    return analytics


if __name__ == "__main__":
    # Drop existing collections
    db.users.drop()
    db.accounts.drop()
    db.transactions.drop()
    db.logs.drop()
    db.analytics.drop()
    print("Existing collections dropped.")

    # Generate and insert users
    users = generate_fake_users()
    db.users.insert_many(users)
    print("Users generated and inserted into the database.")

    # Generate and insert accounts
    print("Generating accounts...")
    accounts = generate_fake_accounts(users)
    db.accounts.insert_many(accounts)
    print("Accounts generated and inserted into the database.")

    # Generate and insert transactions
    print("Generating transactions...")
    transactions = generate_fake_transactions(accounts)
    db.transactions.insert_many(transactions)
    print("Transactions generated and inserted into the database.")

    # Generate and insert logs
    print("Generating logs...")
    logs = generate_fake_logs()
    db.logs.insert_many(logs)
    print("Logs generated and inserted into the database.")

    # Generate and insert analytics
    print("Generating analytics...")
    analytics = generate_fake_analytics()
    db.analytics.insert_many(analytics)
    print("Analytics generated and inserted into the database.")
