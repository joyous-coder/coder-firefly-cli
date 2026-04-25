import pytest
import responses
from requests.exceptions import ConnectionError, Timeout

from api_client import FireflyClient


class TestFireflyClientInit:
    """测试 FireflyClient 初始化"""

    @responses.activate
    def test_init_success(self, base_url, pat):
        """测试成功初始化客户端"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/about",
            json={
                "data": {
                    "type": "system",
                    "attributes": {
                        "version": "6.1.0",
                        "api_version": "2.0.4"
                    }
                }
            },
            status=200
        )

        client = FireflyClient(base_url, pat)
        assert client.base_url == base_url
        assert client.pat == pat
        assert "Authorization" in client.headers
        assert client.headers["Authorization"] == f"Bearer {pat}"

    @responses.activate
    def test_init_trailing_slash_removed(self, base_url, pat):
        """测试基础 URL 末尾的斜杠被正确移除"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/about",
            json={"data": {"type": "system"}},
            status=200
        )

        client = FireflyClient(base_url + "/", pat)
        assert client.base_url == base_url

    @responses.activate
    def test_init_connection_error(self, base_url, pat):
        """测试连接失败时抛出 RuntimeError"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/about",
            body=ConnectionError("Connection refused")
        )

        with pytest.raises(RuntimeError, match="无法连接到 Firefly III 实例"):
            FireflyClient(base_url, pat)

    @responses.activate
    def test_init_auth_error(self, base_url, pat):
        """测试认证失败时抛出 RuntimeError"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/about",
            json={"message": "Unauthorized"},
            status=401
        )

        with pytest.raises(RuntimeError, match="认证失败"):
            FireflyClient(base_url, pat)


class TestRequestMethods:
    """测试 HTTP 请求方法"""

    @responses.activate
    def test_get_request(self, client, base_url, pat):
        """测试 GET 请求"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/accounts",
            json={"data": [{"id": "1", "attributes": {"name": "现金"}}]},
            status=200
        )

        result = client.get("/accounts")
        assert "data" in result
        assert len(result["data"]) == 1
        assert result["data"][0]["attributes"]["name"] == "现金"

    @responses.activate
    def test_post_request(self, client, base_url):
        """测试 POST 请求"""
        responses.add(
            responses.POST,
            f"{base_url}/api/v1/accounts",
            json={
                "data": {
                    "type": "accounts",
                    "id": "123",
                    "attributes": {"name": "新账户"}
                }
            },
            status=200
        )

        result = client.post("/accounts", data={"name": "新账户"})
        assert result["data"]["id"] == "123"

    @responses.activate
    def test_put_request(self, client, base_url):
        """测试 PUT 请求"""
        responses.add(
            responses.PUT,
            f"{base_url}/api/v1/accounts/1",
            json={
                "data": {
                    "type": "accounts",
                    "id": "1",
                    "attributes": {"name": "更新后的账户"}
                }
            },
            status=200
        )

        result = client.put("/accounts/1", data={"name": "更新后的账户"})
        assert result["data"]["attributes"]["name"] == "更新后的账户"

    @responses.activate
    def test_delete_request(self, client, base_url):
        """测试 DELETE 请求"""
        responses.add(
            responses.DELETE,
            f"{base_url}/api/v1/accounts/1",
            status=204
        )

        result = client.delete("/accounts/1")
        assert result["status"] == "success"
        assert result["code"] == 204


class TestErrorHandling:
    """测试错误处理"""

    @responses.activate
    def test_404_error(self, client, base_url):
        """测试 404 错误处理"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/accounts/999",
            json={"message": "Not Found"},
            status=404
        )

        with pytest.raises(RuntimeError, match="资源未找到"):
            client.get_account(999)

    @responses.activate
    def test_422_error(self, client, base_url):
        """测试 422 验证错误处理"""
        responses.add(
            responses.POST,
            f"{base_url}/api/v1/accounts",
            json={"message": "验证失败：名称不能为空"},
            status=422
        )

        with pytest.raises(RuntimeError, match="请求参数错误"):
            client.create_account({})

    @responses.activate
    def test_timeout_error(self, client, base_url):
        """测试超时错误处理"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/accounts",
            body=Timeout("Request timed out")
        )

        with pytest.raises(RuntimeError, match="请求超时"):
            client.get_accounts()


class TestAccountEndpoints:
    """测试账户相关端点"""

    @responses.activate
    def test_get_accounts(self, client, base_url, sample_account):
        """测试获取账户列表"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/accounts",
            json={"data": [sample_account]},
            status=200
        )

        result = client.get_accounts()
        assert len(result["data"]) == 1
        assert result["data"][0]["attributes"]["name"] == "测试账户"

    @responses.activate
    def test_get_accounts_with_params(self, client, base_url):
        """测试带参数的账户列表请求"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/accounts",
            json={"data": []},
            status=200
        )

        client.get_accounts(params={"type": "asset", "limit": 10, "page": 2})

        request = responses.calls[0].request
        assert "type=asset" in request.url
        assert "limit=10" in request.url
        assert "page=2" in request.url

    @responses.activate
    def test_get_account(self, client, base_url, sample_account):
        """测试获取单个账户"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/accounts/1",
            json={"data": sample_account},
            status=200
        )

        result = client.get_account(1)
        assert result["data"]["id"] == "1"

    @responses.activate
    def test_create_account(self, client, base_url):
        """测试创建账户"""
        responses.add(
            responses.POST,
            f"{base_url}/api/v1/accounts",
            json={
                "data": {
                    "type": "accounts",
                    "id": "123",
                    "attributes": {
                        "name": "新储蓄账户",
                        "type": "asset"
                    }
                }
            },
            status=200
        )

        result = client.create_account({
            "name": "新储蓄账户",
            "type": "asset",
            "currency_code": "CNY"
        })
        assert result["data"]["attributes"]["name"] == "新储蓄账户"


