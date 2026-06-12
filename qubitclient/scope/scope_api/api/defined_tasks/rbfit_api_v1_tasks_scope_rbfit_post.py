from http import HTTPStatus
from typing import Any

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.body_rbfit_api_v1_tasks_scope_rbfit_post import BodyRbfitApiV1TasksScopeRbfitPost
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    body: BodyRbfitApiV1TasksScopeRbfitPost,
    type_: str | Unset = "rbfit",
) -> dict[str, Any]:
    headers: dict[str, Any] = {}

    params: dict[str, Any] = {}

    params["type"] = type_

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    _kwargs: dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/tasks/scope/rbfit",
        "params": params,
    }

    _kwargs["files"] = body.to_multipart()

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Any | HTTPValidationError | None:
    if response.status_code == 200:
        response_200 = response.json()
        return response_200

    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422

    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[Any | HTTPValidationError]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyRbfitApiV1TasksScopeRbfitPost,
    type_: str | Unset = "rbfit",
) -> Response[Any | HTTPValidationError]:
    r"""Rbfit

     rbfit

    Args:
        files: 上传的.npy文件列表
        type: 任务类型，默认为\"rbfit\"

    Returns:
        dict: 包含检测结果的字典

    Args:
        type_ (str | Unset): 任务类型 Default: 'rbfit'.
        body (BodyRbfitApiV1TasksScopeRbfitPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        type_=type_,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient | Client,
    body: BodyRbfitApiV1TasksScopeRbfitPost,
    type_: str | Unset = "rbfit",
) -> Any | HTTPValidationError | None:
    r"""Rbfit

     rbfit

    Args:
        files: 上传的.npy文件列表
        type: 任务类型，默认为\"rbfit\"

    Returns:
        dict: 包含检测结果的字典

    Args:
        type_ (str | Unset): 任务类型 Default: 'rbfit'.
        body (BodyRbfitApiV1TasksScopeRbfitPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return sync_detailed(
        client=client,
        body=body,
        type_=type_,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient | Client,
    body: BodyRbfitApiV1TasksScopeRbfitPost,
    type_: str | Unset = "rbfit",
) -> Response[Any | HTTPValidationError]:
    r"""Rbfit

     rbfit

    Args:
        files: 上传的.npy文件列表
        type: 任务类型，默认为\"rbfit\"

    Returns:
        dict: 包含检测结果的字典

    Args:
        type_ (str | Unset): 任务类型 Default: 'rbfit'.
        body (BodyRbfitApiV1TasksScopeRbfitPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Any | HTTPValidationError]
    """

    kwargs = _get_kwargs(
        body=body,
        type_=type_,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient | Client,
    body: BodyRbfitApiV1TasksScopeRbfitPost,
    type_: str | Unset = "rbfit",
) -> Any | HTTPValidationError | None:
    r"""Rbfit

     rbfit

    Args:
        files: 上传的.npy文件列表
        type: 任务类型，默认为\"rbfit\"

    Returns:
        dict: 包含检测结果的字典

    Args:
        type_ (str | Unset): 任务类型 Default: 'rbfit'.
        body (BodyRbfitApiV1TasksScopeRbfitPost):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Any | HTTPValidationError
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
            type_=type_,
        )
    ).parsed
