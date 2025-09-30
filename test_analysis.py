#!/usr/bin/env python3
"""
Test script for analysis features
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from server import (
    create_project_handler,
    write_scenario_handler,
    analyze_project_handler,
    analyze_scenario_flow_handler,
    delete_project_handler,
    PROJECTS_DIR
)

TEST_PROJECT = "analysis_test"


async def test_analysis():
    """分析機能のテスト"""
    print("=" * 60)
    print("Analysis Features Test")
    print("=" * 60)

    # プロジェクト作成
    print("\n[1] Creating test project...")
    await create_project_handler({
        "project_name": TEST_PROJECT,
        "template": "tyranoscript_ja"
    })

    # 複雑なシナリオを作成
    print("\n[2] Creating test scenarios...")

    # メインシナリオ
    main_scenario = """*start

[cm]
[bg storage="room.jpg"]

[chara_new name="hero" storage="hero.png" jname="主人公"]
[chara_new name="friend" storage="friend.png" jname="友達"]

これはテストゲームです。[p]
物語が始まります。[p]

[jump target="*choice1"]
[s]

*choice1

どうしますか？[p]

[glink text="友達に会いに行く" target="*meet_friend" size=20 width=400 x=50 y=200]
[glink text="一人で過ごす" target="*alone" size=20 width=400 x=50 y=260]
[s]

*meet_friend
[chara_show name="friend"]
#友達
やあ！元気だった？[p]

#主人公
うん、元気だよ！[p]

[jump target="*end"]

*alone
一人の時間も大切だ。[p]
ゆっくり過ごそう。[p]

[jump target="*end"]

*end
こうして一日が終わった。[p]
おしまい。[p]

[s]
"""

    await write_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "main.ks",
        "content": main_scenario
    })

    # サブシナリオ
    sub_scenario = """*sub_start

これはサブシナリオです。[p]

[call target="*sub_routine"]

サブルーチンから戻りました。[p]

[return]

*sub_routine
サブルーチン内の処理。[p]
[return]
"""

    await write_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "sub.ks",
        "content": sub_scenario
    })

    # ダミーリソースを追加
    print("\n[3] Creating dummy resources...")
    project_path = PROJECTS_DIR / TEST_PROJECT

    # 画像
    (project_path / "data" / "bgimage" / "room.jpg").write_text("dummy")
    (project_path / "data" / "fgimage" / "hero.png").write_text("dummy")
    (project_path / "data" / "fgimage" / "friend.png").write_text("dummy")

    # 音声
    (project_path / "data" / "bgm" / "theme.ogg").write_text("dummy")
    (project_path / "data" / "sound" / "click.ogg").write_text("dummy")

    # プロジェクト分析
    print("\n[4] Analyzing project...")
    print("=" * 60)
    result = await analyze_project_handler({
        "project_name": TEST_PROJECT
    })
    print(result[0].text)

    # シナリオフロー分析
    print("\n[5] Analyzing scenario flow...")
    print("=" * 60)
    result = await analyze_scenario_flow_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "main.ks"
    })
    print(result[0].text)

    # クリーンアップ
    print("\n[6] Cleaning up...")
    await delete_project_handler({
        "project_name": TEST_PROJECT
    })
    print("✅ Test completed")


if __name__ == "__main__":
    asyncio.run(test_analysis())