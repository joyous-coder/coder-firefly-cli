r"""
Firefly III API 客户端

封装 Firefly III REST API 调用，处理认证、错误和响应解析。
"""

import requests
import os
from typing import Dict, Any, Optional


class FireflyClient:
    """Firefly III API 客户端"""

    def __init__(self, base_url: str, pat: str):
        """
        初始化 Firefly III 客户端

        Args:
            base_url: Firefly III 实例地址
            pat: Personal Access Token
        """
        self.base_url = base_url.rstrip('/')
        self.pat = pat
        self.headers = {
            'Authorization': f'Bearer {pat}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }

        # 验证连接
        self._validate_connection()

    def _validate_connection(self):
        """验证与 Firefly III 实例的连接"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/about",
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()
        except requests.exceptions.ConnectionError:
            raise RuntimeError(
                f"无法连接到 Firefly III 实例: {self.base_url}\n"
                f"请检查:\n"
                f"1. Firefly III 实例是否正在运行\n"
                f"2. 基础 URL 是否正确\n"
                f"3. 网络连接是否正常"
            )
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise RuntimeError(
                    "认证失败: Personal Access Token 无效\n"
                    "请在 Firefly III 的 选项 > 个人资料 > OAuth 中生成新的 PAT"
                )
            raise RuntimeError(f"HTTP 错误 {response.status_code}: {response.text}")

    def request(self, method: str, endpoint: str, params: Dict = None, data: Dict = None) -> Dict[str, Any]:
        """
        发送请求到 Firefly III API

        Args:
            method: HTTP 方法 (get, post, put, delete)
            endpoint: API 端点路径 (例如 /accounts)
            params: URL 查询参数
            data: 请求体数据

        Returns:
            API 响应的 JSON 数据
        """
        url = f"{self.base_url}/api/v1{endpoint}"

        try:
            response = requests.request(
                method=method.upper(),
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=30
            )
            response.raise_for_status()
            if response.status_code == 204:
                return {"status": "success", "code": 204}
            return response.json()
        except requests.exceptions.ConnectionError:
            raise RuntimeError(f"无法连接到 Firefly III 实例: {self.base_url}")
        except requests.exceptions.HTTPError as e:
            if response.status_code == 401:
                raise RuntimeError("认证失败: Personal Access Token 无效")
            elif response.status_code == 404:
                raise RuntimeError(f"资源未找到: {endpoint}")
            elif response.status_code == 422:
                error_detail = response.json().get('message', '未知错误')
                raise RuntimeError(f"请求参数错误: {error_detail}")
            else:
                raise RuntimeError(f"HTTP 错误 {response.status_code}: {response.text}")
        except requests.exceptions.Timeout:
            raise RuntimeError("请求超时，请检查网络连接")
        except Exception as e:
            raise RuntimeError(f"请求失败: {e}")

    def get(self, endpoint: str, params: Dict = None) -> Dict[str, Any]:
        """发送 GET 请求"""
        return self.request('get', endpoint, params=params)

    def post(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """发送 POST 请求"""
        return self.request('post', endpoint, data=data)

    def put(self, endpoint: str, data: Dict = None) -> Dict[str, Any]:
        """发送 PUT 请求"""
        return self.request('put', endpoint, data=data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """发送 DELETE 请求"""
        return self.request('delete', endpoint)

    # ========== 关于 ==========
    def get_about(self) -> Dict[str, Any]:
        """获取 Firefly III 系统信息"""
        return self.get("/about")

    # ========== 账户 ==========
    def get_accounts(self, params: Dict = None) -> Dict[str, Any]:
        """获取账户列表"""
        return self.get("/accounts", params=params)

    def get_account(self, account_id: int) -> Dict[str, Any]:
        """获取单个账户详情"""
        return self.get(f"/accounts/{account_id}")

    def create_account(self, data: Dict) -> Dict[str, Any]:
        """创建新账户"""
        return self.post("/accounts", data=data)

    def update_account(self, account_id: int, data: Dict) -> Dict[str, Any]:
        """更新账户"""
        return self.put(f"/accounts/{account_id}", data=data)

    def delete_account(self, account_id: int) -> Dict[str, Any]:
        """删除账户"""
        return self.delete(f"/accounts/{account_id}")

    # ========== 交易 ==========
    def get_transactions(self, params: Dict = None) -> Dict[str, Any]:
        """获取交易列表"""
        return self.get("/transactions", params=params)

    def get_transaction(self, transaction_id: int) -> Dict[str, Any]:
        """获取单个交易详情"""
        return self.get(f"/transactions/{transaction_id}")

    def create_transaction(self, data: Dict) -> Dict[str, Any]:
        """创建新交易"""
        return self.post("/transactions", data=data)

    def update_transaction(self, transaction_id: int, data: Dict) -> Dict[str, Any]:
        """更新交易"""
        return self.put(f"/transactions/{transaction_id}", data=data)

    def delete_transaction(self, transaction_id: int) -> Dict[str, Any]:
        """删除交易"""
        return self.delete(f"/transactions/{transaction_id}")

    # ========== 预算 ==========
    def get_budgets(self, params: Dict = None) -> Dict[str, Any]:
        """获取预算列表"""
        return self.get("/budgets", params=params)

    def get_budget(self, budget_id: int) -> Dict[str, Any]:
        """获取单个预算详情"""
        return self.get(f"/budgets/{budget_id}")

    def create_budget(self, data: Dict) -> Dict[str, Any]:
        """创建新预算"""
        return self.post("/budgets", data=data)

    def update_budget(self, budget_id: int, data: Dict) -> Dict[str, Any]:
        """更新预算"""
        return self.put(f"/budgets/{budget_id}", data=data)

    def delete_budget(self, budget_id: int) -> Dict[str, Any]:
        """删除预算"""
        return self.delete(f"/budgets/{budget_id}")

    def get_budget_limits(self, budget_id: int, params: Dict = None) -> Dict[str, Any]:
        """获取预算限额"""
        return self.get(f"/budgets/{budget_id}/limits", params=params)

    def create_budget_limit(self, budget_id: int, data: Dict) -> Dict[str, Any]:
        """创建预算限额"""
        return self.post(f"/budgets/{budget_id}/limits", data=data)

    def update_budget_limit(self, budget_limit_id: int, data: Dict) -> Dict[str, Any]:
        """更新预算限额"""
        return self.put(f"/budget_limits/{budget_limit_id}", data=data)

    def delete_budget_limit(self, budget_limit_id: int) -> Dict[str, Any]:
        """删除预算限额"""
        return self.delete(f"/budget_limits/{budget_limit_id}")

    # ========== 分类 ==========
    def get_categories(self, params: Dict = None) -> Dict[str, Any]:
        """获取分类列表"""
        return self.get("/categories", params=params)

    def get_category(self, category_id: int) -> Dict[str, Any]:
        """获取单个分类详情"""
        return self.get(f"/categories/{category_id}")

    def create_category(self, data: Dict) -> Dict[str, Any]:
        """创建新分类"""
        return self.post("/categories", data=data)

    def update_category(self, category_id: int, data: Dict) -> Dict[str, Any]:
        """更新分类"""
        return self.put(f"/categories/{category_id}", data=data)

    def delete_category(self, category_id: int) -> Dict[str, Any]:
        """删除分类"""
        return self.delete(f"/categories/{category_id}")

    # ========== 标签 ==========
    def get_tags(self, params: Dict = None) -> Dict[str, Any]:
        """获取标签列表"""
        return self.get("/tags", params=params)

    def get_tag(self, tag_id: str) -> Dict[str, Any]:
        """获取单个标签详情"""
        return self.get(f"/tags/{tag_id}")

    def create_tag(self, data: Dict) -> Dict[str, Any]:
        """创建新标签"""
        return self.post("/tags", data=data)

    def update_tag(self, tag_id: str, data: Dict) -> Dict[str, Any]:
        """更新标签"""
        return self.put(f"/tags/{tag_id}", data=data)

    def delete_tag(self, tag_id: str) -> Dict[str, Any]:
        """删除标签"""
        return self.delete(f"/tags/{tag_id}")

    # ========== 账单 ==========
    def get_bills(self, params: Dict = None) -> Dict[str, Any]:
        """获取账单列表"""
        return self.get("/bills", params=params)

    def get_bill(self, bill_id: int) -> Dict[str, Any]:
        """获取单个账单详情"""
        return self.get(f"/bills/{bill_id}")

    def create_bill(self, data: Dict) -> Dict[str, Any]:
        """创建新账单"""
        return self.post("/bills", data=data)

    def update_bill(self, bill_id: int, data: Dict) -> Dict[str, Any]:
        """更新账单"""
        return self.put(f"/bills/{bill_id}", data=data)

    def delete_bill(self, bill_id: int) -> Dict[str, Any]:
        """删除账单"""
        return self.delete(f"/bills/{bill_id}")

    # ========== 储蓄罐 ==========
    def get_piggy_banks(self, params: Dict = None) -> Dict[str, Any]:
        """获取储蓄罐列表"""
        return self.get("/piggy-banks", params=params)

    def get_piggy_bank(self, piggy_bank_id: int) -> Dict[str, Any]:
        """获取单个储蓄罐详情"""
        return self.get(f"/piggy-banks/{piggy_bank_id}")

    def create_piggy_bank(self, data: Dict) -> Dict[str, Any]:
        """创建新储蓄罐"""
        return self.post("/piggy-banks", data=data)

    def update_piggy_bank(self, piggy_bank_id: int, data: Dict) -> Dict[str, Any]:
        """更新储蓄罐"""
        return self.put(f"/piggy-banks/{piggy_bank_id}", data=data)

    def delete_piggy_bank(self, piggy_bank_id: int) -> Dict[str, Any]:
        """删除储蓄罐"""
        return self.delete(f"/piggy-banks/{piggy_bank_id}")

    # ========== 搜索 ==========
    def search_transactions(self, query: str, params: Dict = None) -> Dict[str, Any]:
        """搜索交易"""
        p = params or {}
        p['query'] = query
        return self.get("/search/transactions", params=p)

    # ========== 洞察 ==========
    def get_insight(self, insight_type: str, params: Dict = None) -> Dict[str, Any]:
        """获取洞察报告"""
        return self.get(f"/insight/{insight_type}", params=params)

    # ========== 摘要 ==========
    def get_summary(self, summary_type: str, params: Dict = None) -> Dict[str, Any]:
        """获取摘要"""
        return self.get(f"/summary/{summary_type}", params=params)

    # ========== 导出 ==========
    def export_data(self, export_type: str, params: Dict = None) -> Dict[str, Any]:
        """导出数据"""
        return self.get(f"/data/export/{export_type}", params=params)
