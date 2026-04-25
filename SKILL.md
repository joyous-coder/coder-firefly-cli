---
name: "coder-firefly-cli"
description: "Firefly III CLI - 个人财务管理命令行工具，通过命令行连接和操作 Firefly III 实例"
version: "1.0.0"
author: "coder"
---

# coder-firefly-cli

Firefly III 个人财务管理软件的命令行工具，支持账户、交易、预算、分类、标签、账单、储蓄罐等管理操作。

## 安装

```bash
pip install coder-firefly-cli
```

## 前提条件

- Python 3.10+
- 运行中的 Firefly III 实例
- Personal Access Token (PAT)

## 配置

### 环境变量（推荐）

```bash
export FIREFLY_BASE_URL="https://firefly.example.com"
export FIREFLY_PAT="your-personal-access-token"
```

### 命令行参数

```bash
coder-firefly-cli --base-url https://firefly.example.com --pat your-token
```

## 命令组

| 命令组 | 说明 | 对应 API |
|--------|------|----------|
| `accounts` | 账户管理 | `/api/v1/accounts` |
| `transactions` | 交易管理 | `/api/v1/transactions` |
| `budgets` | 预算管理 | `/api/v1/budgets` |
| `categories` | 分类管理 | `/api/v1/categories` |
| `tags` | 标签管理 | `/api/v1/tags` |
| `bills` | 账单管理 | `/api/v1/bills` |
| `piggy-banks` | 储蓄罐管理 | `/api/v1/piggy-banks` |
| `insights` | 财务洞察报告 | `/api/v1/insight/*` |
| `search` | 搜索 | `/api/v1/search/*` |
| `info` | 系统信息 | `/api/v1/about` |

## 使用示例

### 账户管理

```bash
# 列出所有账户
coder-firefly-cli --json accounts list

# 按类型筛选账户
coder-firefly-cli --json accounts list --type asset

# 获取账户详情
coder-firefly-cli --json accounts get --id 123

# 创建账户
coder-firefly-cli --json accounts create --name "现金" --type asset --currency-code CNY

# 删除账户
coder-firefly-cli accounts delete --id 123
```

### 交易管理

```bash
# 列出交易
coder-firefly-cli --json transactions list --limit 10

# 创建支出交易
coder-firefly-cli --json transactions create \
  --description "超市购物" \
  --amount 50.00 \
  --source-account 1 \
  --category "餐饮"

# 创建转账
coder-firefly-cli --json transactions create \
  --description "转账" \
  --amount 100.00 \
  --source-account 1 \
  --destination-account 2 \
  --type transfer

# 获取交易详情
coder-firefly-cli --json transactions get --id 456

# 删除交易
coder-firefly-cli transactions delete --id 456
```

### 预算管理

```bash
# 列出预算
coder-firefly-cli --json budgets list

# 创建预算
coder-firefly-cli budgets create --name "餐饮预算"

# 设置预算限额
coder-firefly-cli budgets limit-create --budget-id 1 --amount 2000 --start 2024-01-01 --end 2024-01-31
```

### 财务洞察

```bash
# 支出报告
coder-firefly-cli --json insights expense --start 2024-01-01 --end 2024-01-31

# 收入报告
coder-firefly-cli --json insights income --start 2024-01-01 --end 2024-01-31
```

### 搜索

```bash
# 搜索交易
coder-firefly-cli --json search transactions --query "超市"
```

### 系统信息

```bash
# 系统信息
coder-firefly-cli --json info about

# 连接状态
coder-firefly-cli info status
```

## Agent 使用指南

### 基本用法

1. **使用 `--json` 获取结构化输出**：所有命令都支持 `--json` 参数
2. **先调用 `info status` 检查连接**：执行操作前确认 Firefly III 连接正常
3. **使用 `--help` 查看命令详情**：每个命令都有详细帮助信息

### 常见工作流

#### 查看账户余额

```bash
# 1. 检查连接
coder-firefly-cli info status

# 2. 列出资产账户
coder-firefly-cli --json accounts list --type asset

# 3. 查看账户详情（获取余额）
coder-firefly-cli --json accounts get --id <account_id>
```

#### 记录支出

```bash
# 1. 查找支出账户
coder-firefly-cli --json accounts list --type expense

# 2. 创建交易
coder-firefly-cli --json transactions create \
  --description "午餐" \
  --amount 15.50 \
  --source-account <asset_account_id> \
  --destination-account <expense_account_id>
```

#### 月度报告

```bash
# 1. 支出报告
coder-firefly-cli --json insights expense --start 2024-01-01 --end 2024-01-31

# 2. 收入报告
coder-firefly-cli --json insights income --start 2024-01-01 --end 2024-01-31
```

### 错误处理

常见错误及解决方案：

1. **连接失败**：检查 FIREFLY_BASE_URL 是否正确
2. **认证失败**：检查 FIREFLY_PAT 是否有效
3. **资源未找到**：检查 ID 是否正确
4. **参数错误**：检查必需参数是否提供

### 最佳实践

1. **使用环境变量存储凭证**：避免在命令行暴露 PAT
2. **使用 `--json` 便于脚本处理**：方便解析和处理输出
3. **操作前先查询**：避免误操作
4. **删除操作需要确认**：删除命令会提示确认

## 故障排除

### 连接问题

```
错误: 无法连接到 Firefly III 实例
```

- 检查 Firefly III 实例是否运行
- 检查网络连接
- 检查 base URL 是否正确

### 认证问题

```
错误: 认证失败: Personal Access Token 无效
```

- 检查 PAT 是否正确
- 在 Firefly III 的 选项 > 个人资料 > OAuth 中生成新的 PAT
- 确保 PAT 未过期

## 许可证

MIT License
