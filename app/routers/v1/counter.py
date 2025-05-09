from fastapi import APIRouter, Depends, status

from app.dependencies import get_database
from app.schemas.counter import Counter, CounterRead

router = APIRouter(prefix="/counter", tags=["Counter Service V1"])


# @router.get("", response_model=CounterRead)
# async def get_counter():
#     res = Resources()
#     process_counter(res)
#     return Counter(counter=res.counter, total_calls=res.total_calls)


@router.post(
    "/up",
    response_model=CounterRead,
    status_code=status.HTTP_201_CREATED
)
def increment_counter(counter: Counter, db=Depends(get_database)):
    counter_data = counter.model_dump()
    new_counter = db.test_collection.insert_one(counter_data)
    return CounterRead(id=str(new_counter.inserted_id), **counter_data)


# @router.post("/down", response_model=Counter)
# async def decrement_counter():
#     res = Resources()
#     process_counter(res, decrement)
#     return Counter(counter=res.counter, total_calls=res.total_calls)
