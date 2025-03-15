from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import select, desc, asc
from fastapi import Query
from fastapi_app.database import get_db
from fastapi_app.models import Transaction, User
from fastapi_app.schemas import TransactionCreate, TransactionResponse
from fastapi_app.dependencies import get_current_user

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.post("/", response_model=TransactionResponse)
async def create_transaction(
    transaction_data: TransactionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    if transaction_data.transaction_type not in ["income", "expense"]:
        raise HTTPException(status_code=400, detail="Invalid transaction type")

    new_transaction = Transaction(
        amount=transaction_data.amount,
        transaction_type=transaction_data.transaction_type,
        category=transaction_data.category,
        user_id=current_user.id
    )
    db.add(new_transaction)

    if transaction_data.transaction_type == "income":
        current_user.balance += transaction_data.amount
    elif transaction_data.transaction_type == "expense":
        if current_user.balance < transaction_data.amount:
            raise HTTPException(status_code=400, detail="Insufficient funds")
        current_user.balance -= transaction_data.amount

    await db.commit()
    await db.refresh(new_transaction)
    return new_transaction


@router.get("/", response_model=list[TransactionResponse])
async def get_transactions(
        db: AsyncSession = Depends(get_db),
        current_user: User = Depends(get_current_user),
        category: str = Query(None, description="Фільтр за категорією"),
        transaction_type: str = Query(None, description="Фільтр за типом (income/expense)"),
        sort_by: str = Query("created_at", description="Сортування за полем (created_at/amount)"),
        order: str = Query("desc", description="Порядок сортування (asc/desc)")
):
    query = select(Transaction).where(Transaction.user_id == current_user.id)

    if category:
        query = query.where(Transaction.category == category)
    if transaction_type:
        query = query.where(Transaction.transaction_type == transaction_type)

    if sort_by not in ["amount", "created_at"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")

    order_by_column = getattr(Transaction, sort_by)
    if order == "desc":
        order_by_column = desc(order_by_column)
    else:
        order_by_column = asc(order_by_column)

    query = query.order_by(order_by_column)

    result = await db.execute(query)
    return result.scalars().all()


@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.delete("/{transaction_id}")
async def delete_transaction(transaction_id: int, db: AsyncSession = Depends(get_db)):
    transaction = await db.get(Transaction, transaction_id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    await db.delete(transaction)
    await db.commit()
    return {"message": "Transaction deleted successfully"}
