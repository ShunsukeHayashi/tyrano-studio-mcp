#!/usr/bin/env python3
"""
TyranoStudio MCP Server
ティラノスタジオのプロジェクト管理を行うMCPサーバー
"""

import os
import json
import shutil
from pathlib import Path
from typing import Any
import mcp.types as types
from mcp.server import Server
from mcp.server.stdio import stdio_server

# TyranoStudioのベースディレクトリ
TYRANO_BASE = Path("/Users/shunsuke/TyranoStudio_mac_std_v603")
PROJECTS_DIR = TYRANO_BASE / "myprojects"
SYSTEM_MASTER_DIR = TYRANO_BASE / "system_master"
EXPORT_DIR = TYRANO_BASE / "export"
DLC_DIR = TYRANO_BASE / "dlc"

app = Server("tyrano-studio")


@app.list_tools()
async def list_tools() -> list[types.Tool]:
    """利用可能なツールのリスト"""
    return [
        types.Tool(
            name="list_projects",
            description="TyranoStudioのプロジェクト一覧を取得",
            inputSchema={
                "type": "object",
                "properties": {},
            },
        ),
        types.Tool(
            name="create_project",
            description="新しいTyranoScriptプロジェクトを作成",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "template": {
                        "type": "string",
                        "description": "テンプレート (tyranoscript_ja または tyranoscript_en)",
                        "enum": ["tyranoscript_ja", "tyranoscript_en"],
                        "default": "tyranoscript_ja",
                    },
                },
                "required": ["project_name"],
            },
        ),
        types.Tool(
            name="read_scenario",
            description="プロジェクトのシナリオファイル(.ks)を読み込む",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "scenario_file": {
                        "type": "string",
                        "description": "シナリオファイル名 (data/scenario内の.ksファイル)",
                    },
                },
                "required": ["project_name", "scenario_file"],
            },
        ),
        types.Tool(
            name="write_scenario",
            description="プロジェクトのシナリオファイル(.ks)を書き込む",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "scenario_file": {
                        "type": "string",
                        "description": "シナリオファイル名 (data/scenario内の.ksファイル)",
                    },
                    "content": {
                        "type": "string",
                        "description": "書き込む内容",
                    },
                },
                "required": ["project_name", "scenario_file", "content"],
            },
        ),
        types.Tool(
            name="list_project_files",
            description="プロジェクト内のファイル一覧を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "path": {
                        "type": "string",
                        "description": "相対パス (省略時はプロジェクトルート)",
                        "default": "",
                    },
                },
                "required": ["project_name"],
            },
        ),
        types.Tool(
            name="read_config",
            description="プロジェクトの設定ファイル(Config.tjs)を読み込む",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                },
                "required": ["project_name"],
            },
        ),
        types.Tool(
            name="write_config",
            description="プロジェクトの設定ファイル(Config.tjs)を書き込む",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "content": {
                        "type": "string",
                        "description": "書き込む内容",
                    },
                },
                "required": ["project_name", "content"],
            },
        ),
        types.Tool(
            name="add_image",
            description="プロジェクトに画像ファイルを追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "source_path": {
                        "type": "string",
                        "description": "コピー元の画像ファイルパス",
                    },
                    "dest_category": {
                        "type": "string",
                        "description": "配置先カテゴリ (fgimage, bgimage, system など)",
                    },
                    "dest_filename": {
                        "type": "string",
                        "description": "配置先ファイル名 (省略時は元のファイル名)",
                        "default": "",
                    },
                },
                "required": ["project_name", "source_path", "dest_category"],
            },
        ),
        types.Tool(
            name="delete_project",
            description="プロジェクトを削除",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                },
                "required": ["project_name"],
            },
        ),
        types.Tool(
            name="get_tyranoscript_reference",
            description="TyranoScriptのタグリファレンスを取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "category": {
                        "type": "string",
                        "description": "カテゴリ (text, character, background, choice, variable, audio, all)",
                        "enum": ["text", "character", "background", "choice", "variable", "audio", "all"],
                        "default": "all",
                    },
                },
            },
        ),
        types.Tool(
            name="validate_scenario",
            description="シナリオファイルの構文チェック（基本的なタグの検証）",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "scenario_file": {
                        "type": "string",
                        "description": "シナリオファイル名",
                    },
                },
                "required": ["project_name", "scenario_file"],
            },
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[types.TextContent]:
    """ツールの実行"""
    try:
        if name == "list_projects":
            return await list_projects_handler()
        elif name == "create_project":
            return await create_project_handler(arguments)
        elif name == "read_scenario":
            return await read_scenario_handler(arguments)
        elif name == "write_scenario":
            return await write_scenario_handler(arguments)
        elif name == "list_project_files":
            return await list_project_files_handler(arguments)
        elif name == "read_config":
            return await read_config_handler(arguments)
        elif name == "write_config":
            return await write_config_handler(arguments)
        elif name == "add_image":
            return await add_image_handler(arguments)
        elif name == "delete_project":
            return await delete_project_handler(arguments)
        elif name == "get_tyranoscript_reference":
            return await get_tyranoscript_reference_handler(arguments)
        elif name == "validate_scenario":
            return await validate_scenario_handler(arguments)
        else:
            return [types.TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"Error: {str(e)}")]


