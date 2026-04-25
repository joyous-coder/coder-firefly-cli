# coder-firefly-cli

Firefly III CLI - 个人财务管理命令行工具

通过命令行连接和管理 Firefly III 个人财务管理系统，支持账户、交易、预算、分类、标签、账单、储蓄罐等全面管理。

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

## 安装为 Skill（AI Agent 使用）

如果你需要将本工具作为 AI Agent 的 Skill 使用，可以将 `SKILL.md` 文件配置到 AI 系统中。

### OhMyOpenCode / CLI-Anything 环境

将本仓库作为 Skill 添加到配置中：

```bash
# 克隆仓库
git clone https://github.com/joyous-coder/coder-firefly-cli.git

# 在 skill 配置中引用 SKILL.md 文件路径
# 或直接复制 SKILL.md 内容到 skill 配置
```

### 通用 AI 工具集成

1. 获取 `SKILL.md` 文件内容
2. 在 AI 系统中配置为可用工具/Skill
3. 配置环境变量 `FIREFLY_BASE_URL` 和 `FIREFLY_PAT`
4. AI 将自动识别并使用 `coder-firefly-cli` 命令

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
| `accounts` | 账户管理（资产、支出、收入、负债） | `/api/v1/accounts` |
| `transactions` | 交易管理（支出、收入、转账） | `/api/v1/transactions` |
| `budgets` | 预算管理（含预算限额） | `/api/v1/budgets` |
| `categories` | 分类管理 | `/api/v1/categories` |
| `tags` | 标签管理 | `/api/v1/tags` |
| `bills` | 账单管理 | `/api/v1/bills` |
| `piggy-banks` | 储蓄罐管理 | `/api/v1/piggy-banks` |
| `insights` | 财务洞察报告（支出/收入/转账分析） | `/api/v1/insight/*` |
| `search` | 搜索交易 | `/api/v1/search/*` |
| `info` | 系统信息 | `/api/v1/about` |

## 详细命令参考

### accounts - 账户管理

```bash
# 列出所有账户
coder-firefly-cli accounts list

# 按类型筛选（asset/expense/revenue/liability）
coder-firefly-cli accounts list --type asset

# 分页查询
coder-firefly-cli accounts list --limit 10 --page 1

# 获取账户详情
coder-firefly-cli accounts get --id 123

# 创建资产账户
coder-firefly-cli accounts create --name "现金" --type asset --currency-code CNY --opening-balance 1000

# 创建支出账户
coder-firefly-cli accounts create --name "餐饮" --type expense

# 更新账户
coder-firefly-cli accounts update --id 123 --name "新名称"

# 删除账户（会提示确认）
coder-firefly-cli accounts delete --id 123
```

### transactions - 交易管理

```bash
# 列出最近交易
coder-firefly-cli transactions list

# 分页和日期范围
coder-firefly-cli transactions list --limit 20 --start 2024-01-01 --end 2024-01-31

# 按类型筛选（withdrawal/deposit/transfer）
coder-firefly-cli transactions list --type withdrawal

# 按账户筛选
coder-firefly-cli transactions list --source-account 1

# 创建支出交易
coder-firefly-cli transactions create --description "超市购物" --amount 150.00 --source-account 1 --category "生活"

# 创建转账
coder-firefly-cli transactions create --description "转账到支付宝" --amount 500.00 --source-account 1 --destination-account 2 --type transfer

# 创建带标签的交易
coder-firefly-cli transactions create --description "午餐" --amount 35.00 --source-account 1 --tags "餐饮,工作日"

# 获取交易详情
coder-firefly-cli transactions get --id 456

# 更新交易
coder-firefly-cli transactions update --id 456 --description "更新后的描述" --amount 160.00

# 删除交易（会提示确认）
coder-firefly-cli transactions delete --id 456
```

### budgets - 预算管理

```bash
# 列出所有预算
coder-firefly-cli budgets list

# 创建预算
coder-firefly-cli budgets create --name "餐饮预算" --notes "每月餐饮支出上限"

# 获取预算详情
coder-firefly-cli budgets get --id 1

# 更新预算
coder-firefly-cli budgets update --id 1 --name "新餐饮预算"

# 删除预算（会提示确认）
coder-firefly-cli budgets delete --id 1

# 查看预算限额
coder-firefly-cli budgets limits --budget-id 1

# 创建预算限额
coder-firefly-cli budgets limit-create --budget-id 1 --amount 2000 --start 2024-01-01 --end 2024-01-31 --currency-code CNY

# 更新预算限额
coder-firefly-cli budgets limit-update --id 10 --amount 2500

# 删除预算限额（会提示确认）
coder-firefly-cli budgets limit-delete --id 10
```

### categories - 分类管理

```bash
# 列出所有分类
coder-firefly-cli categories list

# 创建分类
coder-firefly-cli categories create --name "餐饮" --notes "日常餐饮"

# 获取分类详情
coder-firefly-cli categories get --id 1

# 更新分类
coder-firefly-cli categories update --id 1 --name "日常餐饮"

# 删除分类（会提示确认）
coder-firefly-cli categories delete --id 1
```

### tags - 标签管理

```bash
# 列出所有标签
coder-firefly-cli tags list

# 创建标签
coder-firefly-cli tags create --tag "重要" --description "重要支出标记"

# 获取标签详情
coder-firefly-cli tags get --id "重要"

# 更新标签
coder-firefly-cli tags update --id "重要" --description "更新后的描述"

# 删除标签（会提示确认）
coder-firefly-cli tags delete --id "重要"
```

### bills - 账单管理

