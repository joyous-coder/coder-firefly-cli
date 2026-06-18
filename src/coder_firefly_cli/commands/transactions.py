r"""
交易管理命令组
"""

import click
from datetime import datetime
from ..cli import get_client, output


@click.group()
def transactions():
    """管理交易"""
    pass


@transactions.command(name="list")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
@click.option("--start", help="开始日期 (YYYY-MM-DD)")
@click.option("--end", help="结束日期 (YYYY-MM-DD)")
@click.option("--type",
              type=click.Choice(['withdrawal', 'deposit', 'transfer']),
              help="交易类型")
@click.option("--source-account", help="源账户 ID 或名称")
@click.option("--destination-account", help="目标账户 ID 或名称")
def transactions_list(limit, page, start, end, type, source_account, destination_account):
    """列出交易"""
    client = get_client()
    params = {"limit": limit, "page": page}

    if start:
        params["start"] = start
    if end:
        params["end"] = end
    if type:
        params["type"] = type
    if source_account:
        params["source_id"] = source_account
    if destination_account:
        params["destination_id"] = destination_account

    result = client.get_transactions(params)
    output(result)


@transactions.command(name="get")
@click.option("--id", required=True, type=int, help="交易 ID")
def transactions_get(id):
    """获取交易详情"""
    client = get_client()
    result = client.get_transaction(id)
    output(result)


@transactions.command(name="create")
@click.option("--description", required=True, help="交易描述")
@click.option("--amount", required=True, help="交易金额")
@click.option("--source-account", required=True, help="源账户 ID")
@click.option("--destination-account", help="目标账户 ID (转账时需要)")
@click.option("--type",
              type=click.Choice(['withdrawal', 'deposit', 'transfer']),
              default='withdrawal',
              help="交易类型")
@click.option("--date", default=lambda: datetime.now().strftime('%Y-%m-%d'),
              help="交易日期 (YYYY-MM-DD)")
@click.option("--category", help="分类名称")
@click.option("--tags", help="标签 (逗号分隔)")
@click.option("--budget", help="预算名称")
@click.option("--notes", help="备注")
@click.option("--group-title", default=None,
              help="分组标题（可选）。不传则不分组，避免首页显示 '描述: 描述' 的冗余结构。")
def transactions_create(description, amount, source_account, destination_account,
                       type, date, category, tags, budget, notes, group_title):
    """创建新交易"""
    client = get_client()

    # 始终在 transaction_data 内部设置 group_title=""，避免 Firefly III
    # 自动将 description 复制为 group_title，导致首页显示 "xxx: xxx"
    transaction_data = {
        "type": type,
        "date": date,
        "amount": amount,
        "description": description,
        "source_id": source_account,
        "group_title": group_title if group_title else "",
    }

    if destination_account:
        transaction_data["destination_id"] = destination_account
    if category:
        transaction_data["category_name"] = category
    if tags:
        transaction_data["tags"] = [tag.strip() for tag in tags.split(",")]
    if budget:
        transaction_data["budget_name"] = budget
    if notes:
        transaction_data["notes"] = notes

    data = {
        "error_if_duplicate_hash": True,
        "error_if_duplicate_hash_v2": True,
        "apply_rules": True,
        "fire_webhooks": True,
        "transactions": [transaction_data]
    }

    result = client.create_transaction(data)
    output(result)


@transactions.command(name="update")
@click.option("--id", required=True, type=int, help="交易 ID")
@click.option("--description", help="交易描述")
@click.option("--amount", help="交易金额")
@click.option("--category", help="分类名称")
@click.option("--tags", help="标签 (逗号分隔)")
@click.option("--notes", help="备注")
@click.option("--group-title", "group_title", default=None,
              help="分组标题（可选）。传空字符串可清空分组标题，解决首页 '描述: 描述' 冗余问题。")
def transactions_update(id, description, amount, category, tags, notes, group_title):
    """更新现有交易"""
    client = get_client()

    transaction_data = {}
    if description:
        transaction_data["description"] = description
    if amount:
        transaction_data["amount"] = amount
    if category:
        transaction_data["category_name"] = category
    if tags:
        transaction_data["tags"] = [tag.strip() for tag in tags.split(",")]
    if notes:
        transaction_data["notes"] = notes
    # 仅当显式传入 group_title（包含空字符串）时才设置
    if group_title is not None:
        transaction_data["group_title"] = group_title

    if not transaction_data:
        click.echo("错误: 至少需要提供一个更新字段", err=True)
        return

    data = {
        "apply_rules": True,
        "fire_webhooks": True,
        "transactions": [transaction_data]
    }

    result = client.update_transaction(id, data)
    output(result)


@transactions.command(name="delete")
@click.option("--id", required=True, type=int, help="交易 ID")
@click.confirmation_option(prompt="确定要删除此交易吗？")
def transactions_delete(id):
    """删除交易"""
    client = get_client()
    result = client.delete_transaction(id)
    output(result)
