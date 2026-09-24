from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import Any, List, Optional, Generic, TypeVar, Type
from app.utils.ibase_repo import IBaseRepo

T = TypeVar("T")

class BaseRepo(IBaseRepo[T]):
    def __init__(self, db_session: AsyncSession, model: Type[T]):
        self.db_session = db_session
        self.model = model

    async def create(self, item: T) -> T:
        try:
            self.db_session.add(item)
            await self.db_session.commit()
            await self.db_session.refresh(item)
            return item
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def update(self, id: Any, item_data: Any) -> Optional[T]:
        try:
            db_item = await self.get_by_id(id)
            if not db_item:
                return None
            
            # item_data could be a dict or a Pydantic model
            update_data = item_data if isinstance(item_data, dict) else item_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(db_item, key, value)
                
            await self.db_session.commit()
            await self.db_session.refresh(db_item)
            return db_item
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def delete(self, id: Any) -> bool:
        try:
            db_item = await self.get_by_id(id)
            if db_item:
                await self.db_session.delete(db_item)
                await self.db_session.commit()
                return True
            return False
        except Exception as e:
            await self.db_session.rollback()
            raise e

    async def get_all(self) -> List[T]:
        try:
            result = await self.db_session.execute(select(self.model))
            return result.scalars().all()
        except Exception as e:
            raise e

    async def get_by_id(self, id: Any) -> Optional[T]:
        try:
            result = await self.db_session.execute(select(self.model).filter(self.model.id == id))
            return result.scalar_one_or_none()
        except Exception as e:
            raise e
