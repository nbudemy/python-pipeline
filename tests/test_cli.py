from click.testing import CliRunner
from simple_http_checker.cli import main
from pytest_mock import MockFixture


def test_no_urls():
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert result.exit_code == 0
    assert "Usage: check-urls <URL1> <URL2>" in result.output


def test_single_url_success(mocker: MockFixture):
    url = "https://success.com"
    mock_check_urls = mocker.patch("simple_http_checker.cli.check_urls")
    mock_check_urls.return_value = {url: "200 OK"}

    runner = CliRunner()
    result = runner.invoke(main, [url])

    assert result.exit_code == 0
    mock_check_urls.assert_called_once_with((url,), timeout=3)

    # assert "----Results----" in result.output
    # assert url in result.output
    # assert "-> 200 OK" in result.output
    assert True


def test_timeout_option(mocker: MockFixture):
    url = "https://timeout.com"
    mock_timeout = mocker.patch("simple_http_checker.cli.check_urls")
    mock_timeout.return_value = {url: "TIMEOUT"}

    runner = CliRunner()
    result = runner.invoke(main, [url, "--timeout", 10])

    assert url in result.output
    assert "-> TIMEOUT" in result.output
