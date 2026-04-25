---
name: "coder-firefly-cli"
description: "Firefly III CLI - 个人财务管理命令行工具，通过命令行连接和操作 Firefly III 实例"
version: "1.0.0"
author: "coder"
---

# coder-firefly-cli

Firefly III 个人财务管理软件的命令行工具，支持账户、交易、预算、分类、标签、账单、储蓄罐等管理操作。

## 安装

### 方式一：通过 PyPI 安装（推荐）

```bash
pip install coder-firefly-cli
```

### 方式二：通过 GitHub 安装

```bash
pip install git+https://github.com/joyous-coder/coder-firefly-cli.git
```

### 方式三：本地开发安装

```bash
git clone https://github.com/joyous-coder/coder-firefly-cli.git
cd coder-firefly-cli
pip install -e .
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

## 全局选项

| 选项 | 说明 |
|------|------|
| `--json` | 以 JSON 格式输出结构化数据 |
| `--base-url` | Firefly III 实例地址 |
| `--pat` | Personal Access Token |
| `--help` | 查看帮助信息 |

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

## 详细命令参考

### accounts - 账户管理

```bash
# 列出所有账户
coder-firefly-cli --json accounts list

# 按类型筛选（asset/expense/revenue/liability）
coder-firefly-cli --json accounts list --type asset

# 分页查询
coder-firefly-cli --json accounts list --limit 10 --page 1

# 获取账户详情
coder-firefly-cli --json accounts get --id 123

# 创建资产账户
coder-firefly-cli --json accounts create \
  --name "现金" \
  --type asset \
  --currency-code CNY \
  --opening-balance 1000

# 创建支出账户
coder-firefly-cli --json accounts create \
  --name "餐饮" \
  --type expense

# 更新账户
coder-firefly-cli --json accounts update --id 123 --name "新名称"

# 删除账户（会提示确认）
coder-firefly-cli accounts delete --id 123
```

### transactions - 交易管理

```bash
# 列出最近交易
coder-firefly-cli --json transactions list

# 分页和日期范围
coder-firefly-cli --json transactions list \
  --limit 20 \
  --start 2024-01-01 \
  --end 2024-01-31

# 按类型筛选（withdrawal/deposit/transfer）
coder-firefly-cli --json transactions list --type withdrawal

# 按账户筛选
coder-firefly-cli --json transactions list --source-account 1

# 创建支出交易
coder-firefly-cli --json transactions create \
  --description "超市购物" \
  --amount 150.00 \
  --source-account 1 \
  --category "生活"

# 创建转账
coder-firefly-cli --json transactions create \
  --description "转账到支付宝" \
  --amount 500.00 \
  --source-account 1 \
  --destination-account 2 \
  --type transfer

# 创建带标签的交易
coder-firefly-cli --json transactions create \
  --description "午餐" \
  --amount 35.00 \
  --source-account 1 \
  --tags "餐饮,工作日"

# 获取交易详情
coder-firefly-cli --json transactions get --id 456

# 更新交易
coder-firefly-cli --json transactions update \
  --id 456 \
  --description "更新后的描述" \
  --amount 160.00

# 删除交易（会提示确认）
coder-firefly-cli transactions delete --id 456
```

### budgets - 预算管理

```bash
# 列出所有预算
coder-firefly-cli --json budgets list

# 创建预算
coder-firefly-cli --json budgets create \
  --name "餐饮预算" \
  --notes "每月餐饮支出上限"

# 获取预算详情
coder-firefly-cli --json budgets get --id 1

# 更新预算
coder-firefly-cli --json budgets update --id 1 --name "新餐饮预算"

# 删除预算
coder-firefly-cli budgets delete --id 1

# 查看预算限额
coder-firefly-cli --json budgets limits --budget-id 1

# 创建预算限额
coder-firefly-cli --json budgets limit-create \
  --budget-id 1 \
  --amount 2000 \
  --start 2024-01-01 \
  --end 2024-01-31 \
  --currency-code CNY

# 更新预算限额
coder-firefly-cli --json budgets limit-update --id 10 --amount 2500

# 删除预算限额
coder-firefly-cli budgets limit-delete --id 10
```

### categories - 分类管理

```bash
# 列出所有分类
coder-firefly-cli --json categories list

# 创建分类
coder-firefly-cli --json categories create --name "餐饮" --notes "日常餐饮"

# 获取分类详情
coder-firefly-cli --json categories get --id 1

# 更新分类
coder-firefly-cli --json categories update --id 1 --name "日常餐饮"

# 删除分类
coder-firefly-cli categories delete --id 1
```

### tags - 标签管理

```bash
# 列出所有标签
coder-firefly-cli --json tags list

# 创建标签
coder-firefly-cli --json tags create --tag "重要" --description "重要支出标记"

# 获取标签详情
coder-firefly-cli --json tags get --id "重要"

