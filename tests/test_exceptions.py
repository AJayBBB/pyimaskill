import pytest

from pyimaskill.exceptions import (
    ImaAuthError,
    ImaError,
    ImaNotFoundError,
    ImaPermissionError,
    ImaRateLimitError,
    ImaServerError,
    ImaValidationError,
    raise_for_retcode,
)


def test_raise_for_retcode_success():
    raise_for_retcode(0, "成功")


def test_raise_for_retcode_auth_error():
    with pytest.raises(ImaAuthError) as exc_info:
        raise_for_retcode(20004, "鉴权失败")
    assert exc_info.value.retcode == 20004
    assert exc_info.value.errmsg == "鉴权失败"


def test_raise_for_retcode_not_found():
    with pytest.raises(ImaNotFoundError):
        raise_for_retcode(100006, "笔记已删除")


def test_raise_for_retcode_rate_limit():
    with pytest.raises(ImaRateLimitError):
        raise_for_retcode(20002, "超过限频")


def test_raise_for_retcode_permission():
    with pytest.raises(ImaPermissionError):
        raise_for_retcode(100005, "不是笔记的作者")


def test_raise_for_retcode_validation():
    with pytest.raises(ImaValidationError):
        raise_for_retcode(100001, "参数错误")


def test_raise_for_retcode_server():
    with pytest.raises(ImaServerError):
        raise_for_retcode(100003, "服务器内部错误")


def test_raise_for_retcode_unknown():
    with pytest.raises(ImaError) as exc_info:
        raise_for_retcode(999999, "未知错误")
    assert exc_info.value.retcode == 999999
