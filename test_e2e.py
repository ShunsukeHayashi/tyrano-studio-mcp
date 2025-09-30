#!/usr/bin/env python3
"""
End-to-End Test for TyranoStudio MCP Server
"""

import sys
import asyncio
from pathlib import Path

# サーバーのインポート
sys.path.insert(0, str(Path(__file__).parent))
from server import (
    list_projects_handler,
    create_project_handler,
    write_scenario_handler,
    read_scenario_handler,
    validate_scenario_handler,
    add_image_handler,
    add_audio_handler,
    list_audio_handler,
    generate_scenario_template_handler,
    delete_project_handler,
    PROJECTS_DIR
)

# テスト用プロジェクト名
TEST_PROJECT = "e2e_test_project"


async def test_project_management():
    """プロジェクト管理のテスト"""
    print("=" * 60)
    print("TEST: Project Management")
    print("=" * 60)

    # 1. プロジェクト一覧（初期状態）
    print("\n[1] Initial project list...")
    result = await list_projects_handler()
    print(result[0].text)

    # 2. 新規プロジェクト作成
    print(f"\n[2] Creating project '{TEST_PROJECT}'...")
    result = await create_project_handler({
        "project_name": TEST_PROJECT,
        "template": "tyranoscript_ja"
    })
    print(result[0].text)

    # 3. プロジェクト一覧（作成後）
    print("\n[3] Project list after creation...")
    result = await list_projects_handler()
    print(result[0].text)

    # プロジェクトが作成されたか確認
    project_path = PROJECTS_DIR / TEST_PROJECT
    assert project_path.exists(), f"Project directory not created: {project_path}"
    print(f"✅ Project directory exists: {project_path}")

    return True


async def test_scenario_operations():
    """シナリオファイル操作のテスト"""
    print("\n" + "=" * 60)
    print("TEST: Scenario Operations")
    print("=" * 60)

    # 1. シナリオファイル書き込み
    print("\n[1] Writing test scenario...")
    test_content = """*start

[cm]
[bg storage="room.jpg"]

これはテストシナリオです。[p]

[jump target="*next"]
[s]

*next
次のシーンです。[p]
[s]
"""
    result = await write_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "test_scene.ks",
        "content": test_content
    })
    print(result[0].text)

    # 2. シナリオファイル読み込み
    print("\n[2] Reading test scenario...")
    result = await read_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "test_scene.ks"
    })
    print("Content (first 100 chars):", result[0].text[:100])
    assert "これはテストシナリオです" in result[0].text
    print("✅ Scenario content verified")

    # 3. シナリオ検証
    print("\n[3] Validating scenario...")
    result = await validate_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "test_scene.ks"
    })
    print(result[0].text)

    return True


async def test_template_generation():
    """テンプレート生成のテスト"""
    print("\n" + "=" * 60)
    print("TEST: Template Generation")
    print("=" * 60)

    templates = [
        ("basic_scene", {
            "label": "scene1",
            "bg": "bg1.jpg",
            "text": "テストテキスト",
            "next_label": "*scene2"
        }),
        ("character_intro", {
            "label": "intro",
            "chara_name": "hero",
            "chara_jname": "主人公",
            "dialogue": "よろしく！"
        }),
        ("choice_branch", {
            "label": "choice1",
            "prompt_text": "どうする？",
            "choice1_text": "進む",
            "choice2_text": "戻る"
        }),
        ("dialogue", {
            "label": "talk",
            "chara1_name": "太郎",
            "chara2_name": "花子"
        }),
        ("title_screen", {
            "label": "title",
            "start_label": "game_start"
        })
    ]

    for i, (template_type, params) in enumerate(templates, 1):
        print(f"\n[{i}] Generating '{template_type}' template...")
        result = await generate_scenario_template_handler({
            "project_name": TEST_PROJECT,
            "scenario_file": f"template_{template_type}.ks",
            "template_type": template_type,
            "params": params
        })
        print(result[0].text)

        # ファイルが生成されたか確認
        scenario_path = PROJECTS_DIR / TEST_PROJECT / "data" / "scenario" / f"template_{template_type}.ks"
        assert scenario_path.exists(), f"Template file not created: {scenario_path}"
        print(f"✅ Template file created: template_{template_type}.ks")

    return True


