r"""
预算管理命令组
"""

import click
from cli import get_client, output


@click.group()
def budgets():
    """管理预算"""
    pass


@budgets.command(name="list")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
def budgets_list(limit, page):
    """列出所有预算"""
    client = get_client()
    params = {"limit": limit, "page": page}
    result = client.get_budgets(params)
    output(result)


@budgets.command(name="get")
@click.option("--id", required=True, type=int, help="预算 ID")
def budgets_get(id):
    """获取预算详情"""
    client = get_client()
    result = client.get_budget(id)
    output(result)


@budgets.command(name="create")
@click.option("--name", required=True, help="预算名称")
@click.option("--notes", help="备注")
def budgets_create(name, notes):
    """创建新预算"""
    client = get_client()

    data = {"name": name}
    if notes:
        data["notes"] = notes

    result = client.create_budget(data)
    output(result)


@budgets.command(name="update")
@click.option("--id", required=True, type=int, help="预算 ID")
@click.option("--name", help="预算名称")
@click.option("--notes", help="备注")
def budgets_update(id, name, notes):
    """更新现有预算"""
    client = get_client()

    data = {}
    if name:
        data["name"] = name
    if notes:
        data["notes"] = notes

    if not data:
        click.echo("错误: 至少需要提供一个更新字段", err=True)
        return

    result = client.update_budget(id, data)
    output(result)


@budgets.command(name="delete")
@click.option("--id", required=True, type=int, help="预算 ID")
@click.confirmation_option(prompt="确定要删除此预算吗？")
def budgets_delete(id):
    """删除预算"""
    client = get_client()
    result = client.delete_budget(id)
    output(result)


# ========== 预算限额 ==========

@budgets.command(name="limits")
@click.option("--budget-id", required=True, type=int, help="预算 ID")
@click.option("--start", help="开始日期 (YYYY-MM-DD)")
@click.option("--end", help="结束日期 (YYYY-MM-DD)")
def budgets_limits(budget_id, start, end):
    """列出预算限额"""
    client = get_client()
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    result = client.get_budget_limits(budget_id, params)
    output(result)


@budgets.command(name="limit-create")
@click.option("--budget-id", required=True, type=int, help="预算 ID")
@click.option("--amount", required=True, help="金额")
@click.option("--start", required=True, help="开始日期 (YYYY-MM-DD)")
@click.option("--end", required=True, help="结束日期 (YYYY-MM-DD)")
@click.option("--currency-code", default="USD", help="货币代码")
def budgets_limit_create(budget_id, amount, start, end, currency_code):
    """创建预算限额"""
    client = get_client()

    data = {
        "amount": amount,
        "start": start,
        "end": end,
        "currency_id": currency_code,
    }

    result = client.create_budget_limit(budget_id, data)
    output(result)


@budgets.command(name="limit-update")
@click.option("--id", required=True, type=int, help="预算限额 ID")
@click.option("--amount", help="金额")
def budgets_limit_update(id, amount):
    """更新预算限额"""
    client = get_client()

    data = {}
    if amount:
        data["amount"] = amount

    if not data:
        click.echo("错误: 金额是必填项", err=True)
        return

    result = client.update_budget_limit(id, data)
    output(result)


@budgets.command(name="limit-delete")
@click.option("--id", required=True, type=int, help="预算限额 ID")
@click.confirmation_option(prompt="确定要删除此预算限额吗？")
def budgets_limit_delete(id):
    """删除预算限额"""
    client = get_client()
    result = client.delete_budget_limit(id)
    output(result)
