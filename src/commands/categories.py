r"""
分类管理命令组
"""

import click
from cli import get_client, output


@click.group()
def categories():
    """管理分类"""
    pass


@categories.command(name="list")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
def categories_list(limit, page):
    """列出所有分类"""
    client = get_client()
    params = {"limit": limit, "page": page}
    result = client.get_categories(params)
    output(result)


@categories.command(name="get")
@click.option("--id", required=True, type=int, help="分类 ID")
def categories_get(id):
    """获取分类详情"""
    client = get_client()
    result = client.get_category(id)
    output(result)


@categories.command(name="create")
@click.option("--name", required=True, help="分类名称")
@click.option("--notes", help="备注")
def categories_create(name, notes):
    """创建新分类"""
    client = get_client()

    data = {"name": name}
    if notes:
        data["notes"] = notes

    result = client.create_category(data)
    output(result)


@categories.command(name="update")
@click.option("--id", required=True, type=int, help="分类 ID")
@click.option("--name", help="分类名称")
@click.option("--notes", help="备注")
def categories_update(id, name, notes):
    """更新现有分类"""
    client = get_client()

    data = {}
    if name:
        data["name"] = name
    if notes:
        data["notes"] = notes

    if not data:
        click.echo("错误: 至少需要提供一个更新字段", err=True)
        return

    result = client.update_category(id, data)
    output(result)


@categories.command(name="delete")
@click.option("--id", required=True, type=int, help="分类 ID")
@click.confirmation_option(prompt="确定要删除此分类吗？")
def categories_delete(id):
    """删除分类"""
    client = get_client()
    result = client.delete_category(id)
    output(result)