async def test_validation_advanced():
    """高度な検証機能のテスト"""
    print("\n" + "=" * 60)
    print("TEST: Advanced Validation")
    print("=" * 60)

    # エラーのあるシナリオを作成
    print("\n[1] Creating scenario with errors...")
    error_scenario = """*start

[if exp="f.flag==1"]
テストです[p]
; [endif]が抜けている

[jump target="*undefined_label"]

[chara_show name="undefined_character"]

[bg storage="nonexistent.jpg"]

[s]
"""
    result = await write_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "error_test.ks",
        "content": error_scenario
    })
    print(result[0].text)

    # 検証実行
    print("\n[2] Validating scenario with errors...")
    result = await validate_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "error_test.ks"
    })
    print(result[0].text)

    # エラーが検出されることを確認
    assert "エラー" in result[0].text or "警告" in result[0].text
    print("✅ Validation detected errors as expected")

    return True


async def test_audio_management():
    """音声ファイル管理のテスト"""
    print("\n" + "=" * 60)
    print("TEST: Audio Management")
    print("=" * 60)

    # 1. ダミー音声ファイルを作成
    print("\n[1] Creating dummy audio files...")
    bgm_dir = PROJECTS_DIR / TEST_PROJECT / "data" / "bgm"
    sound_dir = PROJECTS_DIR / TEST_PROJECT / "data" / "sound"
    bgm_dir.mkdir(parents=True, exist_ok=True)
    sound_dir.mkdir(parents=True, exist_ok=True)

    # ダミーファイル作成
    (bgm_dir / "test_bgm.ogg").write_text("dummy bgm")
    (sound_dir / "test_se.ogg").write_text("dummy se")
    print("✅ Dummy audio files created")

    # 2. 音声ファイル一覧
    print("\n[2] Listing audio files...")
    result = await list_audio_handler({
        "project_name": TEST_PROJECT,
        "audio_type": "all"
    })
    print(result[0].text)

    assert "test_bgm.ogg" in result[0].text
    assert "test_se.ogg" in result[0].text
    print("✅ Audio files listed correctly")

    # 3. BGMのみ一覧
    print("\n[3] Listing BGM only...")
    result = await list_audio_handler({
        "project_name": TEST_PROJECT,
        "audio_type": "bgm"
    })
    print(result[0].text)

    return True


async def test_resource_validation():
    """リソース検証のテスト"""
    print("\n" + "=" * 60)
    print("TEST: Resource Validation")
    print("=" * 60)

    # リソースを参照するシナリオを作成
    print("\n[1] Creating scenario with resource references...")
    resource_scenario = """*start

[bg storage="room.jpg"]
[playbgm storage="test_bgm.ogg"]
[playse storage="test_se.ogg"]

テキスト[p]

[s]
"""
    result = await write_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "resource_test.ks",
        "content": resource_scenario
    })
    print(result[0].text)

    # 検証実行
    print("\n[2] Validating resource references...")
    result = await validate_scenario_handler({
        "project_name": TEST_PROJECT,
        "scenario_file": "resource_test.ks"
    })
    print(result[0].text)

    # BGMとSEは存在するので警告なし、room.jpgは警告あり
    assert "test_bgm.ogg" not in result[0].text or "見つかりません" not in result[0].text
    print("✅ Resource validation working")

    return True


async def cleanup():
    """テストプロジェクトのクリーンアップ"""
    print("\n" + "=" * 60)
    print("CLEANUP")
    print("=" * 60)

    print(f"\n[*] Deleting test project '{TEST_PROJECT}'...")
    result = await delete_project_handler({
        "project_name": TEST_PROJECT
    })
    print(result[0].text)

    # プロジェクトが削除されたか確認
    project_path = PROJECTS_DIR / TEST_PROJECT
    assert not project_path.exists(), f"Project directory not deleted: {project_path}"
    print(f"✅ Project deleted successfully")


async def run_all_tests():
    """すべてのテストを実行"""
    print("\n" + "=" * 60)
    print("TYRANO STUDIO MCP SERVER - E2E TEST")
    print("=" * 60)

    tests = [
        ("Project Management", test_project_management),
        ("Scenario Operations", test_scenario_operations),
        ("Template Generation", test_template_generation),
        ("Advanced Validation", test_validation_advanced),
        ("Audio Management", test_audio_management),
        ("Resource Validation", test_resource_validation),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            await test_func()
            passed += 1
            print(f"\n✅ {test_name}: PASSED")
        except Exception as e:
            failed += 1
            print(f"\n❌ {test_name}: FAILED")
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

    # クリーンアップ
    try:
        await cleanup()
    except Exception as e:
        print(f"\n⚠️  Cleanup failed: {e}")

    # 結果サマリー
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Total: {passed + failed}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print("=" * 60)

    if failed == 0:
        print("\n🎉 ALL TESTS PASSED!")
        return 0
    else:
        print(f"\n❌ {failed} TEST(S) FAILED")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(run_all_tests())
    sys.exit(exit_code)