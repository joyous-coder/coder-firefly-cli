import pytest
from click.testing import CliRunner
from unittest.mock import MagicMock, patch

from cli import cli


@pytest.fixture
def runner():
    """创建 Click 测试运行器"""
    return CliRunner()


@pytest.fixture
def mock_client():
    """创建模拟的 API 客户端"""
    client = MagicMock()
    return client


class TestCliBase:
    """测试 CLI 基础功能"""

    def test_cli_without_args(self, runner):
        """测试不带参数运行 CLI 应该显示帮助信息"""
        result = runner.invoke(cli, [])
        # Click group 没有子命令时 exit_code=2（显示帮助）
        assert result.exit_code == 2
        assert "Usage:" in result.output

    def test_cli_with_args_no_subcommand(self, runner):
        """测试带参数但不带子命令运行 CLI 应显示帮助"""
        with patch('cli.FireflyClient') as mock_client_class:
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token'
            ])
            # Click group 没有子命令时显示帮助
            assert result.exit_code == 2
            assert "Usage:" in result.output

    def test_cli_help(self, runner):
        """测试 CLI 帮助信息"""
        result = runner.invoke(cli, ['--help'])
        assert result.exit_code == 0
        assert 'Firefly III CLI' in result.output
        assert '--base-url' in result.output
        assert '--pat' in result.output
        assert '--json' in result.output

    def test_cli_json_output_flag(self, runner):
        """测试 JSON 输出标志"""
        with patch('cli.FireflyClient') as mock_client_class:
            mock_client = MagicMock()
            mock_client.get_about.return_value = {
                "data": {"type": "system", "attributes": {"version": "6.1.0"}}
            }
            mock_client_class.return_value = mock_client

            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                '--json',
                'info', 'about'
            ])
            assert result.exit_code == 0
            assert '"data"' in result.output


class TestAccountsCommands:
    """测试账户命令"""

    def test_accounts_list(self, runner, mock_client):
        """测试列出账户"""
        mock_client.get_accounts.return_value = {
            "data": [
                {"id": "1", "attributes": {"name": "现金"}},
                {"id": "2", "attributes": {"name": "储蓄"}}
            ]
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'accounts', 'list'
            ])
            assert result.exit_code == 0
            mock_client.get_accounts.assert_called_once()
            assert "现金" in result.output
            assert "储蓄" in result.output

    def test_accounts_list_with_type_filter(self, runner, mock_client):
        """测试带类型筛选的账户列表"""
        mock_client.get_accounts.return_value = {"data": []}

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'accounts', 'list', '--type', 'asset'
            ])
            assert result.exit_code == 0
            mock_client.get_accounts.assert_called_once_with(
                {"limit": 50, "page": 1, "type": "asset"}
            )

    def test_accounts_get(self, runner, mock_client):
        """测试获取单个账户"""
        mock_client.get_account.return_value = {
            "data": {
                "id": "1",
                "attributes": {
                    "name": "测试账户",
                    "type": "asset"
                }
            }
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'accounts', 'get', '--id', '1'
            ])
            assert result.exit_code == 0
            mock_client.get_account.assert_called_once_with(1)
            assert "测试账户" in result.output

    def test_accounts_create(self, runner, mock_client):
        """测试创建账户"""
        mock_client.create_account.return_value = {
            "data": {"id": "123", "attributes": {"name": "新账户"}}
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'accounts', 'create',
                '--name', '新账户',
                '--type', 'asset',
                '--currency-code', 'CNY'
            ])
            assert result.exit_code == 0
            mock_client.create_account.assert_called_once()
            call_args = mock_client.create_account.call_args[0][0]
            assert call_args["name"] == "新账户"
            assert call_args["type"] == "asset"
            assert call_args["currency_code"] == "CNY"

    def test_accounts_delete(self, runner, mock_client):
        """测试删除账户"""
        mock_client.delete_account.return_value = {"status": "success", "code": 204}

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'accounts', 'delete', '--id', '1'
            ], input='y\n')
            assert result.exit_code == 0
            mock_client.delete_account.assert_called_once_with(1)


class TestTransactionsCommands:
    """测试交易命令"""

    def test_transactions_list(self, runner, mock_client):
        """测试列出交易"""
        mock_client.get_transactions.return_value = {
            "data": [
                {"id": "1", "attributes": {"description": "超市购物", "amount": "100.00", "name": "超市购物"}}
            ]
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'transactions', 'list'
            ])
            assert result.exit_code == 0
            mock_client.get_transactions.assert_called_once()
            assert "超市购物" in result.output

    def test_transactions_list_with_date_range(self, runner, mock_client):
        """测试带日期范围的交易列表"""
        mock_client.get_transactions.return_value = {"data": []}

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'transactions', 'list',
                '--start', '2024-01-01',
                '--end', '2024-01-31'
            ])
            assert result.exit_code == 0
            # 检查调用参数
            call_args = mock_client.get_transactions.call_args
            # 支持位置参数或关键字参数
            if call_args.kwargs:
                params = call_args.kwargs.get("params", {})
            else:
                params = call_args[0][0] if call_args[0] else {}
            assert params.get("start") == "2024-01-01"
            assert params.get("end") == "2024-01-31"

    def test_transactions_create(self, runner, mock_client):
        """测试创建交易"""
        mock_client.create_transaction.return_value = {
            "data": {"id": "456", "attributes": {"description": "超市购物"}}
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'transactions', 'create',
                '--description', '超市购物',
                '--amount', '150.00',
                '--source-account', '1'
            ])
            assert result.exit_code == 0
            mock_client.create_transaction.assert_called_once()
            call_args = mock_client.create_transaction.call_args[0][0]
            assert call_args["group_title"] == "超市购物"
            assert call_args["transactions"][0]["amount"] == "150.00"

    def test_transactions_delete(self, runner, mock_client):
        """测试删除交易"""
        mock_client.delete_transaction.return_value = {"status": "success", "code": 204}

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'transactions', 'delete', '--id', '1'
            ], input='y\n')
            assert result.exit_code == 0
            mock_client.delete_transaction.assert_called_once_with(1)


