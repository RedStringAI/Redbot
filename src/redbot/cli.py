from __future__ import annotations

import argparse
from pathlib import Path

from redbot.llm import DemoLLMClient, LLMConfig, OpenAICompatibleClient
from redbot.knowledge import import_path
from redbot.runner import RedbotRunner
from redbot.server import serve
from redbot.store import RedbotStore
from redbot.templates import get_template, list_templates


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="redbot",
        description="Redbot: a lightweight personal AI execution assistant.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("templates", help="List built-in task templates.")

    run_parser = subparsers.add_parser("run", help="Run one Redbot task.")
    run_parser.add_argument("template_id", help="Template ID, such as short-video-script.")
    run_parser.add_argument("--topic", "-t", required=True, help="Task topic.")
    run_parser.add_argument("--audience", "-a", default="普通用户", help="Target audience.")
    run_parser.add_argument("--context", "-c", default="", help="Background material.")
    run_parser.add_argument("--demo", action="store_true", help="Run without an API key.")
    run_parser.add_argument(
        "--workspace",
        "-w",
        default="redbot_workspace",
        help="Output workspace directory.",
    )

    serve_parser = subparsers.add_parser("serve", help="Start the local Redbot client server.")
    serve_parser.add_argument("--host", default="127.0.0.1", help="Bind host.")
    serve_parser.add_argument("--port", type=int, default=8765, help="Bind port.")
    serve_parser.add_argument(
        "--workspace",
        "-w",
        default="redbot_workspace",
        help="Workspace for database, artifacts, and traces.",
    )
    serve_parser.add_argument("--demo", action="store_true", help="Run without a model API key.")

    kb_parser = subparsers.add_parser("kb", help="Knowledge base commands.")
    kb_subparsers = kb_parser.add_subparsers(dest="kb_command", required=True)
    kb_import = kb_subparsers.add_parser("import", help="Import .md/.txt files into the local KB.")
    kb_import.add_argument("path", help="File or directory to import.")
    kb_import.add_argument(
        "--workspace",
        "-w",
        default="redbot_workspace",
        help="Workspace containing redbot.db.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if args.command == "templates":
        return _templates_command()
    if args.command == "run":
        return _run_command(args)
    if args.command == "serve":
        serve(host=args.host, port=args.port, workspace=args.workspace, demo=args.demo)
        return 0
    if args.command == "kb":
        return _kb_command(args)
    parser.error(f"Unknown command: {args.command}")
    return 2


def _templates_command() -> int:
    for template in list_templates():
        print(f"{template.id}\t{template.name}\t{template.description}")
    return 0


def _run_command(args: argparse.Namespace) -> int:
    template = get_template(args.template_id)
    llm = DemoLLMClient() if args.demo else OpenAICompatibleClient(LLMConfig.from_env())
    result = RedbotRunner(llm=llm, workspace=Path(args.workspace)).run(
        template=template,
        topic=args.topic,
        audience=args.audience,
        context=args.context,
    )
    print(f"Artifact: {result.artifact_path}")
    print(f"Trace: {result.trace_path}")
    return 0


def _kb_command(args: argparse.Namespace) -> int:
    if args.kb_command == "import":
        workspace = Path(args.workspace)
        store = RedbotStore(workspace / "redbot.db")
        count = import_path(store, args.path)
        print(f"Imported {count} knowledge document(s).")
        return 0
    raise ValueError(f"Unknown kb command: {args.kb_command}")
