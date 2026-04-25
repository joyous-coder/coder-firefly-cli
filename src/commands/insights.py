r"""
洞察命令组
"""

import click
from cli import get_client, output


@click.group()
def insights():
    """查看财务洞察"""
    pass


@insights.command(name="expense")
@click.option("--start", help="开始日期 (YYYY-MM-DD)")
@click.option("--end", help="结束日期 (YYYY-MM-DD)")
@click.option("--accounts", help="账户 ID (逗号分隔)")
@click.option("--categories", help="分类 ID (逗号分隔)")
@click.option("--budgets", help="预算 ID (逗号分隔)")
@click.option("--tags", help="标签 (逗号分隔)")
def insights_expense(start, end, accounts, categories, budgets, tags):
    """支出洞察"""
    client = get_client()
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    if accounts:
        params["accounts"] = accounts
    if categories:
        params["categories"] = categories
    if budgets:
        params["budgets"] = budgets
    if tags:
        params["tags"] = tags

    result = client.get_insight("expense", params)
    output(result)


@insights.command(name="income")
@click.option("--start", help="开始日期 (YYYY-MM-DD)")
@click.option("--end", help="结束日期 (YYYY-MM-DD)")
@click.option("--accounts", help="账户 ID (逗号分隔)")
@click.option("--categories", help="分类 ID (逗号分隔)")
@click.option("--tags", help="标签 (逗号分隔)")
def insights_income(start, end, accounts, categories, tags):
    """收入洞察"""
    client = get_client()
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    if accounts:
        params["accounts"] = accounts
    if categories:
        params["categories"] = categories
    if tags:
        params["tags"] = tags

    result = client.get_insight("income", params)
    output(result)


@insights.command(name="transfer")
@click.option("--start", help="开始日期 (YYYY-MM-DD)")
@click.option("--end", help="结束日期 (YYYY-MM-DD)")
@click.option("--accounts", help="账户 ID (逗号分隔)")
@click.option("--tags", help="标签 (逗号分隔)")
def insights_transfer(start, end, accounts, tags):
    """转账洞察"""
    client = get_client()
    params = {}
    if start:
        params["start"] = start
    if end:
        params["end"] = end
    if accounts:
        params["accounts"] = accounts
    if tags:
        params["tags"] = tags

    result = client.get_insight("transfer", params)
    output(result)