class TestBudgetsCommands:
    """测试预算命令"""

    def test_budgets_list(self, runner, mock_client):
        """测试列出预算"""
        mock_client.get_budgets.return_value = {
            "data": [{"id": "1", "attributes": {"name": "餐饮"}}]
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'budgets', 'list'
            ])
            assert result.exit_code == 0
            mock_client.get_budgets.assert_called_once()
            assert "餐饮" in result.output

    def test_budgets_create(self, runner, mock_client):
        """测试创建预算"""
        mock_client.create_budget.return_value = {
            "data": {"id": "1", "attributes": {"name": "新预算"}}
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'budgets', 'create', '--name', '新预算'
            ])
            assert result.exit_code == 0
            mock_client.create_budget.assert_called_once_with({"name": "新预算"})

    def test_budgets_limit_create(self, runner, mock_client):
        """测试创建预算限额"""
        mock_client.create_budget_limit.return_value = {
            "data": {"id": "10", "attributes": {"amount": "2000.00"}}
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'budgets', 'limit-create',
                '--budget-id', '1',
                '--amount', '2000',
                '--start', '2024-01-01',
                '--end', '2024-01-31'
            ])
            assert result.exit_code == 0
            mock_client.create_budget_limit.assert_called_once()


class TestCategoriesCommands:
    """测试分类命令"""

    def test_categories_list(self, runner, mock_client):
        """测试列出分类"""
        mock_client.get_categories.return_value = {
            "data": [{"id": "1", "attributes": {"name": "餐饮"}}]
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'categories', 'list'
            ])
            assert result.exit_code == 0
            assert "餐饮" in result.output


class TestSearchCommands:
    """测试搜索命令"""

    def test_search_transactions(self, runner, mock_client):
        """测试搜索交易"""
        mock_client.search_transactions.return_value = {
            "data": [{"id": "1", "attributes": {"description": "超市购物", "name": "超市购物"}}]
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'search', 'transactions', '--query', '超市'
            ])
            assert result.exit_code == 0
            mock_client.search_transactions.assert_called_once()
            assert "超市" in result.output


class TestInfoCommands:
    """测试系统信息命令"""

    def test_info_about(self, runner, mock_client):
        """测试获取系统信息"""
        mock_client.get_about.return_value = {
            "data": {
                "attributes": {
                    "version": "6.1.0",
                    "api_version": "2.0.4"
                }
            }
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'info', 'about'
            ])
            assert result.exit_code == 0
            mock_client.get_about.assert_called_once()

    def test_info_status(self, runner, mock_client):
        """测试连接状态"""
        mock_client.get_about.return_value = {
            "data": {
                "attributes": {
                    "version": "6.1.0",
                    "api_version": "2.0.4"
                }
            }
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                'info', 'status'
            ])
            assert result.exit_code == 0
            assert "连接正常" in result.output


class TestJsonOutput:
    """测试 JSON 输出格式"""

    def test_json_output_accounts_list(self, runner, mock_client):
        """测试 JSON 输出格式"""
        mock_client.get_accounts.return_value = {
            "data": [{"id": "1", "attributes": {"name": "现金"}}]
        }

        with patch('cli.FireflyClient', return_value=mock_client):
            result = runner.invoke(cli, [
                '--base-url', 'https://test.firefly.local',
                '--pat', 'test_token',
                '--json',
                'accounts', 'list'
            ])
            assert result.exit_code == 0
            assert '"data"' in result.output
            assert '"name": "现金"' in result.output


class TestErrorHandling:
    """测试错误处理"""

    def test_connection_error(self, runner):
        """测试连接错误处理"""
        from cli import FireflyClient
        with patch('cli.FireflyClient', side_effect=RuntimeError("无法连接")):
            result = runner.invoke(cli, [
                '--base-url', 'https://invalid.local',
                '--pat', 'test_token',
                'accounts', 'list'
            ])
            assert result.exit_code != 0
            assert "无法连接" in result.output

    def test_missing_required_params(self, runner):
        """测试缺少必需参数"""
        result = runner.invoke(cli, ['accounts', 'get'])
        assert result.exit_code != 0
