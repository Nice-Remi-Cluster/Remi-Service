# How To Use

```shell
# 运行应用
uvicorn run:app --reload
```

## 数据库迁移 (Aerich)

本项目使用Aerich进行数据库迁移管理，以下是常用操作：

### 创建新的迁移

当您修改了模型后，使用以下命令创建新的迁移文件：

```powershell
aerich migrate --name <migration_name>
```

例如：`aerich migrate --name add_email_field`

### 应用迁移

将未应用的迁移应用到数据库：

```powershell
aerich upgrade
```

### 回滚迁移

回滚到之前的迁移版本：

```powershell
aerich downgrade
```

### 查看迁移历史

```powershell
aerich history
```
