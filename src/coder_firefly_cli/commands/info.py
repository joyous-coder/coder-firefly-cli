r"""
系统信息命令组
"""

import click
from ..cli import get_client, output


@click.group()
def info():
    """系统信息"""
    pass


@info.command(name="about")
def info_about():
    """获取 Firefly III 系统信息"""
    client = get_client()
    result = client.get_about()
    output(result)


@info.command(name="status")
def info_status():
    """检查 Firefly III 连接状态"""
    try:
        client = get_client()
        result = client.get_about()
        click.echo("Firefly III 连接正常")
        if 'data' in result:
            attrs = result['data'].get('attributes', {})
            click.echo(f"  版本: {attrs.get('version', 'N/A')}")
            click.echo(f"  API 版本: {attrs.get('api_version', 'N/A')}")
            click.echo(f"  环境: {attrs.get('environment', 'N/A')}")
    except Exception as e:
        click.echo(f"连接失败: {e}", err=True)