```bash
# 列出所有账单
coder-firefly-cli bills list

# 创建账单
coder-firefly-cli bills create --name "房租" --amount-min 3000 --amount-max 3000 --date 2024-01-01 --repeat-freq monthly

# 获取账单详情
coder-firefly-cli bills get --id 1

# 更新账单
coder-firefly-cli bills update --id 1 --amount-min 3200

# 删除账单（会提示确认）
coder-firefly-cli bills delete --id 1
```

### piggy-banks - 储蓄罐管理

```bash
# 列出所有储蓄罐
coder-firefly-cli piggy-banks list

# 创建储蓄罐
coder-firefly-cli piggy-banks create --name "旅行基金" --account-id 1 --target-amount 10000 --current-amount 2000 --target-date 2024-12-31

# 获取储蓄罐详情
coder-firefly-cli piggy-banks get --id 1

# 更新储蓄罐
coder-firefly-cli piggy-banks update --id 1 --current-amount 2500

# 删除储蓄罐（会提示确认）
coder-firefly-cli piggy-banks delete --id 1
```

### insights - 财务洞察

```bash
# 支出洞察
coder-firefly-cli insights expense --start 2024-01-01 --end 2024-01-31

# 收入洞察
coder-firefly-cli insights income --start 2024-01-01 --end 2024-01-31

# 转账洞察
coder-firefly-cli insights transfer --start 2024-01-01 --end 2024-01-31

# 按账户筛选洞察
coder-firefly-cli insights expense --start 2024-01-01 --end 2024-01-31 --accounts "1,2"

# 按分类筛选洞察
coder-firefly-cli insights expense --start 2024-01-01 --end 2024-01-31 --categories "3,4"
```

### search - 搜索

```bash
# 搜索交易
coder-firefly-cli search transactions --query "超市"

# 分页搜索
coder-firefly-cli search transactions --query "餐饮" --limit 10 --page 2
```

### info - 系统信息

```bash
# 获取系统信息
coder-firefly-cli info about

# 检查连接状态
coder-firefly-cli info status
```

## JSON 输出

所有命令都支持 `--json` 参数以结构化格式输出：

```bash
# 查看账户列表的 JSON 输出
coder-firefly-cli --json accounts list

# 查看交易详情的 JSON 输出
coder-firefly-cli --json transactions get --id 456

# 查看洞察报告的 JSON 输出
coder-firefly-cli --json insights expense --start 2024-01-01 --end 2024-01-31
```

JSON 输出便于脚本处理和数据分析，所有字段都以标准 JSON 格式返回。

## 常见工作流示例

### 查看账户余额

```bash
# 1. 检查连接
coder-firefly-cli info status

# 2. 列出资产账户
coder-firefly-cli accounts list --type asset

# 3. 查看账户详情（获取余额）
coder-firefly-cli accounts get --id <account_id>
```

### 记录日常支出

```bash
# 1. 查找支出账户
coder-firefly-cli accounts list --type expense

# 2. 创建支出交易
coder-firefly-cli transactions create \
  --description "午餐" \
  --amount 35.00 \
  --source-account <asset_account_id> \
  --category "餐饮" \
  --tags "工作日"
```

### 月度财务报告

```bash
# 1. 支出报告
coder-firefly-cli --json insights expense --start 2024-01-01 --end 2024-01-31

# 2. 收入报告
coder-firefly-cli --json insights income --start 2024-01-01 --end 2024-01-31

# 3. 搜索特定交易
coder-firefly-cli --json search transactions --query "超市" --start 2024-01-01 --end 2024-01-31
```

### 预算管理

```bash
# 1. 创建预算
coder-firefly-cli budgets create --name "餐饮预算"

# 2. 设置预算限额
coder-firefly-cli budgets limit-create \
  --budget-id 1 \
  --amount 2000 \
  --start 2024-01-01 \
  --end 2024-01-31

# 3. 查看预算使用情况
coder-firefly-cli budgets limits --budget-id 1
```

## 故障排除

### 连接失败

```
错误: 无法连接到 Firefly III 实例
```

检查：
1. Firefly III 实例是否正在运行
2. 基础 URL 是否正确（注意结尾不要带斜杠）
3. 网络连接是否正常

### 认证失败

```
错误: 认证失败: Personal Access Token 无效
```

检查：
1. PAT 是否正确
2. PAT 是否已过期
3. 在 Firefly III 的 选项 > 个人资料 > OAuth 中生成新的 PAT

### 数据格式问题

```
错误: 请求参数错误
```

检查：
1. 金额是否为字符串格式（如 "100.00"）
2. 日期格式是否为 YYYY-MM-DD
3. 必需参数是否都已提供

### 资源未找到

```
错误: 资源未找到
```

检查：
1. ID 是否正确
2. 资源是否存在（可能已被删除）

## 开发

```bash
# 安装开发依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 带覆盖率报告
pytest --cov=src

# 代码格式化
black src/
```

## 项目结构

```
coder-firefly-cli/
├── setup.py              # 包安装配置
├── requirements.txt      # 依赖列表
├── README.md             # 项目文档
├── SKILL.md              # AI Agent Skill 文档
├── .github/
│   └── workflows/
│       └── publish.yml   # GitHub Actions 自动发布
└── src/
    ├── api_client.py     # Firefly III API 客户端
    ├── cli.py            # CLI 主入口
    └── commands/         # 命令模块
        ├── accounts.py
        ├── bills.py
        ├── budgets.py
        ├── categories.py
        ├── info.py
        ├── insights.py
        ├── piggy_banks.py
        ├── search.py
        ├── tags.py
        └── transactions.py
```

## 许可证

MIT License
