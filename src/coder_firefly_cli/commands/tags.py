r"""
标签管理命令组
"""

import click
from ..cli import get_client, output


@click.group()
def tags():
    """管理标签"""
    pass


@tags.command(name="list")
@click.option("--limit", default=50, help="限制结果数量")
@click.option("--page", default=1, help="页码")
def tags_list(limit, page):
    """列出所有标签"""
    client = get_client()
    params = {"limit": limit, "page": page}
    result = client.get_tags(params)
    output(result)


@tags.command(name="get")
@click.option("--id", required=True, help="标签 ID")
def tags_get(id):
    """获取标签详情"""
    client = get_client()
    result = client.get_tag(id)
    output(result)


@tags.command(name="create")
@click.option("--tag", required=True, help="标签名称")
@click.option("--date", help="日期 (YYYY-MM-DD)")
@click.option("--description", help="描述")
@click.option("--latitude", help="纬度")
@click.option("--longitude", help="经度")
@click.option("--zoom", help="缩放级别")
@click.option("--notes", help="备注")
def tags_create(tag, date, description, latitude, longitude, zoom, notes):
    """创建新标签"""
    client = get_client()

    data = {"tag": tag}
    if date:
        data["date"] = date
    if description:
        data["description"] = description
    if latitude:
        data["latitude"] = latitude
    if longitude:
        data["longitude"] = longitude
    if zoom:
        data["zoom"] = zoom
    if notes:
        data["notes"] = notes

    result = client.create_tag(data)
    output(result)


@tags.command(name="update")
@click.option("--id", required=True, help="标签 ID")
@click.option("--tag", help="标签名称")
@click.option("--date", help="日期 (YYYY-MM-DD)")
@click.option("--description", help="描述")
@click.option("--notes", help="备注")
def tags_update(id, tag, date, description, notes):
    """更新现有标签"""
    client = get_client()

    data = {}
    if tag:
        data["tag"] = tag
    if date:
        data["date"] = date
    if description:
        data["description"] = description
    if notes:
        data["notes"] = notes

    if not data:
        click.echo("错误: 至少需要提供一个更新字段", err=True)
        return

    result = client.update_tag(id, data)
    output(result)


@tags.command(name="delete")
@click.option("--id", required=True, help="标签 ID")
@click.confirmation_option(prompt="确定要删除此标签吗？")
def tags_delete(id):
    """删除标签"""
    client = get_client()
    result = client.delete_tag(id)
    output(result)
