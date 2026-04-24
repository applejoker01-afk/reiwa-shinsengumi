# 📌 X投稿の追加方法

このファイル（`x-posts.json`）にURLを追加するだけで、
レポートページの「疑惑の人物たちのこの件に対する対応」セクションに自動掲載されます。

---

## ✏️ 追加の手順（30秒）

1. `x-posts.json` を開く
2. 追加したい投稿の情報を以下の形式で末尾に追記
3. GitHubにコミット＆プッシュ → ページに即反映

---

## 📄 x-posts.json の書き方

```json
[
  {
    "person": "山本太郎",
    "role": "代表（活動休止中）",
    "date": "2026-04-24",
    "url": "https://twitter.com/yamamototaro0/status/1234567890123456789",
    "note": "秘書給与問題についての本人コメント（任意）"
  },
  {
    "person": "大石あきこ",
    "role": "共同代表",
    "date": "2026-04-23",
    "url": "https://twitter.com/oishiakiko/status/9876543210987654321",
    "note": ""
  }
]
```

### 各フィールドの説明

| フィールド | 必須 | 説明 |
|---|---|---|
| `person` | ✅ | 人物名（同じ名前でグルーピングされます） |
| `role` | ✅ | 役職名（グループヘッダーに表示） |
| `date` | ✅ | 投稿日（`YYYY-MM-DD` 形式） |
| `url` | ✅ | XのポストURL（`https://twitter.com/ユーザー名/status/数字`） |
| `note` | ─ | 備考・コメント（任意、空文字 `""` でも可） |

---

## ⚠️ よくある間違い

### ❌ NG: URLが不完全
```
"url": "https://twitter.com/username"   ← status/数字 がない
"url": "https://x.com/username/status/..."   ← x.com でも動作しますが twitter.com 推奨
```

### ❌ NG: カンマの付け忘れ
```json
[
  { "person": "山本太郎", ... }   ← 最後の要素はカンマ不要
  { "person": "大石あきこ", ... } ← ここにカンマが必要！
]
```

### ✅ 正しい形式
```json
[
  { "person": "山本太郎", "role": "代表", "date": "2026-04-24", "url": "https://twitter.com/.../status/123", "note": "" },
  { "person": "大石あきこ", "role": "共同代表", "date": "2026-04-23", "url": "https://twitter.com/.../status/456", "note": "コメント" }
]
```

---

## 🎥 動画付き投稿の扱い

Xの公式埋め込みウィジェットは動画も自動的に表示・再生されます。
特別な操作は不要です。URLを追加するだけで動画も表示されます。

---

## 👁️ ローカルで確認する方法

GitHubにプッシュせずにローカルで確認したい場合：

```bash
# Python でローカルサーバーを起動（CORS対策のため必要）
python -m http.server 8000

# ブラウザで開く
# http://localhost:8000
```

> ⚠️ `index.html` をブラウザで直接開くと CORS エラーで x-posts.json が読み込めません。
> 必ずローカルサーバー経由で確認してください。

---

## 🔄 自動更新との連携

`auto_update.py` は現在、タイムライン・ネット反応を自動更新しますが、
X投稿の選定は **手動** で行うことを推奨します（誤った投稿の掲載を防ぐため）。