async def list_projects_handler() -> list[types.TextContent]:
    """プロジェクト一覧を取得"""
    if not PROJECTS_DIR.exists():
        return [types.TextContent(type="text", text="プロジェクトディレクトリが存在しません")]

    projects = [d.name for d in PROJECTS_DIR.iterdir() if d.is_dir()]

    if not projects:
        return [types.TextContent(type="text", text="プロジェクトが見つかりません")]

    result = "プロジェクト一覧:\n" + "\n".join(f"- {p}" for p in projects)
    return [types.TextContent(type="text", text=result)]


async def create_project_handler(arguments: dict) -> list[types.TextContent]:
    """新しいプロジェクトを作成"""
    project_name = arguments["project_name"]
    template = arguments.get("template", "tyranoscript_ja")

    project_path = PROJECTS_DIR / project_name
    template_path = SYSTEM_MASTER_DIR / template

    if project_path.exists():
        return [types.TextContent(type="text", text=f"プロジェクト '{project_name}' は既に存在します")]

    if not template_path.exists():
        return [types.TextContent(type="text", text=f"テンプレート '{template}' が見つかりません")]

    # テンプレートをコピー
    shutil.copytree(template_path, project_path)

    return [types.TextContent(type="text", text=f"プロジェクト '{project_name}' を作成しました")]


async def read_scenario_handler(arguments: dict) -> list[types.TextContent]:
    """シナリオファイルを読み込む"""
    project_name = arguments["project_name"]
    scenario_file = arguments["scenario_file"]

    # .ks拡張子を確認
    if not scenario_file.endswith(".ks"):
        scenario_file += ".ks"

    scenario_path = PROJECTS_DIR / project_name / "data" / "scenario" / scenario_file

    if not scenario_path.exists():
        return [types.TextContent(type="text", text=f"シナリオファイル '{scenario_file}' が見つかりません")]

    content = scenario_path.read_text(encoding="utf-8")
    return [types.TextContent(type="text", text=content)]


async def write_scenario_handler(arguments: dict) -> list[types.TextContent]:
    """シナリオファイルに書き込む"""
    project_name = arguments["project_name"]
    scenario_file = arguments["scenario_file"]
    content = arguments["content"]

    # .ks拡張子を確認
    if not scenario_file.endswith(".ks"):
        scenario_file += ".ks"

    scenario_dir = PROJECTS_DIR / project_name / "data" / "scenario"
    scenario_path = scenario_dir / scenario_file

    # ディレクトリが存在しない場合は作成
    scenario_dir.mkdir(parents=True, exist_ok=True)

    scenario_path.write_text(content, encoding="utf-8")

    return [types.TextContent(type="text", text=f"シナリオファイル '{scenario_file}' を保存しました")]


async def list_project_files_handler(arguments: dict) -> list[types.TextContent]:
    """プロジェクト内のファイル一覧を取得"""
    project_name = arguments["project_name"]
    rel_path = arguments.get("path", "")

    project_path = PROJECTS_DIR / project_name
    if not project_path.exists():
        return [types.TextContent(type="text", text=f"プロジェクト '{project_name}' が見つかりません")]

    target_path = project_path / rel_path if rel_path else project_path

    if not target_path.exists():
        return [types.TextContent(type="text", text=f"パス '{rel_path}' が見つかりません")]

    files = []
    dirs = []

    for item in target_path.iterdir():
        if item.is_dir():
            dirs.append(f"[DIR]  {item.name}")
        else:
            size = item.stat().st_size
            files.append(f"[FILE] {item.name} ({size} bytes)")

    result = f"プロジェクト '{project_name}' のファイル一覧 ({rel_path or 'root'}):\n"
    result += "\n".join(dirs + files)

    return [types.TextContent(type="text", text=result)]