class TestTransactionEndpoints:
    """测试交易相关端点"""

    @responses.activate
    def test_get_transactions(self, client, base_url, sample_transaction):
        """测试获取交易列表"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/transactions",
            json={"data": [sample_transaction]},
            status=200
        )

        result = client.get_transactions()
        assert len(result["data"]) == 1
        assert result["data"][0]["attributes"]["description"] == "测试交易"

    @responses.activate
    def test_get_transactions_with_date_range(self, client, base_url):
        """测试带日期范围的交易查询"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/transactions",
            json={"data": []},
            status=200
        )

        client.get_transactions(params={"start": "2024-01-01", "end": "2024-01-31"})

        request = responses.calls[0].request
        assert "start=2024-01-01" in request.url
        assert "end=2024-01-31" in request.url

    @responses.activate
    def test_create_transaction(self, client, base_url):
        """测试创建交易"""
        responses.add(
            responses.POST,
            f"{base_url}/api/v1/transactions",
            json={
                "data": {
                    "type": "transactions",
                    "id": "456",
                    "attributes": {
                        "description": "超市购物",
                        "amount": "150.00"
                    }
                }
            },
            status=200
        )

        result = client.create_transaction({
            "group_title": "超市购物",
            "transactions": [{
                "type": "withdrawal",
                "amount": "150.00",
                "description": "超市购物",
                "source_id": "1"
            }]
        })
        assert result["data"]["attributes"]["description"] == "超市购物"


class TestBudgetEndpoints:
    """测试预算相关端点"""

    @responses.activate
    def test_get_budgets(self, client, base_url):
        """测试获取预算列表"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/budgets",
            json={
                "data": [
                    {
                        "type": "budgets",
                        "id": "1",
                        "attributes": {"name": "餐饮预算"}
                    }
                ]
            },
            status=200
        )

        result = client.get_budgets()
        assert len(result["data"]) == 1
        assert result["data"][0]["attributes"]["name"] == "餐饮预算"

    @responses.activate
    def test_create_budget_limit(self, client, base_url):
        """测试创建预算限额"""
        responses.add(
            responses.POST,
            f"{base_url}/api/v1/budgets/1/limits",
            json={
                "data": {
                    "type": "budget_limits",
                    "id": "10",
                    "attributes": {
                        "amount": "2000.00",
                        "start": "2024-01-01",
                        "end": "2024-01-31"
                    }
                }
            },
            status=200
        )

        result = client.create_budget_limit(1, {
            "amount": "2000.00",
            "start": "2024-01-01",
            "end": "2024-01-31"
        })
        assert result["data"]["attributes"]["amount"] == "2000.00"


class TestSearchEndpoints:
    """测试搜索相关端点"""

    @responses.activate
    def test_search_transactions(self, client, base_url):
        """测试搜索交易"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/search/transactions",
            json={
                "data": [
                    {
                        "type": "transactions",
                        "id": "1",
                        "attributes": {"description": "超市购物"}
                    }
                ]
            },
            status=200
        )

        result = client.search_transactions("超市")
        assert len(result["data"]) == 1
        # 中文会被 URL 编码
        assert "query=" in responses.calls[0].request.url


class TestHeaders:
    """测试请求头"""

    @responses.activate
    def test_auth_header_present(self, client, base_url, pat):
        """测试认证头是否正确设置"""
        responses.add(
            responses.GET,
            f"{base_url}/api/v1/accounts",
            json={"data": []},
            status=200
        )

        client.get_accounts()

        request = responses.calls[0].request
        assert request.headers["Authorization"] == f"Bearer {pat}"
        assert request.headers["Accept"] == "application/json"
        assert request.headers["Content-Type"] == "application/json"
