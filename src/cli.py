r"""
Firefly III CLI - 个人财务管理命令行工具

独立的 CLI 工具，用于连接和管理 Firefly III 实例。
"""

import click
import json
import os
import sys
from typing import Dict, Any, Optional

from api_client import FireflyClient

# 全局状态
_json_output = False
_client = None


def get_client() -> FireflyClient:
    """获取客户端实例，如果未初始化则抛出错误"""
    if _client is None:
        raise RuntimeError("客户端未初始化，请检查配置")
    return _client


def output(data: Any):
    """统一输出格式：JSON 或人类可读"""
    if _json_output:
        try:
            click.echo(json.dumps(data, indent=2, ensure_ascii=False))
        except UnicodeEncodeError:
            click.echo(json.dumps(data, indent=2, ensure_ascii=True))
    else:
        # 人类可读格式
        if isinstance(data, dict):
            if 'data' in data:
                # Firefly III API 标准响应格式
                items = data['data']
                if isinstance(items, list):
                    for item in items:
                        attrs = item.get('attributes', {})
                        name = attrs.get('name', item.get('id'))
                        click.echo(f"  {item.get('id', 'N/A')}: {name}")
                else:
                    attrs = items.get('attributes', {})
                    for key, value in attrs.items():
                        click.echo(f"  {key}: {value}")
            elif 'meta' in data:
                # 带元数据的响应
                click.echo(f"  总计: {data.get('meta', {}).get('pagination', {}).get('total', 'N/A')}")
            else:
                for key, value in data.items():
                    click.echo(f"  {key}: {value}")
        elif isinstance(data, list):
            for item in data:
                click.echo(f"  - {item}")
        else:
            click.echo(f"  {data}")


@click.group()
@click.option("--json", "use_json", is_flag=True, help="以 JSON 格式输出")
@click.option("--base-url", help="Firefly III 基础 URL")
@click.option("--pat", help="Personal Access Token")
@click.pass_context
def cli(ctx, use_json, base_url, pat):
    """Firefly III CLI - 个人财务管理命令行工具

    示例:
        coder-firefly-cli --base-url https://firefly.example.com --pat YOUR_TOKEN accounts list

    环境变量:
        FIREFLY_BASE_URL: Firefly III 实例地址
        FIREFLY_PAT: Personal Access Token
    """
    global _json_output, _client

    _json_output = use_json

    # 从参数和环境变量获取配置
    base_url = base_url or os.environ.get('FIREFLY_BASE_URL')
    pat = pat or os.environ.get('FIREFLY_PAT')

    if not base_url or not pat:
        click.echo("错误: 必须提供 FIREFLY_BASE_URL 和 FIREFLY_PAT", err=True)
        click.echo("\n使用方法:", err=True)
        click.echo("  coder-firefly-cli --base-url URL --pat TOKEN", err=True)
        click.echo("\n或设置环境变量:", err=True)
        click.echo("  export FIREFLY_BASE_URL=https://firefly.yourdomain.com", err=True)
        click.echo("  export FIREFLY_PAT=your-personal-access-token", err=True)
        ctx.exit(1)

    try:
        _client = FireflyClient(base_url, pat)
    except RuntimeError as e:
        click.echo(f"错误: {e}", err=True)
        ctx.exit(1)


# 导入命令组
from commands.accounts import accounts
from commands.transactions import transactions
from commands.budgets import budgets
from commands.categories import categories
from commands.tags import tags
from commands.bills import bills
from commands.piggy_banks import piggy_banks
from commands.search import search
from commands.insights import insights
from commands.info import info

# 注册命令组
cli.add_command(accounts)
cli.add_command(transactions)
cli.add_command(budgets)
cli.add_command(categories)
cli.add_command(tags)
cli.add_command(bills)
cli.add_command(piggy_banks)
cli.add_command(search)
cli.add_command(insights)
cli.add_command(info)


def main():
    """入口点"""
    cli()


if __name__ == '__main__':
    main()
