# インストールガイド

TyranoStudio MCP Serverの詳細なインストール手順です。

## 📋 システム要件

### 必須
- **Python**: 3.11以上
- **OS**: macOS, Linux, Windows
- **TyranoStudio**: v6.0以上推奨

### 推奨
- **Claude Code**: MCPクライアント
- **Git**: バージョン管理機能使用時
- **ディスク空き容量**: 100MB以上

## 🚀 インストール方法

### 方法1: GitHubからクローン（推奨）

#### ステップ1: リポジトリをクローン

```bash
cd ~/
git clone https://github.com/ShunsukeHayashi/tyrano-studio-mcp.git
cd tyrano-studio-mcp
```

#### ステップ2: 依存関係をインストール

```bash
# Python 3.11を使用
pip install -r requirements.txt

# または特定のPythonバージョンを指定
pip3.11 install -r requirements.txt
```

#### ステップ3: インストール確認

```bash
python3.11 -c "import mcp; print('MCP module OK')"
```

成功すれば「MCP module OK」と表示されます。

#### ステップ4: テスト実行

```bash
python3.11 test_e2e.py
```

すべてのテストがパスすれば成功です！

### 方法2: 手動ダウンロード

1. https://github.com/ShunsukeHayashi/tyrano-studio-mcp
2. 「Code」→「Download ZIP」
3. ZIPを解凍
4. ターミナルで解凍先に移動
5. 上記のステップ2以降を実行

## 🔧 Claude Code設定

### ステップ1: 設定ファイルを開く

```bash
# macOS/Linux
nano ~/.claude/mcp_config.json

# または
open -a "TextEdit" ~/.claude/mcp_config.json
```

### ステップ2: サーバー設定を追加

```json
{
  "mcpServers": {
    "tyrano-studio": {
      "command": "python3.11",
      "args": ["/Users/YOUR_USERNAME/tyrano-studio-mcp/server.py"],
      "description": "TyranoStudio project management and development"
    }
  }
}
```

**重要**: `/Users/YOUR_USERNAME/` を実際のパスに置き換えてください。

### ステップ3: パスの確認

```bash
# 現在のディレクトリの絶対パスを取得
pwd

# 例: /Users/shunsuke/tyrano-studio-mcp
```

このパスを `args` の値として使用します。

### ステップ4: Claude Codeを再起動

設定を反映させるため、Claude Codeを再起動してください。

## 🎮 TyranoStudioパス設定

### デフォルトパス

サーバーはデフォルトで以下のパスを使用します：

```
/Users/shunsuke/TyranoStudio_mac_std_v603
```

### カスタムパスの設定

TyranoStudioが別の場所にある場合：

#### ステップ1: server.pyを開く

```bash
nano ~/tyrano-studio-mcp/server.py
```

#### ステップ2: TYRANO_BASEを編集

14行目付近を編集：

```python
# 変更前
TYRANO_BASE = Path("/Users/shunsuke/TyranoStudio_mac_std_v603")

# 変更後（例）
TYRANO_BASE = Path("/Applications/TyranoStudio/TyranoStudio_mac_std_v603")
```

#### ステップ3: 保存して終了

```bash
# nanoの場合
Ctrl + X → Y → Enter
```

## ✅ 動作確認

### 1. MCPサーバーのテスト

```bash
cd ~/tyrano-studio-mcp
python3.11 test_e2e.py
```

**期待される出力**:
```
============================================================
TYRANO STUDIO MCP SERVER - E2E TEST
============================================================
...
🎉 ALL TESTS PASSED!
```

### 2. デモプロジェクト生成

```bash
python3.11 examples/create_demo.py
```

**期待される出力**:
```
✅ Demo project created successfully!
```

### 3. Claude Codeで確認

Claude Codeを起動し、以下のように入力：

```
List all projects in TyranoStudio
```

プロジェクト一覧が表示されれば成功です！

## 🔍 トラブルシューティング

### エラー: "ModuleNotFoundError: No module named 'mcp'"

**原因**: mcpモジュールがインストールされていない

**解決方法**:
```bash
pip3.11 install mcp
```

### エラー: "Permission denied"

**原因**: 実行権限がない

**解決方法**:
```bash
chmod +x ~/tyrano-studio-mcp/server.py
chmod +x ~/tyrano-studio-mcp/test_e2e.py
```

### エラー: "TyranoStudio path not found"

**原因**: TyranoStudioのパスが正しくない

**解決方法**:
1. TyranoStudioの実際のパスを確認
2. `server.py`の`TYRANO_BASE`を修正

```bash
# TyranoStudioのパスを探す
find ~ -name "TyranoStudio.app" -type d 2>/dev/null
```

### エラー: "Command not found: python3.11"

**原因**: Python 3.11がインストールされていない

**解決方法**:

#### macOS (Homebrew):
```bash
brew install python@3.11
```

#### Linux (apt):
```bash
sudo apt update
sudo apt install python3.11
```

### Claude Codeでサーバーが表示されない

**チェックリスト**:
1. ✅ `mcp_config.json`の構文が正しい
2. ✅ パスが絶対パス
3. ✅ Python実行可能ファイルのパスが正しい
4. ✅ Claude Codeを再起動した

**確認方法**:
```bash
# 設定ファイルを確認
cat ~/.claude/mcp_config.json

# JSONの構文チェック
python3 -m json.tool ~/.claude/mcp_config.json
```

## 🔄 アップデート

### 最新版への更新

```bash
cd ~/tyrano-studio-mcp
git pull origin master
pip install -r requirements.txt --upgrade
```

### バージョン確認

```bash
cd ~/tyrano-studio-mcp
git log -1 --oneline
```

## 🗑️ アンインストール

### MCPサーバーの削除

```bash
# ディレクトリごと削除
rm -rf ~/tyrano-studio-mcp

# Claude Code設定から削除
# ~/.claude/mcp_config.jsonを編集し、
# "tyrano-studio"セクションを削除
```

### 依存関係の削除

```bash
pip uninstall mcp -y
```

## 📚 次のステップ

インストールが完了したら：

1. **[QUICKSTART.md](QUICKSTART.md)** - 5分で始める
2. **[examples/create_demo.py](examples/create_demo.py)** - デモ実行
3. **[API.md](API.md)** - 全機能の詳細
4. **[FEATURES.md](FEATURES.md)** - 機能カタログ

## 💬 サポート

問題が解決しない場合：

- **GitHub Issues**: https://github.com/ShunsukeHayashi/tyrano-studio-mcp/issues
- **ドキュメント**: リポジトリ内の各種ドキュメント
- **ログ確認**: エラーメッセージの全文を記録

## 🎉 インストール完了！

TyranoStudio MCP Serverが使えるようになりました。
素晴らしいゲームを作ってください！

---

**最終更新**: 2025年10月
**バージョン**: 1.0.0