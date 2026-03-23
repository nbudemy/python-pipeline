from asyncio import timeout

import pytest
import requests
import sys
from pytest_mock import MockFixture, MockerFixture
from simple_http_checker.checker import check_urls


def test_check_urls_success(mocker: MockFixture):
    mock_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True

    mock_requests_get.return_value = mock_response

    urls = ["https://www.example.com"]

    results = check_urls(urls)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "200 OK"


def test_check_urls_custom_timeout(mocker: MockFixture):
    mock_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 200
    mock_response.reason = "OK"
    mock_response.ok = True

    mock_requests_get.return_value = mock_response

    urls = ["https://www.example.com"]
    custom_timeout = 10

    results = check_urls(urls, timeout=custom_timeout)

    mock_requests_get.assert_called_once_with(urls[0], timeout=custom_timeout)
    assert results[urls[0]] == "200 OK"


def test_check_urls_client_error(mocker: MockFixture):
    mock_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_response = mocker.MagicMock(spec=requests.Response)
    mock_response.status_code = 404
    mock_response.reason = "Not found"
    mock_response.ok = False

    mock_requests_get.return_value = mock_response

    urls = ["https://www.giveme.com/404"]

    results = check_urls(urls)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == "404 Not found"


@pytest.mark.parametrize(
    "error_exception, expected_status",
    [
        (requests.exceptions.Timeout, "TIMEOUT"),
        (requests.exceptions.ConnectionError, "CONNECTION_ERROR"),
        (requests.exceptions.RequestException, "REQUEST_ERROR: RequestException"),
    ],
)
def test_check_urls_request_exceptions(
    mocker: MockerFixture, error_exception, expected_status
):
    mock_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_requests_get.side_effect = error_exception(f"Simulated {expected_status}")

    urls = ["https://problems.com"]

    results = check_urls(urls)

    mock_requests_get.assert_called_once_with(urls[0], timeout=5)
    assert results[urls[0]] == expected_status


def test_check_urls_with_multiple_urls(mocker: MockerFixture):
    mock_requests_get = mocker.patch("simple_http_checker.checker.requests.get")

    mock_ok_response = mocker.MagicMock(spec=requests.Response)
    mock_ok_response.status_code = 200
    mock_ok_response.ok = True
    mock_ok_response.reason = "OK"

    mock_server_error_response = mocker.MagicMock(spec=requests.Response)
    mock_server_error_response.status_code = 500
    mock_server_error_response.ok = False
    mock_server_error_response.reason = "Server Error"

    mock_timeout_exception = requests.exceptions.Timeout("Mocked timeout")

    mock_requests_get.side_effect = [
        mock_ok_response,
        mock_server_error_response,
        mock_timeout_exception,
    ]

    urls = ["https://success.com", "https://servererror.com", "https://exception.com"]
    results = check_urls(urls)

    assert len(results) == 3
    assert mock_requests_get.call_count == 3
    assert results[urls[0]] == "200 OK"
    assert results[urls[1]] == "500 Server Error"
    assert results[urls[2]] == "TIMEOUT"


def test_check_urls_empty_list():
    result = check_urls([])
    assert result == {}
