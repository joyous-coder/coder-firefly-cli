import pytest
import responses
import sys
import os

# 确保可以导入 src 目录下的模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from api_client import FireflyClient


@pytest.fixture
def base_url():
    """测试用的 Firefly III 基础 URL"""
    return "https://test.firefly.local"


@pytest.fixture
def pat():
    """测试用的 Personal Access Token"""
    return "test_pat_12345"


@pytest.fixture
def client(base_url, pat):
    """创建 API 客户端实例（用于需要已验证客户端的测试）"""
    # 使用 mock 来绕过连接验证
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            f"{base_url}/api/v1/about",
            json={
                "data": {
                    "type": "system",
                    "id": "1",
                    "attributes": {
                        "version": "6.1.0",
                        "api_version": "2.0.4"
                    }
                }
            },
            status=200
        )
        client = FireflyClient(base_url, pat)
    return client


@pytest.fixture
def sample_account():
    """示例账户数据"""
    return {
        "type": "accounts",
        "id": "1",
        "attributes": {
            "created_at": "2024-01-01T12:00:00+01:00",
            "updated_at": "2024-01-01T12:00:00+01:00",
            "name": "测试账户",
            "type": "asset",
            "account_role": "defaultAsset",
            "currency_code": "CNY",
            "current_balance": "1000.00",
            "current_balance_date": "2024-01-01"
        }
    }


@pytest.fixture
def sample_transaction():
    """示例交易数据"""
    return {
        "type": "transactions",
        "id": "1",
        "attributes": {
            "created_at": "2024-01-15T12:00:00+01:00",
            "updated_at": "2024-01-15T12:00:00+01:00",
            "description": "测试交易",
            "amount": "100.00",
            "type": "withdrawal",
            "date": "2024-01-15"
        }
    }


@pytest.fixture
def mock_api_response():
    """通用 mock API 响应结构"""
    def _make_response(data, meta=None):
        response = {"data": data}
        if meta:
            response["meta"] = meta
        return response
    return _make_response
