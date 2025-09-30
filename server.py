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
            name="add_audio",
            description="プロジェクトに音声ファイル（BGM/効果音）を追加",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "source_path": {
                        "type": "string",
                        "description": "コピー元の音声ファイルパス",
                    },
                    "audio_type": {
                        "type": "string",
                        "description": "音声タイプ (bgm: BGM, sound: 効果音)",
                        "enum": ["bgm", "sound"],
                    },
                    "dest_filename": {
                        "type": "string",
                        "description": "配置先ファイル名 (省略時は元のファイル名)",
                        "default": "",
                    },
                },
                "required": ["project_name", "source_path", "audio_type"],
            },
        ),
        types.Tool(
            name="list_audio",
            description="プロジェクト内の音声ファイル一覧を取得",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "audio_type": {
                        "type": "string",
                        "description": "音声タイプ (bgm, sound, all)",
                        "enum": ["bgm", "sound", "all"],
                        "default": "all",
                    },
                },
                "required": ["project_name"],
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
        types.Tool(
            name="generate_scenario_template",
            description="テンプレートからシナリオを生成",
            inputSchema={
                "type": "object",
                "properties": {
                    "project_name": {
                        "type": "string",
                        "description": "プロジェクト名",
                    },
                    "scenario_file": {
                        "type": "string",
                        "description": "生成するシナリオファイル名",
                    },
                    "template_type": {
                        "type": "string",
                        "description": "テンプレートタイプ",
                        "enum": ["basic_scene", "character_intro", "choice_branch", "dialogue", "title_screen"],
                    },
                    "params": {
                        "type": "object",
                        "description": "テンプレートパラメータ（JSON形式）",
                        "default": {},
                    },
                },
                "required": ["project_name", "scenario_file", "template_type"],
            },
        ),
        types.Tool(
            name="analyze_project",
            description="プロジェクト全体を分析（シナリオ統計、リソース使用状況等）",
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
            name="analyze_scenario_flow",
            description="シナリオフローを解析（ラベル間の遷移を可視化）",
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
        elif name == "add_audio":
            return await add_audio_handler(arguments)
        elif name == "list_audio":
            return await list_audio_handler(arguments)
        elif name == "delete_project":
            return await delete_project_handler(arguments)
        elif name == "get_tyranoscript_reference":
            return await get_tyranoscript_reference_handler(arguments)
        elif name == "validate_scenario":
            return await validate_scenario_handler(arguments)
        elif name == "generate_scenario_template":
            return await generate_scenario_template_handler(arguments)
        elif name == "analyze_project":
            return await analyze_project_handler(arguments)
        elif name == "analyze_scenario_flow":
            return await analyze_scenario_flow_handler(arguments)
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


async def add_audio_handler(arguments: dict) -> list[types.TextContent]:
    """音声ファイルを追加"""
    project_name = arguments["project_name"]
    source_path = Path(arguments["source_path"])
    audio_type = arguments["audio_type"]
    dest_filename = arguments.get("dest_filename", "")

    if not source_path.exists():
        return [types.TextContent(type="text", text=f"ソースファイル '{source_path}' が見つかりません")]

    # 配置先ディレクトリ
    dest_dir = PROJECTS_DIR / project_name / "data" / audio_type
    dest_dir.mkdir(parents=True, exist_ok=True)

    # ファイル名
    filename = dest_filename if dest_filename else source_path.name
    dest_path = dest_dir / filename

    # コピー
    try:
        shutil.copy2(source_path, dest_path)
        type_name = "BGM" if audio_type == "bgm" else "効果音"
        return [types.TextContent(type="text", text=f"{type_name}ファイル '{filename}' を追加しました")]
    except Exception as e:
        return [types.TextContent(type="text", text=f"ファイルコピーエラー: {str(e)}")]


async def list_audio_handler(arguments: dict) -> list[types.TextContent]:
    """音声ファイル一覧を取得"""
    project_name = arguments["project_name"]
    audio_type = arguments.get("audio_type", "all")

    project_path = PROJECTS_DIR / project_name
    if not project_path.exists():
        return [types.TextContent(type="text", text=f"プロジェクト '{project_name}' が見つかりません")]

    result = []

    if audio_type in ["bgm", "all"]:
        bgm_dir = project_path / "data" / "bgm"
        if bgm_dir.exists():
            bgm_files = [f.name for f in bgm_dir.iterdir() if f.is_file()]
            if bgm_files:
                result.append(f"【BGM】({len(bgm_files)}件)")
                result.extend(f"  - {f}" for f in sorted(bgm_files))
            else:
                result.append("【BGM】なし")

    if audio_type in ["sound", "all"]:
        sound_dir = project_path / "data" / "sound"
        if sound_dir.exists():
            sound_files = [f.name for f in sound_dir.iterdir() if f.is_file()]
            if sound_files:
                result.append(f"【効果音】({len(sound_files)}件)")
                result.extend(f"  - {f}" for f in sorted(sound_files))
            else:
                result.append("【効果音】なし")

    if not result:
        result.append("音声ファイルが見つかりません")

    return [types.TextContent(type="text", text="\n".join(result))]


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
    """シナリオファイルの高度な構文チェック"""
    project_name = arguments["project_name"]
    scenario_file = arguments["scenario_file"]

    if not scenario_file.endswith(".ks"):
        scenario_file += ".ks"

    project_path = PROJECTS_DIR / project_name
    scenario_path = project_path / "data" / "scenario" / scenario_file

    if not scenario_path.exists():
        return [types.TextContent(type="text", text=f"シナリオファイル '{scenario_file}' が見つかりません")]

    content = scenario_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    errors = []
    warnings = []
    info = []

    # ラベルとジャンプ先を収集
    labels = set()
    jump_targets = []
    call_targets = []
    link_targets = []

    # リソース参照を収集
    image_refs = []
    bgm_refs = []
    se_refs = []
    video_refs = []
    storage_refs = []

    # キャラクター定義と使用
    defined_charas = set()
    used_charas = set()

    # 基本的なチェック
    tag_stack = []
    import re

    for i, line in enumerate(lines, 1):
        line_strip = line.strip()

        # コメントはスキップ
        if line_strip.startswith(";") or line_strip.startswith("//"):
            continue

        # ラベル定義を収集
        if line_strip.startswith("*"):
            label_name = line_strip[1:].strip()
            if label_name:
                labels.add(label_name)

        # タグの対応チェック
        if "[if" in line_strip:
            tag_stack.append(("if", i))
        elif "[endif]" in line_strip:
            if tag_stack and tag_stack[-1][0] == "if":
                tag_stack.pop()
            else:
                errors.append(f"行 {i}: 対応する[if]がありません")

        if "[iscript]" in line_strip:
            tag_stack.append(("iscript", i))
        elif "[endscript]" in line_strip:
            if tag_stack and tag_stack[-1][0] == "iscript":
                tag_stack.pop()
            else:
                errors.append(f"行 {i}: 対応する[iscript]がありません")

        if "[link" in line_strip:
            tag_stack.append(("link", i))
        elif "[endlink]" in line_strip:
            if tag_stack and tag_stack[-1][0] == "link":
                tag_stack.pop()
            else:
                warnings.append(f"行 {i}: 対応する[link]がありません")

        # ジャンプ先のチェック
        if "[jump" in line_strip or "@jump" in line_strip:
            match = re.search(r'target=["\']?\*?([^"\'\s\]]+)', line_strip)
            if match:
                target = match.group(1)
                jump_targets.append((target, i))

        if "[call" in line_strip or "@call" in line_strip:
            match = re.search(r'target=["\']?\*?([^"\'\s\]]+)', line_strip)
            if match:
                target = match.group(1)
                call_targets.append((target, i))

        if "[link" in line_strip or "[glink" in line_strip:
            match = re.search(r'target=["\']?\*?([^"\'\s\]]+)', line_strip)
            if match:
                target = match.group(1)
                link_targets.append((target, i))

        # リソース参照のチェック
        if "[bg" in line_strip or "[image" in line_strip or "[chara_new" in line_strip or "[chara_show" in line_strip or "[chara_mod" in line_strip:
            match = re.search(r'storage=["\']([^"\']+)["\']', line_strip)
            if match:
                storage = match.group(1)
                if "[bg" in line_strip:
                    image_refs.append((storage, "bgimage", i))
                elif "[image" in line_strip:
                    image_refs.append((storage, "image", i))
                elif "[chara" in line_strip:
                    image_refs.append((storage, "fgimage", i))

        if "[playbgm" in line_strip:
            match = re.search(r'storage=["\']?([^"\'\s\]]+)', line_strip)
            if match:
                bgm_refs.append((match.group(1), i))

        if "[playse" in line_strip:
            match = re.search(r'storage=["\']?([^"\'\s\]]+)', line_strip)
            if match:
                se_refs.append((match.group(1), i))

        if "[playvideo" in line_strip:
            match = re.search(r'storage=["\']?([^"\'\s\]]+)', line_strip)
            if match:
                video_refs.append((match.group(1), i))

        if "[call" in line_strip or "@call" in line_strip:
            match = re.search(r'storage=["\']([^"\']+)["\']', line_strip)
            if match:
                storage_refs.append((match.group(1), i))

        # キャラクター定義と使用
        if "[chara_new" in line_strip:
            match = re.search(r'name=["\']([^"\']+)["\']', line_strip)
            if match:
                defined_charas.add(match.group(1))

        if any(tag in line_strip for tag in ["[chara_show", "[chara_hide", "[chara_mod", "[chara_layer"]):
            match = re.search(r'name=["\']([^"\']+)["\']', line_strip)
            if match:
                used_charas.add(match.group(1))

    # 未閉じタグのチェック
    for tag, line_num in tag_stack:
        errors.append(f"行 {line_num}: [{tag}]が閉じられていません")

    # ラベル存在チェック
    for target, line_num in jump_targets + call_targets + link_targets:
        if target not in labels:
            errors.append(f"行 {line_num}: ラベル '*{target}' が定義されていません")

    # ストレージファイル存在チェック
    for storage_file, line_num in storage_refs:
        if not storage_file.endswith(".ks"):
            storage_file += ".ks"
        storage_path = project_path / "data" / "scenario" / storage_file
        if not storage_path.exists():
            warnings.append(f"行 {line_num}: シナリオファイル '{storage_file}' が見つかりません")

    # リソースファイル存在チェック
    for img_file, category, line_num in image_refs:
        img_path = project_path / "data" / category / img_file
        if not img_path.exists():
            warnings.append(f"行 {line_num}: 画像ファイル '{img_file}' が {category}/ に見つかりません")

    for bgm_file, line_num in bgm_refs:
        bgm_path = project_path / "data" / "bgm" / bgm_file
        if not bgm_path.exists():
            warnings.append(f"行 {line_num}: BGMファイル '{bgm_file}' が見つかりません")

    for se_file, line_num in se_refs:
        se_path = project_path / "data" / "sound" / se_file
        if not se_path.exists():
            warnings.append(f"行 {line_num}: 効果音ファイル '{se_file}' が見つかりません")

    for video_file, line_num in video_refs:
        video_path = project_path / "data" / "video" / video_file
        if not video_path.exists():
            warnings.append(f"行 {line_num}: 動画ファイル '{video_file}' が見つかりません")

    # 未定義キャラクター使用チェック
    for chara in used_charas:
        if chara not in defined_charas:
            warnings.append(f"キャラクター '{chara}' が定義されていません（[chara_new]で定義してください）")

    # 統計情報
    info.append(f"ラベル数: {len(labels)}")
    info.append(f"ジャンプ/リンク数: {len(jump_targets) + len(call_targets) + len(link_targets)}")
    info.append(f"定義済みキャラクター数: {len(defined_charas)}")

    # 結果
    if not errors and not warnings:
        result = "✅ 構文エラーは見つかりませんでした\n\n"
        result += "【統計】\n" + "\n".join(info)
    else:
        result = "🔍 構文チェック結果:\n\n"
        if errors:
            result += "【エラー】\n" + "\n".join(errors) + "\n\n"
        if warnings:
            result += "【警告】\n" + "\n".join(warnings) + "\n\n"
        if info:
            result += "【統計】\n" + "\n".join(info)

    return [types.TextContent(type="text", text=result)]


async def generate_scenario_template_handler(arguments: dict) -> list[types.TextContent]:
    """テンプレートからシナリオを生成"""
    project_name = arguments["project_name"]
    scenario_file = arguments["scenario_file"]
    template_type = arguments["template_type"]
    params = arguments.get("params", {})

    if not scenario_file.endswith(".ks"):
        scenario_file += ".ks"

    templates = {
        "basic_scene": lambda p: f"""; 基本シーン
*{p.get('label', 'start')}

[cm]
[bg storage="{p.get('bg', 'room.jpg')}"]

{p.get('text', 'ここにテキストを入力してください。')}[p]

[jump target="{p.get('next_label', '*end')}"]
[s]
""",
        "character_intro": lambda p: f"""; キャラクター登場シーン
*{p.get('label', 'chara_intro')}

[cm]
[bg storage="{p.get('bg', 'room.jpg')}"]

[chara_new name="{p.get('chara_name', 'character1')}" storage="{p.get('chara_image', 'chara/character1.png')}" jname="{p.get('chara_jname', 'キャラクター')}"]
[chara_show name="{p.get('chara_name', 'character1')}"]

#{p.get('chara_jname', 'キャラクター')}
{p.get('dialogue', 'こんにちは！')}[p]

[jump target="{p.get('next_label', '*next')}"]
[s]
""",
        "choice_branch": lambda p: f"""; 選択肢分岐
*{p.get('label', 'choice')}

[cm]
{p.get('prompt_text', '選択してください。')}[p]

[glink text="{p.get('choice1_text', '選択肢1')}" target="*{p.get('choice1_label', 'branch1')}" size=20 width=500 x=30 y=200]
[glink text="{p.get('choice2_text', '選択肢2')}" target="*{p.get('choice2_label', 'branch2')}" size=20 width=500 x=30 y=260]
{p.get('choice3_text') and f'[glink text="{p.get("choice3_text")}" target="*{p.get("choice3_label", "branch3")}" size=20 width=500 x=30 y=320]' or ''}
[s]

*{p.get('choice1_label', 'branch1')}
[cm]
{p.get('choice1_result', '選択肢1を選びました。')}[p]
[jump target="{p.get('next_label', '*end')}"]

*{p.get('choice2_label', 'branch2')}
[cm]
{p.get('choice2_result', '選択肢2を選びました。')}[p]
[jump target="{p.get('next_label', '*end')}"]
""",
        "dialogue": lambda p: f"""; 会話シーン
*{p.get('label', 'dialogue')}

[cm]
[bg storage="{p.get('bg', 'room.jpg')}"]

#{p.get('chara1_name', 'キャラA')}
{p.get('line1', 'こんにちは。')}[p]

#{p.get('chara2_name', 'キャラB')}
{p.get('line2', 'やあ、元気？')}[p]

#{p.get('chara1_name', 'キャラA')}
{p.get('line3', 'うん、元気だよ！')}[p]

[jump target="{p.get('next_label', '*next')}"]
[s]
""",
        "title_screen": lambda p: f"""; タイトル画面
*{p.get('label', 'title')}

[cm]
[clearfix]
[hidemenubutton]
[bg storage="{p.get('bg', 'title.jpg')}"]

[glink text="はじめから" target="*{p.get('start_label', 'start')}" size=20 width=300 x=490 y=300]
[glink text="つづきから" role="load" size=20 width=300 x=490 y=360]
[glink text="終了" role="sleepgame" size=20 width=300 x=490 y=420]
[s]
"""
    }

    if template_type not in templates:
        return [types.TextContent(type="text", text=f"不明なテンプレートタイプ: {template_type}")]

    # テンプレート生成
    content = templates[template_type](params)

    # ファイルに書き込み
    scenario_dir = PROJECTS_DIR / project_name / "data" / "scenario"
    scenario_path = scenario_dir / scenario_file

    scenario_dir.mkdir(parents=True, exist_ok=True)
    scenario_path.write_text(content, encoding="utf-8")

    return [types.TextContent(type="text", text=f"テンプレート '{template_type}' からシナリオ '{scenario_file}' を生成しました")]


async def analyze_project_handler(arguments: dict) -> list[types.TextContent]:
    """プロジェクト全体を分析"""
    project_name = arguments["project_name"]
    project_path = PROJECTS_DIR / project_name

    if not project_path.exists():
        return [types.TextContent(type="text", text=f"プロジェクト '{project_name}' が見つかりません")]

    import re

    # シナリオファイルを収集
    scenario_dir = project_path / "data" / "scenario"
    scenario_files = []
    if scenario_dir.exists():
        scenario_files = [f.name for f in scenario_dir.iterdir() if f.suffix == ".ks"]

    # リソースを収集
    resource_counts = {}
    resource_dirs = {
        "背景画像": "bgimage",
        "キャラクター画像": "fgimage",
        "その他画像": "image",
        "BGM": "bgm",
        "効果音": "sound",
        "動画": "video"
    }

    for label, dir_name in resource_dirs.items():
        res_dir = project_path / "data" / dir_name
        if res_dir.exists():
            files = [f for f in res_dir.iterdir() if f.is_file()]
            resource_counts[label] = len(files)
        else:
            resource_counts[label] = 0

    # 全シナリオを解析
    total_lines = 0
    total_text_lines = 0
    total_labels = set()
    total_jumps = 0
    total_choices = 0
    all_characters = set()
    word_count = 0

    for scenario_file in scenario_files:
        scenario_path = scenario_dir / scenario_file
        try:
            content = scenario_path.read_text(encoding="utf-8")
            lines = content.split("\n")
            total_lines += len(lines)

            for line in lines:
                line_strip = line.strip()

                # コメントをスキップ
                if line_strip.startswith(";") or line_strip.startswith("//"):
                    continue

                # ラベル
                if line_strip.startswith("*"):
                    label_name = line_strip[1:].strip()
                    if label_name:
                        total_labels.add(label_name)

                # ジャンプ/コール
                if any(tag in line_strip for tag in ["[jump", "@jump", "[call", "@call"]):
                    total_jumps += 1

                # 選択肢
                if "[glink" in line_strip or "[link" in line_strip:
                    total_choices += 1

                # キャラクター定義
                if "[chara_new" in line_strip:
                    match = re.search(r'name=["\']([^"\']+)["\']', line_strip)
                    if match:
                        all_characters.add(match.group(1))

                # テキスト行（タグがない、またはテキストを含む行）
                if line_strip and not line_strip.startswith("[") and not line_strip.startswith("*") and not line_strip.startswith(";"):
                    total_text_lines += 1
                    # 簡易的な文字数カウント（[p]などのタグを除く）
                    text_only = re.sub(r'\[.*?\]', '', line_strip)
                    word_count += len(text_only)

        except Exception as e:
            print(f"Error reading {scenario_file}: {e}")

    # プレイ時間推定（平均読書速度: 600文字/分）
    estimated_playtime = word_count / 600 if word_count > 0 else 0

    # レポート生成
    report = f"""📊 プロジェクト分析レポート: {project_name}
{'=' * 60}

【シナリオ統計】
- シナリオファイル数: {len(scenario_files)}
- 総行数: {total_lines:,}
- テキスト行数: {total_text_lines:,}
- 総文字数: {word_count:,}
- ラベル数: {len(total_labels)}
- ジャンプ/コール数: {total_jumps}
- 選択肢数: {total_choices}
- 定義済みキャラクター数: {len(all_characters)}

【推定プレイ時間】
- 約 {estimated_playtime:.1f} 分 ({estimated_playtime/60:.1f} 時間)
  ※ 平均読書速度600文字/分で計算

【リソース統計】
"""

    for label, count in resource_counts.items():
        report += f"- {label}: {count}件\n"

    if scenario_files:
        report += f"\n【シナリオファイル一覧】\n"
        for sf in sorted(scenario_files):
            report += f"- {sf}\n"

    if all_characters:
        report += f"\n【登場キャラクター】\n"
        for char in sorted(all_characters):
            report += f"- {char}\n"

    return [types.TextContent(type="text", text=report)]


async def analyze_scenario_flow_handler(arguments: dict) -> list[types.TextContent]:
    """シナリオフローを解析"""
    project_name = arguments["project_name"]
    scenario_file = arguments["scenario_file"]

    if not scenario_file.endswith(".ks"):
        scenario_file += ".ks"

    scenario_path = PROJECTS_DIR / project_name / "data" / "scenario" / scenario_file

    if not scenario_path.exists():
        return [types.TextContent(type="text", text=f"シナリオファイル '{scenario_file}' が見つかりません")]

    content = scenario_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    import re

    # ラベルとその遷移を解析
    labels = {}  # {label_name: {"line": line_num, "jumps_to": [], "choices": []}}
    current_label = None

    for i, line in enumerate(lines, 1):
        line_strip = line.strip()

        # コメントをスキップ
        if line_strip.startswith(";") or line_strip.startswith("//"):
            continue

        # ラベル定義
        if line_strip.startswith("*"):
            label_name = line_strip[1:].strip()
            if label_name:
                current_label = label_name
                labels[label_name] = {
                    "line": i,
                    "jumps_to": [],
                    "choices": [],
                    "calls": []
                }

        if current_label:
            # ジャンプ
            if "[jump" in line_strip or "@jump" in line_strip:
                match = re.search(r'target=["\']?\*?([^"\'\s\]]+)', line_strip)
                if match:
                    target = match.group(1)
                    labels[current_label]["jumps_to"].append(target)

            # コール
            if "[call" in line_strip or "@call" in line_strip:
                match = re.search(r'target=["\']?\*?([^"\'\s\]]+)', line_strip)
                if match:
                    target = match.group(1)
                    labels[current_label]["calls"].append(target)

            # 選択肢
            if "[link" in line_strip or "[glink" in line_strip:
                match = re.search(r'target=["\']?\*?([^"\'\s\]]+)', line_strip)
                if match:
                    target = match.group(1)
                    text_match = re.search(r'text=["\']([^"\']+)["\']', line_strip)
                    choice_text = text_match.group(1) if text_match else target
                    labels[current_label]["choices"].append({
                        "text": choice_text,
                        "target": target
                    })

    # フロー図生成
    report = f"""🔀 シナリオフロー解析: {scenario_file}
{'=' * 60}

【ラベル一覧】 ({len(labels)}個)
"""

    for label_name, info in sorted(labels.items(), key=lambda x: x[1]["line"]):
        report += f"\n*{label_name} (行 {info['line']})\n"

        if info["jumps_to"]:
            report += f"  → ジャンプ: " + ", ".join(f"*{t}" for t in info["jumps_to"]) + "\n"

        if info["calls"]:
            report += f"  ⇒ コール: " + ", ".join(f"*{t}" for t in info["calls"]) + "\n"

        if info["choices"]:
            report += f"  ◇ 選択肢:\n"
            for choice in info["choices"]:
                report += f"    - [{choice['text']}] → *{choice['target']}\n"

    # Mermaid形式のフローチャート
    report += f"\n【Mermaidフローチャート】\n```mermaid\ngraph TD\n"

    for label_name, info in labels.items():
        safe_label = label_name.replace("-", "_").replace(" ", "_")

        for target in info["jumps_to"]:
            safe_target = target.replace("-", "_").replace(" ", "_")
            report += f"  {safe_label}[{label_name}] --> {safe_target}[{target}]\n"

        for choice in info["choices"]:
            safe_target = choice["target"].replace("-", "_").replace(" ", "_")
            report += f"  {safe_label}[{label_name}] -->|{choice['text']}| {safe_target}[{choice['target']}]\n"

        for target in info["calls"]:
            safe_target = target.replace("-", "_").replace(" ", "_")
            report += f"  {safe_label}[{label_name}] -.->|call| {safe_target}[{target}]\n"

    report += "```\n"

    return [types.TextContent(type="text", text=report)]


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