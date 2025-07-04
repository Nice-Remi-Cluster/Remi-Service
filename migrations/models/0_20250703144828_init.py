from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS `user` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `uuid` VARCHAR(36) NOT NULL UNIQUE,
    `password_hash` VARCHAR(128),
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6)
) CHARACTER SET utf8mb4 COMMENT='The User model';
CREATE TABLE IF NOT EXISTS `userbind` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `bind_type` VARCHAR(10) NOT NULL COMMENT 'QQ: qq\nDivingFish: divingfish\nLuoxue: luoxue\nMaimaiCN: maimai_cn',
    `bind_name` VARCHAR(30) NOT NULL,
    `bind_content` VARCHAR(255) NOT NULL,
    `is_default` BOOL NOT NULL DEFAULT 0,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `user_id` INT NOT NULL,
    UNIQUE KEY `uid_userbind_bind_ty_1fc935` (`bind_type`, `bind_content`),
    UNIQUE KEY `uid_userbind_user_id_ea9e73` (`user_id`, `bind_type`, `bind_name`),
    CONSTRAINT `fk_userbind_user_3f9d28cf` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='用户绑定模型';
CREATE TABLE IF NOT EXISTS `maimaicnbind` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `divingfish_bind_id` INT,
    `luoxue_bind_id` INT,
    `mai_bind_id` INT NOT NULL,
    UNIQUE KEY `uid_maimaicnbin_mai_bin_939063` (`mai_bind_id`, `luoxue_bind_id`, `divingfish_bind_id`),
    CONSTRAINT `fk_maimaicn_userbind_6b6103a5` FOREIGN KEY (`divingfish_bind_id`) REFERENCES `userbind` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_maimaicn_userbind_1fde5d93` FOREIGN KEY (`luoxue_bind_id`) REFERENCES `userbind` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_maimaicn_userbind_5b1488bd` FOREIGN KEY (`mai_bind_id`) REFERENCES `userbind` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='MaiMai查分器绑定模型';
CREATE TABLE IF NOT EXISTS `maimaicurrent` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `created_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6),
    `updated_at` DATETIME(6) NOT NULL DEFAULT CURRENT_TIMESTAMP(6) ON UPDATE CURRENT_TIMESTAMP(6),
    `mai_bind_id` INT NOT NULL,
    `user_id` INT NOT NULL,
    UNIQUE KEY `uid_maimaicurre_user_id_59473a` (`user_id`, `mai_bind_id`),
    CONSTRAINT `fk_maimaicu_maimaicn_fd01b032` FOREIGN KEY (`mai_bind_id`) REFERENCES `maimaicnbind` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_maimaicu_user_e295efdf` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`) ON DELETE CASCADE
) CHARACTER SET utf8mb4 COMMENT='maimai当前使用的maimai账号';
CREATE TABLE IF NOT EXISTS `aerich` (
    `id` INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    `version` VARCHAR(255) NOT NULL,
    `app` VARCHAR(100) NOT NULL,
    `content` JSON NOT NULL
) CHARACTER SET utf8mb4;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
