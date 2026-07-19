import pytest
from sqlalchemy.orm import Session

from db_models.accounts_transaction import AccountTransactionTemplate
from utils.data_generator import DataGenerator


def test_insufficient_balance_does_not_change_accounts(db_session: Session):

    stan = AccountTransactionTemplate(user=f"Stan_{DataGenerator.generate_random_int(1000000)}", balance=100)
    bob = AccountTransactionTemplate(user=f"Bob_{DataGenerator.generate_random_int(1000000)}", balance=500)


    db_session.add_all([stan, bob])

    db_session.commit()

    def transfer_money(session, from_account, to_account, amount):

        from_account = session.query(AccountTransactionTemplate).filter_by(user=from_account).one()
        to_account = session.query(AccountTransactionTemplate).filter_by(user=to_account).one()


        if from_account.balance < amount:
            raise ValueError("Недостаточно средств на счете")


        from_account.balance -= amount
        to_account.balance += amount


        session.commit()


    assert stan.balance == 100
    assert bob.balance == 500

    with pytest.raises(ValueError):
        transfer_money(db_session, from_account=stan.user, to_account=bob.user, amount=200)

    db_session.rollback()
    assert stan.balance == 100
    assert bob.balance == 500

    db_session.delete(stan)
    db_session.delete(bob)
    db_session.commit()
