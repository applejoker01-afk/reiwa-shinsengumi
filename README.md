# 🔴 れいわ新選組の終焉 ─ 疑惑・内紛の全記録

> 公開情報・報道・証言に基づく調査分析レポート

## 📦 このリポジトリの構成

```
reiwa-end-report/
├── index.html                  # メインレポート（GitHub Pagesで公開）
├── .github/
│   └── workflows/
│       └── deploy.yml          # 自動デプロイ + Note下書き生成
└── README.md
```

## 🚀 GitHub Pagesで公開する手順

1. このリポジトリをGitHubにアップロード（Public）
2. Settings → Pages → Source: `main` / `/ (root)` → Save
3. 2〜3分後、`https://[username].github.io/reiwa-end-report/` で公開

## 📝 コンテンツの更新方法

### ニュース・疑惑の追記
1. `index.html` を開く
2. タイムライン部分（`<!-- TIMELINE -->`）に新しい `<div class="timeline-item">` を追加
3. GitHub Desktopでコミット＆プッシュ → 自動デプロイ

### ネット反応の追加
1. `<!-- NET REACTIONS -->` セクションに `<div class="reaction-card">` を追記
2. プッシュ → 自動反映

## 📬 Note記事への転用

GitHub Actions の Artifacts から `NOTE-DRAFT-[日付].txt` をダウンロードし、
内容を整えてNoteに貼り付けて投稿。

## ⚠️ 注意事項

- 本レポートは公開情報・報道を基にした調査分析であり、特定の政治的立場を代表するものではありません
- 疑惑段階の情報は「疑惑」として明記し、確定事実と明確に区別しています
- 情報の誤りや更新があれば適宜修正します
