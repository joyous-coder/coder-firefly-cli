r"""
账户管理命令组
"""

import click
from cli import get_client, output


@click.group()
def accounts():
    """管理账户"""
    pass


@accounts.command(name="list")
@click.option("--type", 
              type=click.Choice(['asset', 'expense', 'revenue', 'liability', 'all']),
              default='all',
              help="按账户类型筛选")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
def accounts_list(type, limit, page):
    """列出所有账户"""
    client = get_client()
    params = {"limit": limit, "page": page}
    if type != 'all':
        params["type"] = type
    
    result = client.get_accounts(params)
    output(result)


@accounts.command(name="get")
@click.option("--id", required=True, type=int, help="账户 ID")
def accounts_get(id):
    """获取账户详情"""
    client = get_client()
    result = client.get_account(id)
    output(result)


@accounts.command(name="create")
@click.option("--name", required=True, help="账户名称")
@click.option("--type", 
              required=True,
              type=click.Choice(['asset', 'expense', 'revenue', 'liability']),
              help="账户类型")
@click.option("--currency-code", default="USD", help="货币代码 (ISO 4217)")
@click.option("--opening-balance", default="0", help="初始余额")
@click.option("--account-role", help="账户角色 (用于资产账户)")
@click.option("--iban", help="IBAN")
@click.option("--bic", help="BIC")
@click.option("--account-number", help="账户号码")
@click.option("--notes", help="备注")
def accounts_create(name, type, currency_code, opening_balance, account_role, iban, bic, account_number, notes):
    """创建新账户"""
    client = get_client()
    
    data = {
        "name": name,
        "type": type,
        "currency_code": currency_code,
        "opening_balance": opening_balance,
    }
    
    if account_role:
        data["account_role"] = account_role
    if iban:
        data["iban"] = iban
    if bic:
        data["bic"] = bic
    if account_number:
        data["account_number"] = account_number
    if notes:
        data["notes"] = notes
    
    result = client.create_account(data)
    output(result)


@accounts.command(name="update")
@click.option("--id", required=True, type=int, help="账户 ID")
@click.option("--name", help="账户名称")
@click.option("--opening-balance", help="初始余额")
@click.option("--notes", help="备注")
def accounts_update(id, name, opening_balance, notes):
    """更新现有账户"""
    client = get_client()
    
    data = {}
    if name:
        data["name"] = name
    if opening_balance:
        data["opening_balance"] = opening_balance
    if notes:
        data["notes"] = notes
    
    if not data:
        click.echo("错误: 至少需要提供一个更新字段", err=True)
        return
    
    result = client.update_account(id, data)
    output(result)


@accounts.command(name="delete")
@click.option("--id", required=True, type=int, help="账户 ID")
@click.confirmation_option(prompt="确定要删除此账户吗？")
def accounts_delete(id):
    """删除账户"""
    client = get_client()
    result = client.delete_account(id)
    output(result)