async def read_config_handler(arguments: dict) -> list[types.TextContent]:
    """設定ファイルを読み込む"""
    project_name = arguments["project_name"]
    config_path = PROJECTS_DIR / project_name / "data" / "system" / "Config.tjs"

    if not config_path.exists():
        return [types.TextContent(type="text", text=f"設定ファイルが見つかりません")]

    content = config_path.read_text(encoding="utf-8")
    return [types.TextContent(type="text", text=content)]


async def write_config_handler(arguments: dict) -> list[types.TextContent]:
    """設定ファイルに書き込む"""
    project_name = arguments["project_name"]
    content = arguments["content"]

    config_dir = PROJECTS_DIR / project_name / "data" / "system"
    config_path = config_dir / "Config.tjs"

    config_dir.mkdir(parents=True, exist_ok=True)
    config_path.write_text(content, encoding="utf-8")

    return [types.TextContent(type="text", text=f"設定ファイルを保存しました")]


async def add_image_handler(arguments: dict) -> list[types.TextContent]:
    """画像ファイルを追加"""
    project_name = arguments["project_name"]
    source_path = Path(arguments["source_path"])
    dest_category = arguments["dest_category"]
    dest_filename = arguments.get("dest_filename", "")

    if not source_path.exists():
        return [types.TextContent(type="text", text=f"ソースファイル '{source_path}' が見つかりません")]

    # 配置先ディレクトリ
    dest_dir = PROJECTS_DIR / project_name / "data" / dest_category
    dest_dir.mkdir(parents=True, exist_ok=True)

    # ファイル名
    filename = dest_filename if dest_filename else source_path.name
    dest_path = dest_dir / filename

    # コピー
    shutil.copy2(source_path, dest_path)

    return [types.TextContent(type="text", text=f"画像ファイル '{filename}' を {dest_category} に追加しました")]


async def delete_project_handler(arguments: dict) -> list[types.TextContent]:
    """プロジェクトを削除"""
    project_name = arguments["project_name"]
    project_path = PROJECTS_DIR / project_name

    if not project_path.exists():
        return [types.TextContent(type="text", text=f"プロジェクト '{project_name}' が見つかりません")]

    shutil.rmtree(project_path)

    return [types.TextContent(type="text", text=f"プロジェクト '{project_name}' を削除しました")]


