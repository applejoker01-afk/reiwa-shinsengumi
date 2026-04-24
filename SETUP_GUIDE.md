# ⚙️ 24時間自動更新セットアップガイド

## 必要なもの
- GitHubアカウント
- Anthropic APIキー（claude.ai/settings または console.anthropic.com で取得）

---

## 🚀 初回セットアップ（5分）

### STEP 1: リポジトリを作成してアップロード

1. GitHub.com で「New repository」
2. Repository name: `reiwa-end-report`
3. **Public** を選択（GitHub Pages の無料利用のため）
4. GitHub Desktop でこのフォルダを選択してコミット＆プッシュ

### STEP 2: ANTHROPIC_API_KEY を Secret に登録

1. リポジトリのページで `Settings` → `Secrets and variables` → `Actions`
2. `New repository secret` をクリック
3. Name: `ANTHROPIC_API_KEY`
4. Value: Anthropicから取得したAPIキー（`sk-ant-...`）
5. `Add secret` をクリック

### STEP 3: GitHub Pages を有効化

1. `Settings` → `Pages`
2. Source: `GitHub Actions` を選択
3. Save

### STEP 4: 動作確認

1. `Actions` タブを開く
2. `24時間ごとに自動更新＆デプロイ` を選択
3. `Run workflow` → `Run workflow` で手動実行
4. 緑のチェックが付いたら成功！

---

## ⏰ 自動実行スケジュール

| タイミング | 内容 |
|---|---|
| **毎日 09:00 JST** | ニュース自動収集 → HTML更新 → デプロイ |
| **手動実行** | Actions → Run workflow |
| **push時** | 常にデプロイ（手動追記した場合も反映）|

---

## 📋 自動更新の仕組み

```
09:00 JST
  ↓
[GitHub Actions 起動]
  ↓
[Python スクリプト実行]
  ↓
[Anthropic API + Web Search]
  ↓
れいわ新選組 最新ニュース収集
  ↓
[index.html 自動更新]
  新しいタイムラインアイテムを先頭に追加
  ネット反応を先頭に追加
  サイドバーニュースを更新
  「最終更新」日時を更新
  ↓
[git commit & push]
  ↓
[GitHub Pages 自動デプロイ]
  ↓
サイト更新完了 🎉
```

---

## 📬 Note 記事への転用

1. Actions → 最新の実行 → `NOTE-DRAFT-[番号]` をダウンロード
2. `note-draft.txt` の内容をNoteに貼り付けて投稿
3. 毎日自動生成されるので定期投稿が簡単に！

---

## 🔧 トラブルシューティング

**Q: Actions が失敗する**
→ ANTHROPIC_API_KEY が正しく設定されているか確認

**Q: 新しいニュースが追加されない**
→ 当日に新しいニュースがない場合、更新はスキップされます（正常動作）

**Q: APIキーの使用量が心配**
→ 1回の実行で使用するトークン数は約2,000〜5,000トークン程度。
  月額費用は数百円以下が目安です。

---

## 📁 ファイル構成

```
reiwa-end-report/
├── index.html                  # メインレポート（自動更新対象）
├── note-draft.txt              # Note用下書き（自動生成）
├── UPDATE_LOG.md               # 更新履歴（自動生成）
├── README.md                   # このファイル
├── SETUP_GUIDE.md              # セットアップガイド
├── scripts/
│   └── auto_update.py          # 自動更新スクリプト
└── .github/
    └── workflows/
        └── deploy.yml          # GitHub Actions定義
```
