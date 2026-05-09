import uuid
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user import RefreshToken, User


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_user_by_email(self, email: str) -> User | None:
        result = await self.db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: uuid.UUID) -> User | None:
        result = await self.db.execute(
            select(User).where(User.id == user_id)
        )
        return result.scalar_one_or_none()

    async def create_user(self, email: str, hashed_password: str) -> User:
        user = User(
            email=email,
            hashed_password=hashed_password,
        )

        self.db.add(user)

        await self.db.commit()
        await self.db.refresh(user)

        return user

    async def create_refresh_token(
        self,
        user_id: uuid.UUID,
        token_hash: str,
        expires_at: datetime,
    ) -> RefreshToken:
        refresh_token = RefreshToken(
            user_id=user_id,
            token_hash=token_hash,
            expires_at=expires_at,
        )

        self.db.add(refresh_token)

        await self.db.commit()
        await self.db.refresh(refresh_token)

        return refresh_token

    async def get_refresh_token_by_hash(
        self,
        token_hash: str,
    ) -> RefreshToken | None:
        result = await self.db.execute(
            select(RefreshToken).where(
                RefreshToken.token_hash == token_hash
            )
        )
        return result.scalar_one_or_none()

    async def revoke_refresh_token_by_hash(
        self,
        token_hash: str,
    ) -> None:
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.token_hash == token_hash)
            .values(revoked=True)
        )

        await self.db.commit()

    async def revoke_all_user_tokens(
        self,
        user_id: uuid.UUID,
    ) -> None:
        await self.db.execute(
            update(RefreshToken)
            .where(
                RefreshToken.user_id == user_id,
                RefreshToken.revoked.is_(False),
            )
            .values(revoked=True)
        )

        await self.db.commit()

    async def rotate_refresh_token(
        self,
        old_token_hash: str,
        user_id: uuid.UUID,
        new_token_hash: str,
        expires_at: datetime,
    ) -> None:
        async with self.db.begin():
            await self.db.execute(
                update(RefreshToken)
                .where(
                    RefreshToken.token_hash == old_token_hash,
                    RefreshToken.revoked.is_(False),
                )
                .values(revoked=True)
            )

            new_refresh_token = RefreshToken(
                user_id=user_id,
                token_hash=new_token_hash,
                expires_at=expires_at,
            )

            self.db.add(new_refresh_token)
        await self.db.execute(
            update(RefreshToken)
            .where(RefreshToken.user_id == user_id, RefreshToken.revoked == False)
            .values(revoked=True)
        )