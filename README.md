# coder-firefly-cli

Firefly III CLI - 个人财务管理命令行工具

## 安装

```bash
pip install -e .
```

## 前提条件

- Python 3.10+
- 运行中的 Firefly III 实例
- Personal Access Token (PAT)

## 配置

### 环境变量（推荐）

```bash
export FIREFLY_BASE_URL="https://firefly.yourdomain.com"
export FIREFLY_PAT="your-personal-access-token"
```

### 命令行参数

```bash
coder-firefly-cli --base-url https://firefly.yourdomain.com --pat your-token accounts list
```

## 使用方法

### 账户管理

```bash
# 列出账户
coder-firefly-cli accounts list
coder-firefly-cli accounts list --type asset

# 获取账户详情
coder-firefly-cli accounts get --id 123

# 创建账户
coder-firefly-cli accounts create --name "现金" --type asset --currency-code CNY

# 更新账户
coder-firefly-cli accounts update --id 123 --name "新名称"

# 删除账户
coder-firefly-cli accounts delete --id 123
```

### 交易管理

```bash
# 列出交易
coder-firefly-cli transactions list
coder-firefly-cli transactions list --limit 10 --start 2024-01-01

# 创建支出
coder-firefly-cli transactions create --description "超市购物" --amount 100.00 --source-account 1

# 创建转账
coder-firefly-cli transactions create --description "转账" --amount 500.00 --source-account 1 --destination-account 2 --type transfer

# 获取交易详情
coder-firefly-cli transactions get --id 456

# 删除交易
coder-firefly-cli transactions delete --id 456
```

### 预算管理

```bash
# 列出预算
coder-firefly-cli budgets list

# 创建预算
coder-firefly-cli budgets create --name "餐饮预算"

# 设置预算限额
coder-firefly-cli budgets limit-create --budget-id 1 --amount 2000 --start 2024-01-01 --end 2024-01-31
```

### 分类管理

```bash
# 列出分类
coder-firefly-cli categories list

# 创建分类
coder-firefly-cli categories create --name "餐饮"
```

### 标签管理

```bash
# 列出标签
coder-firefly-cli tags list

# 创建标签
coder-firefly-cli tags create --tag "重要"
```

### 账单管理

```bash
# 列出账单
coder-firefly-cli bills list

# 创建账单
coder-firefly-cli bills create --name "房租" --amount-min 3000 --amount-max 3000 --date 2024-01-01
```

### 储蓄罐管理

```bash
# 列出储蓄罐
coder-firefly-cli piggy-banks list

# 创建储蓄罐
coder-firefly-cli piggy-banks create --name "旅行基金" --account-id 1 --target-amount 10000
```

### 搜索

```bash
# 搜索交易
coder-firefly-cli search transactions --query "超市"
```

### 洞察报告

```bash
# 支出洞察
coder-firefly-cli insights expense --start 2024-01-01 --end 2024-01-31

# 收入洞察
coder-firefly-cli insights income --start 2024-01-01 --end 2024-01-31
```

### 系统信息

```bash
# 获取系统信息
coder-firefly-cli info about

# 检查连接状态
coder-firefly-cli info status
```

## JSON 输出

所有命令都支持 `--json` 参数以结构化格式输出：

```bash
coder-firefly-cli --json accounts list
```

## 故障排除

### 连接失败

```
错误: 无法连接到 Firefly III 实例
```

检查：
1. Firefly III 实例是否正在运行
2. 基础 URL 是否正确
3. 网络连接是否正常

### 认证失败

```
错误: 认证失败: Personal Access Token 无效
```

检查：
1. PAT 是否正确
2. PAT 是否已过期
3. 在 Firefly III 的 选项 > 个人资料 > OAuth 中生成新的 PAT

## 开发

```bash
# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black src/
```

## 许可证

MIT License
