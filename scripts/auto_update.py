#!/usr/bin/env python3
"""
れいわ新選組レポート 自動更新スクリプト
- Anthropic API + web_search ツールで最新ニュースを収集
- index.html のタイムライン・ネット反応・サイドバーを自動更新
"""

import anthropic
import json
import re
import sys
from datetime import datetime, timezone, timedelta

JST = timezone(timedelta(hours=9))
TODAY = datetime.now(JST).strftime("%Y年%m月%d日")
TODAY_ISO = datetime.now(JST).strftime("%Y-%m-%d")

# =============================================
# 1. Anthropic API でニュース収集
# =============================================
def fetch_latest_news(api_key: str) -> dict:
    client = anthropic.Anthropic(api_key=api_key)

    system_prompt = """あなたは日本の政治ニュースを調査する専門家です。
提供された情報を元に、構造化されたJSONのみを返してください。
前置きや解説は一切不要です。JSONのみを返してください。"""

    user_prompt = f"""本日 {TODAY} 時点の最新情報を検索してください。

検索対象：
1. れいわ新選組 山本太郎 秘書給与 詐取 最新 2026
2. れいわ新選組 大石あきこ 疑惑 2026
3. れいわ新選組 櫛渕万里 幽霊秘書 2026
4. れいわ新選組 内紛 臨時総会 2026
5. れいわ新選組 最新ニュース {TODAY}

収集した情報を以下のJSON形式で返してください（前置きなしでJSONのみ）:
{{
  "update_date": "{TODAY}",
  "timeline_items": [
    {{
      "date": "YYYY年MM月DD日",
      "tag": "タグ名（例：新疑惑/続報/内紛/告発）",
      "tag_color": "red|warning|info|dark（redがデフォルト）",
      "title": "見出し（100字以内）",
      "body": "本文（200字以内、事実ベースで疑惑は疑惑として記載）",
      "source": "情報源（メディア名と日付）",
      "is_new": true
    }}
  ],
  "net_reactions": [
    {{
      "platform": "X|5ch|note|その他",
      "text": "反応内容（150字以内）",
      "engagement": "RT数・いいね数等（不明の場合は省略）"
    }}
  ],
  "sidebar_news": [
    {{
      "date": "YYYY年MM月DD日",
      "title": "短いニュース見出し（60字以内）"
    }}
  ],
  "summary": "今回の更新で追加した主な内容の要約（100字以内）"
}}

重要な注意事項:
- 疑惑はあくまで「疑惑」として記載し、確定事実と混在させないこと
- 同じニュースを重複して載せないこと
- 直近7日以内の新しい情報を優先すること
- 情報が見つからない場合は timeline_items を空配列にすること
"""

    print(f"[{TODAY}] Anthropic API でニュース収集開始...")
    
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=4096,
        tools=[{"type": "web_search_20250305", "name": "web_search"}],
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )

    # レスポンスからJSONを抽出
    result_text = ""
    for block in response.content:
        if block.type == "text":
            result_text += block.text

    # JSON部分を抽出
    json_match = re.search(r'\{[\s\S]*\}', result_text)
    if not json_match:
        print("WARNING: JSONが見つかりません。空の更新を返します。")
        return {
            "update_date": TODAY,
            "timeline_items": [],
            "net_reactions": [],
            "sidebar_news": [],
            "summary": "新しい情報は見つかりませんでした。"
        }

    try:
        return json.loads(json_match.group())
    except json.JSONDecodeError as e:
        print(f"WARNING: JSONパースエラー: {e}")
        return {
            "update_date": TODAY,
            "timeline_items": [],
            "net_reactions": [],
            "sidebar_news": [],
            "summary": "JSONパースエラーが発生しました。"
        }


# =============================================
# 2. タイムラインHTMLを生成
# =============================================
TAG_COLORS = {
    "red": "",        # デフォルト（赤）
    "warning": " warning",
    "info": " info",
    "dark": " dark",
}

def build_timeline_item(item: dict) -> str:
    date = item.get("date", TODAY)
    tag = item.get("tag", "続報")
    color = TAG_COLORS.get(item.get("tag_color", "red"), "")
    title = item.get("title", "")
    body = item.get("body", "")
    source = item.get("source", "")
    is_new = item.get("is_new", True)
    new_badge = ' <span style="color:var(--crimson);font-size:10px;font-weight:700;">★ NEW</span>' if is_new else ""

    # 日付を年と日に分割
    year_match = re.match(r'(\d{4})年(.+)', date)
    if year_match:
        year = year_match.group(1) + "年"
        day = year_match.group(2)
    else:
        year = ""
        day = date

    source_html = f'\n            <div class="source-badge">📰 {source}</div>' if source else ""

    return f"""
        <div class="timeline-item">
          <div class="timeline-date">
            <span class="tl-year">{year}</span>
            <span class="tl-day">{day}</span>
          </div>
          <div class="timeline-content">
            <span class="tl-tag{color}">{tag}</span>
            <h3>{title}{new_badge}</h3>
            <p>{body}</p>{source_html}
          </div>
        </div>"""


def build_reaction_card(reaction: dict) -> str:
    platform = reaction.get("platform", "X")
    text = reaction.get("text", "")
    engagement = reaction.get("engagement", "")

    icon_map = {"X": "𝕏", "5ch": "2ch", "note": "📝", "その他": "💬"}
    icon = icon_map.get(platform, "💬")
    cls = "x" if platform == "X" else "anon"

    engagement_html = f'\n          <div class="reaction-meta">{engagement}</div>' if engagement else ""

    return f"""
      <div class="reaction-card">
        <div class="reaction-source">
          <div class="source-icon {cls}">{icon}</div>
          <span style="font-family:'Noto Sans JP',sans-serif;font-size:12px;color:#888;">{platform} {TODAY}</span>
        </div>
        <div class="reaction-text">{text}</div>{engagement_html}
      </div>"""


