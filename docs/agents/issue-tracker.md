# Issue tracker: GitHub

このリポジトリの課題と仕様は `lapkomo/firefox-caffeine-design` の GitHub Issues に置かれます。すべての操作は `gh` CLI を使います。

## 運用ルール

- **課題を作成する**: `gh issue create --title "..." --body "..."` を使います。複数行の本文が必要なときは heredoc を使ってください。
- **課題を確認する**: `gh issue view <number> --json number,title,body,labels,comments`
- **課題を一覧表示する**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` を使い、必要に応じて `--label` や `--state` フィルタを追加します。
- **親課題のサブイシューを作る**: `gh issue create --parent <parent> ...` を使うか、後から `gh issue edit <parent> --add-sub-issue <child>` を使います（`gh` 2.94+）。古い `gh` を使う場合は `gh api --method POST repos/<owner>/<repo>/issues/<parent>/sub_issues -F sub_issue_id=<child-db-id>` を使います（データベース ID は **Blocking** の項を参照）。サブイシュー機能が使えない場合は、子課題の本文先頭に `Part of #<parent>` を書いてください。
- **依存関係の管理（Blocking）**: GitHub のネイティブな issue dependencies を使います。依存の追加は `gh issue create --blocked-by <n>,<n> ...` または `gh issue edit <child> --add-blocked-by <blocker>` で行います（`gh` 2.94+）。古い `gh` では `gh api --method POST repos/<owner>/<repo>/issues/<child>/dependencies/blocked_by -F issue_id=<blocker-db-id>` を使います。ここで `<blocker-db-id>` はブロッカーの数値の **database id** です（`gh api repos/<owner>/<repo>/issues/<n> --jq .id` で確認し、`#number` や `node_id` ではありません）。依存関係が使えない場合は、子課題の本文先頭に `Blocked by: #<n>, #<n>` を書いてください。すべての blockers が閉じられた時点でその課題は unblock されます。
- **open な blocker の数を数える**: `gh api repos/<owner>/<repo>/issues/<n> --jq .issue_dependencies_summary.blocked_by` を使います（未解決の blocker のみ。0 は開始可能を意味します）。`gh issue view <n> --json blockedBy` でも確認できますが、閉じた blocker も含まれるので `--jq '[.blockedBy.nodes[] | select(.state == "OPEN")] | length'` のように絞り込みます。
- **課題にコメントする**: `gh issue comment <number> --body "..."`
- **ラベルを付ける / 外す**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **課題を閉じる**: 説明を `gh issue comment <number> --body "..."` で投稿したのち、`gh issue close <number>` を実行します。すでに閉じている issue に対しては `gh issue close --comment` を使うとコメントを残しつつ終了コード 0 で終了できます。

このリポジトリでは `origin` リモートから repo を自動的に判定するため、この checkout から `gh` を実行すれば自動的に対象リポジトリが選ばれます。

## PR を triage の対象にするか

**PR を要求の入口として使う: いいえ。** （外部 PR を機能要求として扱う場合は `yes` に設定してください。`/triage` がこのフラグを読み取ります。）

`yes` にした場合、PR は issue と同じラベルと状態を使い、対応は `gh pr` 系コマンドで行います。

- **PR を確認する**: `gh pr view <number>`、`gh pr view <number> --comments`（TTY 以外では本文ではなくコメントだけが表示されます）、`gh pr diff <number>`
- **triage 対象の外部 PR を一覧表示する**: `gh api --paginate 'repos/{owner}/{repo}/pulls?state=open' --jq '.[] | select(.author_association | IN("OWNER","MEMBER","COLLABORATOR") | not) | {number, title, author: .user.login, author_association, labels: [.labels[].name]}'`
- **コメント / ラベル / close**: `gh pr comment`、`gh pr edit --add-label`/`--remove-label`、`gh pr close`

GitHub は issue と PR で番号空間を共有しているため、`#42` だけでは issue なのか PR なのか曖昧になる場合があります。その場合は `gh pr view 42` を試し、失敗した場合に `gh issue view 42` を使って判定します。

## スキルが「issue tracker に公開」と言ったとき

GitHub の issue を作成します。

## スキルが「関連する ticket を取得」と言ったとき

**課題を確認する** の手順に従って取得します。
