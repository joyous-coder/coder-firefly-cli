r"""
账户管理命令组
"""

import click
from ..cli import get_client, output


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
@click.option("--opening-balance", default=None, help="初始余额 (不传则不设置)")
@click.option("--opening-balance-date", help="开户日期 (YYYY-MM-DD)，当 --opening-balance 非 0 时必填")
@click.option("--account-role",
              # type=click.Choice([...]),
              default='defaultAsset',
              help="账户角色 (asset 类型必填；其他类型会被 API 忽略)")
@click.option("--iban", help="IBAN")
@click.option("--bic", help="BIC")
@click.option("--account-number", help="账户号码")
@click.option("--credit-card-type",
              type=click.Choice(['monthlyFull']),
              default=None,
              help="信用卡类型 (当 account_role=ccAsset 时必填，仅 monthlyFull)")
@click.option("--monthly-payment-date", help="信用卡账单还款日 (YYYY-MM-DD)，当 --account-role=ccAsset 时必填")
@click.option("--liability-type",
              type=click.Choice(['loan', 'debt', 'mortgage']),
              default=None,
              help="负债类型 (type=liability 时必填；信用卡选 debt)")
@click.option("--interest-period",
              type=click.Choice(['daily', 'weekly', 'monthly', 'quarterly', 'half-year', 'yearly']),
              default=None,
              help="利息周期 (type=liability 时必填；信用卡选 monthly)")
@click.option("--interest", help="利率，如 '18.5' 表示 18.5% (type=liability 时必填)")
@click.option("--liability-direction",
              type=click.Choice(['credit', 'debit']),
              default=None,
              help="负债方向 (type=liability 时必填)：credit=应收款（别人欠你），debit=应付款（你欠别人）")
@click.option("--notes", help="备注")
def accounts_create(name, type, currency_code, opening_balance, opening_balance_date, account_role, iban, bic, account_number, credit_card_type, monthly_payment_date, liability_type, interest_period, interest, liability_direction, notes):
    """创建新账户"""
    client = get_client()

    # 当 type=liability 时，Firefly III 要求必填 --liability-type, --interest-period, --interest
    if type == "liability":
        if not liability_type:
            raise click.UsageError(
                "当 --type=liability 时，必须同时指定 --liability-type (loan/debt/mortgage；信用卡选 debt)"
            )
        if not interest_period:
            raise click.UsageError(
                "当 --type=liability 时，必须同时指定 --interest-period (daily/weekly/monthly/quarterly/half-year/yearly)"
            )
        if interest is None:
            raise click.UsageError(
                "当 --type=liability 时，必须同时指定 --interest (年化利率，如 '18.5')"
            )
        if not liability_direction:
            raise click.UsageError(
                "当 --type=liability 时，必须同时指定 --liability-direction (credit/debit)"
            )

    # 当 --account-role=ccAsset 时，Firefly III 要求必填 --credit-card-type 和 --monthly-payment-date
    if account_role == "ccAsset":
        if not credit_card_type:
            raise click.UsageError(
                "当 --account-role=ccAsset 时，必须同时指定 --credit-card-type (monthlyFull)"
            )
        if not monthly_payment_date:
            raise click.UsageError(
                "当 --account-role=ccAsset 时，必须同时指定 --monthly-payment-date (YYYY-MM-DD)"
            )

    # 用 sentinel 区分"用户没传"和"用户传 0/空"
    # 仅在用户显式传了 --opening-balance 且非 0 时，要求提供 --opening-balance-date
    if opening_balance is not None and opening_balance != "" and opening_balance != "0":
        if not opening_balance_date:
            raise click.UsageError(
                "当 --opening-balance 非 0 时，必须同时指定 --opening-balance-date (YYYY-MM-DD)"
            )

    data = {
        "name": name,
        "type": type,
        "currency_code": currency_code,
    }

    # 只有用户显式传了才塞进 body
    if opening_balance is not None and opening_balance != "":
        data["opening_balance"] = opening_balance
    if opening_balance_date:
        data["opening_balance_date"] = opening_balance_date
    if account_role:
        data["account_role"] = account_role
    if credit_card_type:
        data["credit_card_type"] = credit_card_type
    if monthly_payment_date:
        data["monthly_payment_date"] = monthly_payment_date
    if liability_type:
        data["liability_type"] = liability_type
    if interest_period:
        data["interest_period"] = interest_period
    if interest is not None:
        data["interest"] = interest
    if liability_direction:
        data["liability_direction"] = liability_direction
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
