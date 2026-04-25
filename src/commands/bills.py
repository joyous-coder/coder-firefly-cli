r"""
账单管理命令组
"""

import click
from cli import get_client, output


@click.group()
def bills():
    """管理账单"""
    pass


@bills.command(name="list")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
def bills_list(limit, page):
    """列出所有账单"""
    client = get_client()
    params = {"limit": limit, "page": page}
    result = client.get_bills(params)
    output(result)


@bills.command(name="get")
@click.option("--id", required=True, type=int, help="账单 ID")
def bills_get(id):
    """获取账单详情"""
    client = get_client()
    result = client.get_bill(id)
    output(result)


@bills.command(name="create")
@click.option("--name", required=True, help="账单名称")
@click.option("--amount-min", required=True, help="最小金额")
@click.option("--amount-max", required=True, help="最大金额")
@click.option("--date", required=True, help="账单日期 (YYYY-MM-DD)")
@click.option("--repeat-freq", default="monthly", help="重复频率")
@click.option("--skip", default=0, help="跳过次数")
@click.option("--currency-code", default="USD", help="货币代码")
@click.option("--notes", help="备注")
def bills_create(name, amount_min, amount_max, date, repeat_freq, skip, currency_code, notes):
    """创建新账单"""
    client = get_client()

    data = {
        "name": name,
        "amount_min": amount_min,
        "amount_max": amount_max,
        "date": date,
        "repeat_freq": repeat_freq,
        "skip": skip,
        "currency_code": currency_code,
    }
    if notes:
        data["notes"] = notes

    result = client.create_bill(data)
    output(result)


@bills.command(name="update")
@click.option("--id", required=True, type=int, help="账单 ID")
@click.option("--name", help="账单名称")
@click.option("--amount-min", help="最小金额")
@click.option("--amount-max", help="最大金额")
@click.option("--notes", help="备注")
def bills_update(id, name, amount_min, amount_max, notes):
    """更新现有账单"""
    client = get_client()

    data = {}
    if name:
        data["name"] = name
    if amount_min:
        data["amount_min"] = amount_min
    if amount_max:
        data["amount_max"] = amount_max
    if notes:
        data["notes"] = notes

    if not data:
        click.echo("错误: 至少需要提供一个更新字段", err=True)
        return

    result = client.update_bill(id, data)
    output(result)


@bills.command(name="delete")
@click.option("--id", required=True, type=int, help="账单 ID")
@click.confirmation_option(prompt="确定要删除此账单吗？")
def bills_delete(id):
    """删除账单"""
    client = get_client()
    result = client.delete_bill(id)
    output(result)
