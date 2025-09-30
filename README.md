# TyranoStudio MCP Server

TyranoStudio（ティラノスタジオ）のプロジェクト管理とTyranoScriptのゲーム開発を支援するMCPサーバーです。

## 📁 対象ディレクトリ構造

```
/Users/shunsuke/TyranoStudio_mac_std_v603/
├── myprojects/          # ゲームプロジェクト格納ディレクトリ
│   └── [プロジェクト名]/
│       └── data/
│           ├── scenario/    # シナリオファイル(.ks)
│           ├── fgimage/     # 前景画像（キャラクター等）
│           ├── bgimage/     # 背景画像
│           ├── bgm/         # BGM
│           ├── sound/       # 効果音
│           ├── video/       # 動画
│           ├── image/       # その他画像
│           ├── system/      # システムファイル(Config.tjs等)
│           └── others/      # その他
├── system_master/       # テンプレート
│   ├── tyranoscript_ja/ # 日本語テンプレート
│   └── tyranoscript_en/ # 英語テンプレート
├── export/              # エクスポート先
└── dlc/                 # プラグイン

```

## 🛠️ 機能（ツール一覧）

### 1. プロジェクト管理

#### `list_projects`
- 説明: 作成済みプロジェクトの一覧を取得
- パラメータ: なし
- 例:
```json
{}
```

#### `create_project`
- 説明: 新しいプロジェクトを作成
- パラメータ:
  - `project_name` (必須): プロジェクト名
  - `template` (オプション): テンプレート種類 (`tyranoscript_ja` または `tyranoscript_en`)
- 例:
```json
{
  "project_name": "my_game",
  "template": "tyranoscript_ja"
}
```

#### `delete_project`
- 説明: プロジェクトを削除
- パラメータ:
  - `project_name` (必須): プロジェクト名
- 例:
```json
{
  "project_name": "my_game"
}
```

#### `list_project_files`
- 説明: プロジェクト内のファイル・ディレクトリ一覧
- パラメータ:
  - `project_name` (必須): プロジェクト名
  - `path` (オプション): 相対パス（省略時はルート）
- 例:
```json
{
  "project_name": "my_game",
  "path": "data/scenario"
}
```

### 2. シナリオファイル操作

#### `read_scenario`
- 説明: シナリオファイル(.ks)を読み込む
- パラメータ:
  - `project_name` (必須): プロジェクト名
  - `scenario_file` (必須): シナリオファイル名
- 例:
```json
{
  "project_name": "my_game",
  "scenario_file": "scene1.ks"
}
```

#### `write_scenario`
- 説明: シナリオファイル(.ks)を書き込む
- パラメータ:
  - `project_name` (必須): プロジェクト名
  - `scenario_file` (必須): シナリオファイル名
  - `content` (必須): 書き込む内容
- 例:
```json
{
  "project_name": "my_game",
  "scenario_file": "scene1.ks",
  "content": "[bg storage=\"room.jpg\"]\nこんにちは[p]"
}
```

#### `validate_scenario`
- 説明: シナリオファイルの構文チェック
- パラメータ:
  - `project_name` (必須): プロジェクト名
  - `scenario_file` (必須): シナリオファイル名
- 例:
```json
{
  "project_name": "my_game",
  "scenario_file": "scene1.ks"
}
```

### 3. 設定ファイル操作

#### `read_config`
- 説明: Config.tjsを読み込む
- パラメータ:
  - `project_name` (必須): プロジェクト名
- 例:
```json
{
  "project_name": "my_game"
}
```

#### `write_config`
- 説明: Config.tjsを書き込む
- パラメータ:
  - `project_name` (必須): プロジェクト名
  - `content` (必須): 書き込む内容
- 例:
```json
{
  "project_name": "my_game",
  "content": "..."
}
```

### 4. リソース管理

#### `add_image`
- 説明: プロジェクトに画像を追加
- パラメータ:
  - `project_name` (必須): プロジェクト名
  - `source_path` (必須): コピー元の画像パス
  - `dest_category` (必須): 配置先カテゴリ（`fgimage`, `bgimage`, `image`, `system`等）
  - `dest_filename` (オプション): 配置先ファイル名
- 例:
```json
{
  "project_name": "my_game",
  "source_path": "/Users/shunsuke/Downloads/character.png",
  "dest_category": "fgimage",
  "dest_filename": "hero.png"
}
```

