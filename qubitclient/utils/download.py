# -*- coding: utf-8 -*-
"""Download resources from GitHub repositories."""

from __future__ import annotations

import os
import requests


def download_github_folder(
    owner: str,
    repo: str,
    path: str,
    branch: str,
    local_dir: str,
    token: str | None = None,
) -> None:
    """
    Recursively download a folder from a GitHub repository.

    Args:
        owner: GitHub username, e.g. 'yaqiangsun'
        repo: Repository name, e.g. 'QubitClient'
        path: Folder path within the repo, e.g. 'resources/lqcs'
        branch: Branch name, e.g. 'main'
        local_dir: Local directory to save files, e.g. './lqcs'
        token: GitHub Personal Access Token (optional, raises API rate limit)
    """
    api_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{path}"
    params = {"ref": branch}
    headers = {"User-Agent": "Mozilla/5.0"}
    if token:
        headers["Authorization"] = f"token {token}"

    def _download_recursive(api_path: str, current_local: str) -> None:
        resp = requests.get(api_path, headers=headers, params=params)
        if resp.status_code != 200:
            print(f"获取失败: {api_path}, 状态码 {resp.status_code}")
            if resp.status_code == 403 and not token:
                print(
                    "提示：遇到GitHub API速率限制（每小时60次）。可申请token并传入token参数解决。"
                )
            return
        items = resp.json()
        if not isinstance(items, list):
            items = [items]

        for item in items:
            if item["type"] == "file":
                file_url = item["download_url"]
                file_path = os.path.join(current_local, item["name"])
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                file_resp = requests.get(file_url, headers=headers)
                with open(file_path, "wb") as f:
                    f.write(file_resp.content)
                print(f"下载: {file_path}")
            elif item["type"] == "dir":
                sub_local = os.path.join(current_local, item["name"])
                os.makedirs(sub_local, exist_ok=True)
                _download_recursive(item["url"], sub_local)

    os.makedirs(local_dir, exist_ok=True)
    _download_recursive(api_url, local_dir)
