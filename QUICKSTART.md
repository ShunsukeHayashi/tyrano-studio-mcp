# クイックスタートガイド

TyranoStudio MCP Serverを5分で使い始めるためのガイドです。

## 📋 前提条件

- Python 3.11以上
- TyranoStudio（インストール済み）
- Claude Code（推奨）

## ⚡ インストール

### 1. リポジトリをクローン

```bash
git clone https://github.com/ShunsukeHayashi/tyrano-studio-mcp.git
cd tyrano-studio-mcp
```

### 2. 依存関係をインストール

```bash
pip install -r requirements.txt
```

### 3. Claude Codeに設定を追加

`~/.claude/mcp_config.json` に以下を追加：

```json
{
  "mcpServers": {
    "tyrano-studio": {
      "command": "python3.11",
      "args": ["/path/to/tyrano-studio-mcp/server.py"],
      "description": "TyranoStudio project management"
    }
  }
}
```

**注意**: `/path/to/`は実際のパスに置き換えてください。

### 4. 動作確認

```bash
python3.11 test_e2e.py
```

すべてのテストがパスすれば成功です！

## 🎮 最初のプロジェクト

### ステップ1: プロジェクト作成

Claude Codeで以下のように依頼：

```
Create a new TyranoScript project called "my_first_game"
```

または直接MCPツールを使用：

```python
create_project({
  "project_name": "my_first_game",
  "template": "tyranoscript_ja"
})
```

### ステップ2: シナリオ作成

テンプレートを使って素早く作成：

```
Generate a basic scene template for my_first_game as scene1.ks
```

または：

```python
generate_scenario_template({
  "project_name": "my_first_game",
  "scenario_file": "scene1.ks",
  "template_type": "basic_scene",
  "params": {
    "label": "start",
    "bg": "room.jpg",
    "text": "こんにちは、世界！"
  }
})
```

### ステップ3: 検証

シナリオをチェック：

```
Validate the scenario in my_first_game scene1.ks
```

### ステップ4: TyranoStudioで開く

```bash
open /Users/shunsuke/TyranoStudio_mac_std_v603/TyranoStudio.app
```

1. TyranoStudioを起動
2. 「プロジェクトを開く」
3. `myprojects/my_first_game`を選択
4. プレビューで確認

## 🚀 便利なワークフロー

### キャラクターを追加

```python
generate_scenario_template({
  "project_name": "my_first_game",
  "scenario_file": "character_intro.ks",
  "template_type": "character_intro",
  "params": {
    "chara_name": "hero",
    "chara_jname": "主人公",
    "dialogue": "よろしくお願いします！"
  }
})
```

### 選択肢を追加

```python
generate_scenario_template({
  "project_name": "my_first_game",
  "scenario_file": "choices.ks",
  "template_type": "choice_branch",
  "params": {
    "choice1_text": "はい",
    "choice2_text": "いいえ"
  }
})
```

### プロジェクトを分析

```
Analyze my_first_game project
```

結果：
- 統計情報
- プレイ時間推定
- リソース使用状況

## 📊 よく使う機能

### 1. シナリオ検証

```bash
# エラーチェック
validate_scenario("my_first_game", "scene1.ks")
```

**チェック項目**:
- タグの対応
- ラベル存在確認
- リソースファイル確認
- キャラクター定義

### 2. プロジェクト分析

```bash
analyze_project("my_first_game")
```

**取得情報**:
- 文字数、行数
- プレイ時間推定
- リソース統計

### 3. Git管理

```bash
# 初期化
git_init("my_first_game")

# コミット
git_commit("my_first_game", "Initial commit")

# 状態確認
git_status("my_first_game")
```

### 4. リソース最適化

```bash
optimize_resources("my_first_game")
```

**検出内容**:
- 未使用ファイル
- 存在しない参照
- 削減可能サイズ

## 💡 Tips

### 効率的なシナリオ作成

1. **テンプレートを活用**
   - 5種類のテンプレートで素早く作成
   - パラメータでカスタマイズ

2. **検証を頻繁に**
   - 書いたらすぐ検証
   - エラーを早期発見

3. **こまめにコミット**
   - 機能単位でコミット
   - バージョン管理で安心

### トラブルシューティング

#### エラー: "Gitリポジトリが初期化されていません"
```bash
git_init("project_name")
```

#### エラー: "シナリオファイルが見つかりません"
```bash
# ファイル一覧を確認
list_project_files("project_name", "data/scenario")
```

#### 警告: "未定義キャラクター"
```bash
# chara_newで定義が必要
[chara_new name="character" storage="character.png"]
```

## 📚 次に学ぶこと

1. **[FEATURES.md](FEATURES.md)** - 全機能詳細
2. **[Examples](examples/)** - デモプロジェクト
3. **[CONTRIBUTING.md](CONTRIBUTING.md)** - 開発に参加

## ❓ FAQ

### Q: TyranoStudioのパスが違う場合は？

A: `server.py`の`TYRANO_BASE`変数を編集：

```python
TYRANO_BASE = Path("/your/path/to/TyranoStudio")
```

### Q: 複数のプロジェクトを管理できる？

A: はい、`myprojects/`配下に複数作成可能です。

### Q: エクスポート機能はある？

A: 現在はTyranoStudio標準機能をご利用ください。

## 🔗 リソース

- [TyranoScript公式](https://tyrano.jp/)
- [タグリファレンス](https://tyrano.jp/tag/)
- [GitHub Issues](https://github.com/ShunsukeHayashi/tyrano-studio-mcp/issues)

## 🎉 完了！

これでTyranoStudio MCP Serverを使い始める準備が整いました。
素晴らしいゲームを作ってください！