def build_sidebar_news_item(news: dict) -> str:
    date = news.get("date", TODAY)
    title = news.get("title", "")
    return f"""
          <div class="news-item">
            <div class="news-date">{date}</div>
            <div class="news-title">{title}</div>
          </div>"""


# =============================================
# 3. index.html を更新
# =============================================
def update_html(html_path: str, data: dict) -> str:
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    timeline_items = data.get("timeline_items", [])
    net_reactions = data.get("net_reactions", [])
    sidebar_news = data.get("sidebar_news", [])

    # --- タイムラインに新アイテムを先頭に追加 ---
    if timeline_items:
        new_tl_html = "\n".join(build_timeline_item(item) for item in timeline_items)
        # タイムラインの先頭（最初の timeline-item の前）に挿入
        html = re.sub(
            r'(<div class="timeline">)',
            r'\1\n' + new_tl_html,
            html,
            count=1
        )
        print(f"  → タイムライン: {len(timeline_items)}件追加")
    else:
        print("  → タイムライン: 新情報なし")

    # --- ネット反応を先頭に追加 ---
    if net_reactions:
        new_reactions_html = "\n".join(build_reaction_card(r) for r in net_reactions)
        html = re.sub(
            r'(<div class="reactions-section">)',
            r'\1\n' + new_reactions_html,
            html,
            count=1
        )
        print(f"  → ネット反応: {len(net_reactions)}件追加")

    # --- サイドバーニュースを先頭に追加（最大8件を維持） ---
    if sidebar_news:
        new_sidebar_html = "\n".join(build_sidebar_news_item(n) for n in sidebar_news)
        # 既存のニュースアイテムを取得して件数管理
        existing_items = re.findall(r'<div class="news-item">[\s\S]*?</div>\s*</div>', html)
        if len(existing_items) > 6:
            # 古いアイテムを削除（最新6件＋今回追加分を維持）
            for old_item in existing_items[6:]:
                html = html.replace(old_item, "", 1)

        html = re.sub(
            r'(class="sidebar-card-body">\s*\n\s*<div class="news-item">)',
            lambda m: m.group(0).replace(
                '<div class="news-item">',
                new_sidebar_html + '\n          <div class="news-item">'
            ),
            html,
            count=1
        )
        print(f"  → サイドバー: {len(sidebar_news)}件追加")

    # --- 最終更新日を更新 ---
    html = re.sub(
        r'最終更新: <strong>[^<]+</strong>',
        f'最終更新: <strong>{TODAY} 自動更新</strong>',
        html
    )

    return html


# =============================================
# 4. 変更ログを保存
# =============================================
def save_changelog(data: dict, log_path: str):
    summary = data.get("summary", "更新なし")
    timeline_count = len(data.get("timeline_items", []))
    
    log_entry = f"## {TODAY}\n- 追加: {timeline_count}件\n- 概要: {summary}\n\n"
    
    try:
        with open(log_path, "r", encoding="utf-8") as f:
            existing = f.read()
    except FileNotFoundError:
        existing = "# 更新ログ\n\n"

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(existing.replace("# 更新ログ\n\n", f"# 更新ログ\n\n{log_entry}"))

    print(f"  → 変更ログ保存: {summary}")


# =============================================
# メイン処理
# =============================================
def main():
    import os

    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY が設定されていません")
        sys.exit(1)

    html_path = "index.html"
    log_path = "UPDATE_LOG.md"

    # ニュース収集
    data = fetch_latest_news(api_key)
    print(f"\n収集結果: {data.get('summary', '不明')}")
    print(f"  タイムライン: {len(data.get('timeline_items', []))}件")
    print(f"  ネット反応: {len(data.get('net_reactions', []))}件")

    # HTMLが更新対象の場合のみ処理
    if not data.get("timeline_items") and not data.get("net_reactions"):
        print("\n新しい情報なし。HTMLの更新をスキップします。")
        # 最終更新日だけ更新
        with open(html_path, "r", encoding="utf-8") as f:
            html = f.read()
        html = re.sub(
            r'最終更新: <strong>[^<]+</strong>',
            f'最終更新: <strong>{TODAY} 確認済（新情報なし）</strong>',
            html
        )
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        save_changelog(data, log_path)
        return

    # HTML更新
    print("\nindex.html を更新中...")
    updated_html = update_html(html_path, data)

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(updated_html)

    print(f"  → index.html 更新完了")

    # ログ保存
    save_changelog(data, log_path)

    # Note下書き生成
    note_draft = f"""【{TODAY} 自動更新版】

# れいわ新選組の終焉──{data.get('summary', '疑惑と内紛の全記録')}

{chr(10).join(f"■ {item['title']}" for item in data.get('timeline_items', [])[:5])}

{'（詳細はレポートページをご覧ください）' if data.get('timeline_items') else '新しい疑惑情報を継続監視中です。'}

👉 詳細レポート: https://[username].github.io/reiwa-end-report/

---
#れいわ新選組 #山本太郎 #大石あきこ #政治とカネ #秘書給与 #内部告発
"""
    with open("note-draft.txt", "w", encoding="utf-8") as f:
        f.write(note_draft)
    print(f"  → note-draft.txt 生成完了")

    print(f"\n✅ 更新完了: {data.get('summary')}")


if __name__ == "__main__":
    main()
