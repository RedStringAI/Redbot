from __future__ import annotations

import json
import webbrowser
from dataclasses import dataclass
from pathlib import Path

from redbot.server import serve


@dataclass(frozen=True)
class DesktopLaunchConfig:
    host: str = "127.0.0.1"
    port: int = 8765
    workspace: Path = Path("redbot_workspace")
    demo: bool = False
    open_browser: bool = True
    start_server: bool = True


@dataclass(frozen=True)
class DesktopStatus:
    local_url: str
    workspace: Path
    status_file: Path
    webhooks: dict[str, str]


def launch_desktop(config: DesktopLaunchConfig) -> DesktopStatus:
    config.workspace.mkdir(parents=True, exist_ok=True)
    local_url = f"http://{config.host}:{config.port}"
    webhooks = {
        "feishu": f"{local_url}/webhook/feishu",
        "wecom": f"{local_url}/webhook/wecom",
        "wechat": f"{local_url}/webhook/wechat",
        "generic": f"{local_url}/webhook/generic",
    }
    status_file = config.workspace / "desktop-status.json"
    status_file.write_text(
        json.dumps(
            {
                "local_url": local_url,
                "workspace": str(config.workspace),
                "webhooks": webhooks,
                "demo": config.demo,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    if config.open_browser:
        webbrowser.open(local_url)
    if config.start_server:
        serve(
            host=config.host,
            port=config.port,
            workspace=str(config.workspace),
            demo=config.demo,
        )
    return DesktopStatus(
        local_url=local_url,
        workspace=config.workspace,
        status_file=status_file,
        webhooks=webhooks,
    )