# 更新标签
coder-firefly-cli --json tags update --id "重要" --description "更新后的描述"

# 删除标签
coder-firefly-cli tags delete --id "重要"
```

### bills - 账单管理

```bash
# 列出所有账单
coder-firefly-cli --json bills list

# 创建账单
coder-firefly-cli --json bills create \
  --name "房租" \
  --amount-min 3000 \
  --amount-max 3000 \
  --date 2024-01-01 \
  --repeat-freq monthly

# 获取账单详情
coder-firefly-cli --json bills get --id 1

# 更新账单
coder-firefly-cli --json bills update --id 1 --amount-min 3200

# 删除账单
coder-firefly-cli bills delete --id 1
```

### piggy-banks - 储蓄罐管理

```bash
# 列出所有储蓄罐
coder-firefly-cli --json piggy-banks list

# 创建储蓄罐
coder-firefly-cli --json piggy-banks create \
  --name "旅行基金" \
  --account-id 1 \
  --target-amount 10000 \
  --current-amount 2000 \
  --target-date 2024-12-31

# 获取储蓄罐详情
coder-firefly-cli --json piggy-banks get --id 1

# 更新储蓄罐
coder-firefly-cli --json piggy-banks update \
  --id 1 \
  --current-amount 2500

# 删除储蓄罐
coder-firefly-cli piggy-banks delete --id 1
```

### insights - 财务洞察

```bash
# 支出洞察
coder-firefly-cli --json insights expense \
  --start 2024-01-01 \
  --end 2024-01-31

# 收入洞察
coder-firefly-cli --json insights income \
  --start 2024-01-01 \
  --end 2024-01-31

# 转账洞察
coder-firefly-cli --json insights transfer \
  --start 2024-01-01 \
  --end 2024-01-31

# 按账户筛选洞察
coder-firefly-cli --json insights expense \
  --start 2024-01-01 \
  --end 2024-01-31 \
  --accounts "1,2"

# 按分类筛选洞察
coder-firefly-cli --json insights expense \
  --start 2024-01-01 \
  --end 2024-01-31 \
  --categories "3,4"
```

### search - 搜索

```bash
# 搜索交易
coder-firefly-cli --json search transactions \
  --query "超市" \
  --limit 20

# 分页搜索
coder-firefly-cli --json search transactions \
  --query "餐饮" \
  --limit 10 \
  --page 2
```

### info - 系统信息

```bash
# 获取系统信息
coder-firefly-cli --json info about

# 检查连接状态
coder-firefly-cli info status
```

## Agent 使用指南

### 基本用法

1. **使用 `--json` 获取结构化输出**：所有命令都支持 `--json` 参数，返回标准 JSON 格式
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

# 3. 搜索特定交易
coder-firefly-cli --json search transactions --query "超市" --start 2024-01-01 --end 2024-01-31
```

#### 预算管理

```bash
# 1. 创建预算
coder-firefly-cli --json budgets create --name "餐饮预算"

# 2. 设置预算限额
coder-firefly-cli --json budgets limit-create \
  --budget-id 1 \
  --amount 2000 \
  --start 2024-01-01 \
  --end 2024-01-31

# 3. 查看预算使用情况
coder-firefly-cli --json budgets limits --budget-id 1
```

### 错误处理

常见错误及解决方案：

1. **连接失败**：检查 FIREFLY_BASE_URL 是否正确，网络是否连通
2. **认证失败**：检查 FIREFLY_PAT 是否有效，是否已过期
3. **资源未找到**：检查 ID 是否正确，资源是否存在
4. **参数错误**：检查必需参数是否提供，参数格式是否正确
5. **请求超时**：检查网络连接，或增加超时时间

### 最佳实践

1. **使用环境变量存储凭证**：避免在命令行暴露 PAT
2. **使用 `--json` 便于脚本处理**：方便解析和处理输出，支持管道和重定向
3. **操作前先查询**：避免误操作，特别是删除操作
4. **删除操作需要确认**：删除命令会提示确认，防止误删
5. **使用分页处理大量数据**：避免一次性加载过多数据
6. **使用标签和分类组织交易**：便于后续搜索和统计

## 故障排除

### 连接问题

```
错误: 无法连接到 Firefly III 实例
```

- 检查 Firefly III 实例是否运行
- 检查网络连接
- 检查 base URL 是否正确（注意结尾不要带斜杠）

### 认证问题

```
错误: 认证失败: Personal Access Token 无效
```

- 检查 PAT 是否正确
- 在 Firefly III 的 选项 > 个人资料 > OAuth 中生成新的 PAT
- 确保 PAT 未过期

### 数据格式问题

```
错误: 请求参数错误
```

- 检查金额是否为字符串格式（如 "100.00"）
- 检查日期格式是否为 YYYY-MM-DD
- 检查必需参数是否都已提供

## 许可证

MIT License
