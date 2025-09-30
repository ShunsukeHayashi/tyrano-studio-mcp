#!/usr/bin/env python3
"""
デモプロジェクト自動生成スクリプト

このスクリプトは、TyranoStudio MCP Serverの機能を実演するための
完全なデモプロジェクトを自動生成します。
"""

import sys
import asyncio
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from server import (
    create_project_handler,
    write_scenario_handler,
    git_init_handler,
    git_commit_handler,
    analyze_project_handler,
    analyze_scenario_flow_handler,
    PROJECTS_DIR
)

PROJECT_NAME = "demo_adventure"


async def create_demo_project():
    """デモプロジェクトを作成"""
    print("=" * 70)
    print("TyranoStudio MCP Server - Demo Project Generator")
    print("=" * 70)

    # 1. プロジェクト作成
    print("\n[1/8] Creating project...")
    result = await create_project_handler({
        "project_name": PROJECT_NAME,
        "template": "tyranoscript_ja"
    })
    print(f"  ✅ {result[0].text}")

    # 2. Git初期化
    print("\n[2/8] Initializing Git...")
    result = await git_init_handler({
        "project_name": PROJECT_NAME
    })
    print(f"  ✅ {result[0].text}")

    # 3. first.ksを上書き（エントリーポイント）
    print("\n[3/8] Creating first.ks...")
    first_ks = """*start

[title name="冒険者の物語"]

[stop_keyconfig]

@call storage="tyrano.ks"

[layopt layer="message" visible=false]
[hidemenubutton]

@jump storage="title.ks"
[s]
"""
    await write_scenario_handler({
        "project_name": PROJECT_NAME,
        "scenario_file": "first.ks",
        "content": first_ks
    })
    print("  ✅ Entry point created")

    # 4. タイトル画面
    print("\n[4/8] Creating title screen...")
    title_ks = """*title

[cm]
[clearfix]
[hidemenubutton]
[bg storage="room.jpg" time="100"]

[ptext layer="1" page="fore" x="400" y="200" size="50" color="white" text="冒険者の物語"]
[ptext layer="1" page="fore" x="450" y="280" size="25" color="white" text="～ 不思議な森の謎 ～"]

[glink text="はじめから" target="*start_game" size="20" width="300" x="490" y="400"]
[glink text="つづきから" role="load" size="20" width="300" x="490" y="460"]
[s]

*start_game
[cm]
[freeimage layer="1"]
@jump storage="chapter1.ks"
[s]
"""
    await write_scenario_handler({
        "project_name": PROJECT_NAME,
        "scenario_file": "title.ks",
        "content": title_ks
    })
    print("  ✅ Title screen created")

    # 5. 第1章
    print("\n[5/8] Creating chapter 1...")
    chapter1_ks = """*chapter1_start

[cm]
[bg storage="room.jpg" time="1000"]
[showmenubutton]

[position layer="message0" left=160 top=500 width=1000 height=200 page=fore visible=true]
[position layer=message0 page=fore margint="45" marginl="50" marginr="70" marginb="60"]
@layopt layer=message0 visible=true

[ptext name="chara_name_area" layer="message0" color="white" size=28 bold=true x=180 y=510]
[chara_config ptext="chara_name_area"]

# キャラクター定義
[chara_new name="hero" storage="chara/akane/normal.png" jname="勇者"]

目が覚めると、見知らぬ部屋にいた。[p]

ここは...どこだ？[p]

[chara_show name="hero"]

#勇者
最後に覚えているのは、森を歩いていたことだけだ。[p]

どうやら誰かの家のようだ。[p]

外に出てみよう。[p]

[bg storage="rouka.jpg" time="1000"]

廊下に出ると、不思議な雰囲気が漂っていた。[p]

#勇者
この先に何があるんだろう...？[p]

[jump target="*choice1"]
[s]

*choice1

[cm]

さて、どうしよう？[p]

[glink text="森の奥へ進む" target="*forest_path" size="20" width="400" x="440" y="250"]
[glink text="川沿いを探索する" target="*river_path" size="20" width="400" x="440" y="320"]
[s]

*forest_path
[cm]
森の奥へと足を進めた。[p]

木々が深く生い茂り、薄暗い道が続いている。[p]

#勇者
何か...音がする？[p]

[jump storage="chapter2.ks" target="*forest_route"]
[s]

*river_path
[cm]
川沿いの道を選んだ。[p]

清らかな水の流れる音が心地よい。[p]

#勇者
この川、どこに続いているんだろう...？[p]

[jump storage="chapter2.ks" target="*river_route"]
[s]
"""
    await write_scenario_handler({
        "project_name": PROJECT_NAME,
        "scenario_file": "chapter1.ks",
        "content": chapter1_ks
    })
    print("  ✅ Chapter 1 created")

    # 6. 第2章
    print("\n[6/8] Creating chapter 2...")
    chapter2_ks = """*forest_route

[cm]
[bg storage="room.jpg"]

森の奥で、不思議な光を見つけた。[p]

#勇者
あれは...何だ？[p]

光に近づくと、突然景色が変わった。[p]

[jump target="*ending"]
[s]

*river_route

[cm]
[bg storage="rouka.jpg"]

川を遡っていくと、滝が見えてきた。[p]

#勇者
綺麗な滝だな...。[p]

滝の裏に、何か見える。[p]

[jump target="*ending"]
[s]

*ending

[cm]
[bg storage="room.jpg"]

そこには、不思議な扉があった。[p]

#勇者
これが...この世界の謎の鍵なのか？[p]

扉を開けると、光に包まれた。[p]

こうして、私の冒険は始まったのだった。[p]

[cm]
[ptext layer="1" page="fore" x="500" y="300" size="40" color="white" text="To Be Continued..."]

[l]

@jump storage="title.ks"
[s]
"""
    await write_scenario_handler({
        "project_name": PROJECT_NAME,
        "scenario_file": "chapter2.ks",
        "content": chapter2_ks
    })
    print("  ✅ Chapter 2 created")

    # 7. コミット
    print("\n[7/8] Committing changes...")
    result = await git_commit_handler({
        "project_name": PROJECT_NAME,
        "message": "Initial demo project: Adventure game"
    })
    print(f"  ✅ Committed")

    # 8. 分析
    print("\n[8/8] Analyzing project...")
    result = await analyze_project_handler({
        "project_name": PROJECT_NAME
    })
    print("\n" + result[0].text)

    # フロー解析
    print("\n" + "=" * 70)
    print("Scenario Flow Analysis")
    print("=" * 70)
    result = await analyze_scenario_flow_handler({
        "project_name": PROJECT_NAME,
        "scenario_file": "chapter1.ks"
    })
    print("\n" + result[0].text)

    # 完了
    print("\n" + "=" * 70)
    print("✅ Demo project created successfully!")
    print("=" * 70)
    print(f"\nProject location: {PROJECTS_DIR / PROJECT_NAME}")
    print("\nNext steps:")
    print("1. Open TyranoStudio")
    print(f"2. Load project: myprojects/{PROJECT_NAME}")
    print("3. Preview and play!")
    print("\nYou can also:")
    print("- Modify scenarios with MCP tools")
    print("- Add more resources")
    print("- Validate and optimize")
    print("=" * 70)


if __name__ == "__main__":
    asyncio.run(create_demo_project())