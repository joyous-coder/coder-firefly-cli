r"""
储蓄罐管理命令组
"""

import click
from ..cli import get_client, output


@click.group()
def piggy_banks():
    """管理储蓄罐"""
    pass


@piggy_banks.command(name="list")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
def piggy_banks_list(limit, page):
    """列出所有储蓄罐"""
    client = get_client()
    params = {"limit": limit, "page": page}
    result = client.get_piggy_banks(params)
    output(result)


@piggy_banks.command(name="get")
@click.option("--id", required=True, type=int, help="储蓄罐 ID")
def piggy_banks_get(id):
    """获取储蓄罐详情"""
    client = get_client()
    result = client.get_piggy_bank(id)
    output(result)


@piggy_banks.command(name="create")
@click.option("--name", required=True, help="储蓄罐名称")
@click.option("--account-id", required=True, type=int, help="关联账户 ID")
@click.option("--target-amount", required=True, help="目标金额")
@click.option("--current-amount", default="0", help="当前金额")
@click.option("--start-date", help="开始日期 (YYYY-MM-DD)")
@click.option("--target-date", help="目标日期 (YYYY-MM-DD)")
@click.option("--notes", help="备注")
def piggy_banks_create(name, account_id, target_amount, current_amount, start_date, target_date, notes):
    """创建新储蓄罐"""
    client = get_client()

    data = {
        "name": name,
        "account_id": account_id,
        "target_amount": target_amount,
        "current_amount": current_amount,
    }
    if start_date:
        data["start_date"] = start_date
    if target_date:
        data["target_date"] = target_date
    if notes:
        data["notes"] = notes

    result = client.create_piggy_bank(data)
    output(result)


@piggy_banks.command(name="update")
@click.option("--id", required=True, type=int, help="储蓄罐 ID")
@click.option("--name", help="储蓄罐名称")
@click.option("--target-amount", help="目标金额")
@click.option("--current-amount", help="当前金额")
@click.option("--notes", help="备注")
def piggy_banks_update(id, name, target_amount, current_amount, notes):
    """更新现有储蓄罐"""
    client = get_client()

    data = {}
    if name:
        data["name"] = name
    if target_amount:
        data["target_amount"] = target_amount
    if current_amount:
        data["current_amount"] = current_amount
    if notes:
        data["notes"] = notes

    if not data:
        click.echo("错误: 至少需要提供一个更新字段", err=True)
        return

    result = client.update_piggy_bank(id, data)
    output(result)


@piggy_banks.command(name="delete")
@click.option("--id", required=True, type=int, help="储蓄罐 ID")
@click.confirmation_option(prompt="确定要删除此储蓄罐吗？")
def piggy_banks_delete(id):
    """删除储蓄罐"""
    client = get_client()
    result = client.delete_piggy_bank(id)
    output(result)