async def get_tyranoscript_reference_handler(arguments: dict) -> list[types.TextContent]:
    """TyranoScriptのタグリファレンスを取得"""
    category = arguments.get("category", "all")

    reference = {
        "text": """
【テキスト・メッセージ系タグ】
[l] - クリック待ち
[p] - クリック待ち＆改ページ
[r] - 改行
[er] - 現在のメッセージレイヤをクリア
[cm] - すべてのメッセージレイヤをクリア
[font] - フォント設定
[resetfont] - フォント設定をリセット
[ruby] - ルビ（ふりがな）を振る
[nowait] - 瞬間表示モード開始
[endnowait] - 瞬間表示モード終了
""",
        "character": """
【キャラクター系タグ】
[chara_new name="キャラ名" storage="画像ファイル"] - キャラクター定義
[chara_show name="キャラ名"] - キャラクター表示
[chara_hide name="キャラ名"] - キャラクター非表示
[chara_hide_all] - すべてのキャラクターを非表示
[chara_mod name="キャラ名" storage="画像ファイル"] - キャラクター表情変更
[chara_ptext name="キャラ名" text="表示名"] - キャラクター名表示
[chara_config] - キャラクター設定
[chara_layer name="キャラ名" layer="レイヤ番号"] - レイヤ変更
""",
        "background": """
【背景・画像系タグ】
[bg storage="画像ファイル"] - 背景変更
[image layer="レイヤ番号" storage="画像ファイル"] - 画像表示
[freeimage layer="レイヤ番号"] - 画像削除
[layopt layer="レイヤ番号" visible="true/false"] - レイヤ表示/非表示
[trans time="ミリ秒"] - トランジション実行
[wt] - トランジション完了待ち
[ptext] - テキストをレイヤに配置
[free] - レイヤ内の要素を解放
""",
        "choice": """
【選択肢・ジャンプ系タグ】
[link target="ラベル名"] - テキストリンク作成
[endlink] - リンク終了
[glink target="ラベル名" text="選択肢テキスト"] - グラフィカルリンク
[button] - ボタン作成
[jump target="ラベル名"] - ラベルへジャンプ
[call storage="シナリオファイル" target="ラベル名"] - サブルーチン呼び出し
[return] - サブルーチンから戻る
[s] - シナリオ停止
*ラベル名 - ラベル定義
""",
        "variable": """
【変数・演算系タグ】
[eval exp="変数=値"] - JavaScript式を評価
[iscript] - JavaScript開始
[endscript] - JavaScript終了
[if exp="条件式"] - 条件分岐開始
[elsif exp="条件式"] - 条件分岐（else if）
[else] - 条件分岐（else）
[endif] - 条件分岐終了
[emb exp="変数名"] - 変数埋め込み表示
[checkpoint] - ロールバックポイント登録
[rollback] - ロールバック
""",
        "audio": """
【音声系タグ】
[playbgm storage="音楽ファイル"] - BGM再生
[stopbgm] - BGM停止
[pausebgm] - BGM一時停止
[resumebgm] - BGM再開
[fadeinbgm] - BGMフェードイン
[fadeoutbgm] - BGMフェードアウト
[playse storage="効果音ファイル"] - 効果音再生
[stopse] - 効果音停止
[wse] - 効果音終了待ち
[playvideo storage="動画ファイル"] - 動画再生
[wb] - 動画再生終了待ち
"""
    }

    if category == "all":
        result = "\n".join(reference.values())
    elif category in reference:
        result = reference[category]
    else:
        result = "不明なカテゴリです"

    return [types.TextContent(type="text", text=result)]


async def validate_scenario_handler(arguments: dict) -> list[types.TextContent]:
    """シナリオファイルの基本的な構文チェック"""
    project_name = arguments["project_name"]
    scenario_file = arguments["scenario_file"]

    if not scenario_file.endswith(".ks"):
        scenario_file += ".ks"

    scenario_path = PROJECTS_DIR / project_name / "data" / "scenario" / scenario_file

    if not scenario_path.exists():
        return [types.TextContent(type="text", text=f"シナリオファイル '{scenario_file}' が見つかりません")]

    content = scenario_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    errors = []
    warnings = []

    # 基本的なチェック
    tag_stack = []
    for i, line in enumerate(lines, 1):
        line = line.strip()

        # コメントはスキップ
        if line.startswith(";") or line.startswith("//"):
            continue

        # タグの対応チェック
        if "[if" in line:
            tag_stack.append(("if", i))
        elif "[endif]" in line:
            if tag_stack and tag_stack[-1][0] == "if":
                tag_stack.pop()
            else:
                errors.append(f"行 {i}: 対応する[if]がありません")

        if "[iscript]" in line:
            tag_stack.append(("iscript", i))
        elif "[endscript]" in line:
            if tag_stack and tag_stack[-1][0] == "iscript":
                tag_stack.pop()
            else:
                errors.append(f"行 {i}: 対応する[iscript]がありません")

        # リンクの対応チェック
        if "[link" in line:
            tag_stack.append(("link", i))
        elif "[endlink]" in line:
            if tag_stack and tag_stack[-1][0] == "link":
                tag_stack.pop()
            else:
                warnings.append(f"行 {i}: 対応する[link]がありません")

    # 未閉じタグのチェック
    for tag, line_num in tag_stack:
        errors.append(f"行 {line_num}: [{tag}]が閉じられていません")

    # 結果
    if not errors and not warnings:
        result = "✓ 構文エラーは見つかりませんでした"
    else:
        result = "構文チェック結果:\n\n"
        if errors:
            result += "【エラー】\n" + "\n".join(errors) + "\n\n"
        if warnings:
            result += "【警告】\n" + "\n".join(warnings)

    return [types.TextContent(type="text", text=result)]


async def main():
    """メイン関数"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())