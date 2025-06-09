from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `uuid` VARCHAR(36) NOT NULL UNIQUE,
    `password_hash` VARCHAR(128),
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4 COMMENT='The User model';
CREATE TABLE IF NOT EXISTS `userbind` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `bind_type` VARCHAR(10) NOT NULL COMMENT 'QQ: qq\nDivingFish: divingfish\nLuoxue: luoxue',
    `bind_content` VARCHAR(255) NOT NULL,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL,
    UNIQUE KEY `uid_userbind_user_id_20591f` (`user_id`, `bind_type`, `bind_content`),
    CONSTRAINT `fk_userbind_user_3f9d28cf` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用户绑定模型';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