### 5. TyranoScriptリファレンス

#### `get_tyranoscript_reference`
- 説明: TyranoScriptのタグリファレンスを取得
- パラメータ:
  - `category` (オプション): カテゴリ（`text`, `character`, `background`, `choice`, `variable`, `audio`, `all`）
- 例:
```json
{
  "category": "character"
}
```

## 📝 TyranoScriptの基本タグ

### テキスト・メッセージ系
- `[l]` - クリック待ち
- `[p]` - クリック待ち＆改ページ
- `[r]` - 改行
- `[cm]` - メッセージクリア

### キャラクター系
- `[chara_new name="キャラ名" storage="画像ファイル"]` - キャラクター定義
- `[chara_show name="キャラ名"]` - キャラクター表示
- `[chara_hide name="キャラ名"]` - キャラクター非表示
- `[chara_mod name="キャラ名" storage="画像ファイル"]` - 表情変更

### 背景・画像系
- `[bg storage="画像ファイル"]` - 背景変更
- `[image layer="レイヤ番号" storage="画像ファイル"]` - 画像表示

### 選択肢・ジャンプ系
- `[link target="ラベル名"]テキスト[endlink]` - 選択肢
- `[glink target="ラベル名" text="選択肢テキスト"]` - グラフィカル選択肢
- `[jump target="ラベル名"]` - ジャンプ
- `[s]` - 停止
- `*ラベル名` - ラベル定義

### 音声系
- `[playbgm storage="音楽ファイル"]` - BGM再生
- `[playse storage="効果音ファイル"]` - 効果音再生

## 🚀 セットアップ

### 1. 依存パッケージのインストール

```bash
pip install mcp
```

### 2. Claude Codeへの設定追加

`~/.claude/mcp_config.json` に以下を追加:

```json
{
  "mcpServers": {
    "tyrano-studio": {
      "command": "python3",
      "args": ["/Users/shunsuke/tyrano_studio_mcp_server.py"],
      "description": "TyranoStudio project management"
    }
  }
}
```

### 3. サーバー起動確認

```bash
python3 /Users/shunsuke/tyrano_studio_mcp_server.py
```

## 💡 使用例

### 新しいゲームプロジェクトを作成

```json
{
  "tool": "create_project",
  "arguments": {
    "project_name": "my_visual_novel",
    "template": "tyranoscript_ja"
  }
}
```

### シンプルなシナリオを作成

```json
{
  "tool": "write_scenario",
  "arguments": {
    "project_name": "my_visual_novel",
    "scenario_file": "scene1.ks",
    "content": "*start\n\n[bg storage=\"room.jpg\"]\n\nこんにちは、世界！[p]\n\nこれはTyranoScriptで作られたゲームです。[p]\n\n[s]"
  }
}
```

### キャラクターを追加

```json
{
  "tool": "add_image",
  "arguments": {
    "project_name": "my_visual_novel",
    "source_path": "/path/to/character.png",
    "dest_category": "fgimage"
  }
}
```

### シナリオの構文チェック

```json
{
  "tool": "validate_scenario",
  "arguments": {
    "project_name": "my_visual_novel",
    "scenario_file": "scene1.ks"
  }
}
```

## 📖 参考リンク

- [TyranoScript公式サイト](https://tyrano.jp/)
- [タグリファレンス](https://tyrano.jp/tag/)
- [TyranoBuilder（GUI開発ツール）](https://tyranobuilder.jp/)

## 🎮 TyranoStudioの起動

```bash
open /Users/shunsuke/TyranoStudio_mac_std_v603/TyranoStudio.app
```

作成したプロジェクトは `myprojects/` ディレクトリに保存され、TyranoStudioから直接開いてプレビュー・編集できます。

## 🔧 トラブルシューティング

### プロジェクトが見つからない
- `myprojects/` ディレクトリを確認
- プロジェクト名のスペルミスを確認

### 画像が表示されない
- 画像ファイルが適切なディレクトリに配置されているか確認
- ファイル名の大文字小文字を確認（特にmacOS）

### シナリオの構文エラー
- `validate_scenario` ツールで検証
- タグの開始/終了が正しく対応しているか確認

## 📄 ライセンス

このMCPサーバーはTyranoStudioの操作を支援するものであり、TyranoScript/TyranoStudio本体のライセンスに従います。