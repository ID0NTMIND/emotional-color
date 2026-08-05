"""
Test script for business logic demonstration
Run inside container: docker compose exec app python src/test_services.py
"""

from sqlmodel import Session, select
from src.db.database import engine
from src.db.models import User
from src.services.user_service import (
    create_user, get_user_by_username, top_up_balance, deduct_balance, get_user_history
)
from decimal import Decimal


def main():
    with Session(engine) as session:
        print("=== 1. Initial data check ===")
        demo = get_user_by_username(session, "demo")
        if demo and demo.balance is not None:
            print(f"Demo user balance: {demo.balance.amount}")
        else:
            print("ERROR: demo user or balance missing")

        admin = get_user_by_username(session, "admin")
        if admin and admin.balance is not None:
            print(f"Admin user balance: {admin.balance.amount}")
        else:
            print("ERROR: admin user or balance missing")

        print("\n=== 2. Top up demo balance by 50 ===")
        if demo and demo.balance is not None:
            top_up_balance(session, demo, Decimal("50"))
            print(f"Balance after top up: {demo.balance.amount}")

        print("\n=== 3. Deduct 30 (success expected) ===")
        if demo and demo.balance is not None:
            success = deduct_balance(session, demo, Decimal("30"))
            print(
                f"Deduct 30 success: {success}, balance: {demo.balance.amount}")

        print("\n=== 4. Deduct 9999 (failure expected — insufficient funds) ===")
        if demo and demo.balance is not None:
            success = deduct_balance(session, demo, Decimal("9999"))
            print(
                f"Deduct 9999 success: {success}, balance: {demo.balance.amount}")

        print("\n=== 5. Create new user testuser ===")
        existing = session.exec(select(User).where(
            User.username == "testuser")).first()
        if existing:
            if existing.balance is not None:
                print(
                    f"User testuser already exists with balance: {existing.balance.amount}")
            else:
                print("User testuser exists but has no balance record")
        else:
            new_user = create_user(session, "testuser",
                                   "test_hash", initial_balance=Decimal("25"))
            if new_user.balance is not None:
                print(
                    f"Created user: {new_user.username}, balance: {new_user.balance.amount}")
            else:
                print(
                    f"Created user: {new_user.username}, but balance creation failed")

        print("\n=== 6. Transaction history for demo (last 5) ===")
        if demo:
            transactions, tasks = get_user_history(session, demo, limit=5)
            for t in transactions:
                print(
                    f"  {t.timestamp} | {t.transaction_type.value} | {t.amount}")
            if not transactions:
                print("  (no transactions)")

        print("\n=== 7. ML task history for demo (last 5) ===")
        if demo:
            for task in tasks:
                print(
                    f"  {task.created_at} | {task.status} | input: {task.input_data[:30]}...")
            if not tasks:
                print("  (no ML tasks yet)")

        print("\n=== All tests completed ===")


if __name__ == "__main__":
    main()
