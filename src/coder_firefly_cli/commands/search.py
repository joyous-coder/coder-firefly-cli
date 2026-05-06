r"""
搜索命令组
"""

import click
from ..cli import get_client, output


@click.group()
def search():
    """搜索交易"""
    pass


@search.command(name="transactions")
@click.option("--query", required=True, help="搜索关键词")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
def search_transactions(query, limit, page):
    """搜索交易"""
    client = get_client()
    params = {"limit": limit, "page": page}
    
    result = client.search_transactions(query, params)
    output(result)
