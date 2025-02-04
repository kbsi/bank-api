from faker import Faker
from app.services.mongo import get_user_collection, get_account_collection

fake = Faker()

def generate_fake_users(count=100):
    users = []
    for _ in range(count):
        users.append({
            "email": fake.email(),
            "password_hash": fake.password(),
            "roles": ["client"],
            "accounts": [],
            "created_at": fake.date_time_this_year()
        })
    return users

def generate_fake_accounts(users):
    accounts = []
    for user in users:
        account_count = fake.random_int(min=1, max=3)
        for _ in range(account_count):
            accounts.append({
                "user_id": user["_id"],
                "account_number": fake.iban(),
                "balance": fake.random_int(min=100, max=10000),
                "currency": fake.random_element(elements=("EUR", "USD")),
                "transactions": [],
                "status": "active",
                "created_at": fake.date_time_this_year()
            })
    return accounts

if __name__ == "__main__":
    print("Génération des utilisateurs...")
    users = generate_fake_users()
    get_user_collection().insert_many(users)

    print("Génération des comptes...")
    accounts = generate_fake_accounts(users)
    get_account_collection().insert_many(accounts)

    print("Données générées avec succès.")
