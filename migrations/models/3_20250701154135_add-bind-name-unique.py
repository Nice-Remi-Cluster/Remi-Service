from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `userbind` ADD UNIQUE INDEX `uid_userbind_user_id_ea9e73` (`user_id`, `bind_type`, `bind_name`);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `userbind` DROP INDEX `uid_userbind_user_id_ea9e73`;"""
