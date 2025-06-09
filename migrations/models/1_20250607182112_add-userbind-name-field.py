from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `userbind` ADD `bind_name` VARCHAR(30);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE `userbind` DROP COLUMN `bind_name`;"""
