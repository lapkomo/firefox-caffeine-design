# Domain Docs

エンジニアリングスキルがコードベースを調査するとき、どのドメイン文書を読むべきかを定義します。

## 調査前に読むもの

- リポジトリルートの **`GLOSSARY.md`**、または
- ルートに `GLOSSARY-MAP.md` がある場合は、そのファイル。これはコンテキストごとの `GLOSSARY.md` へのマップです。対象トピックに関連するものをすべて読む。
- **`docs/adr/`**: 対象領域に関係する ADR を読む。マルチコンテキストのリポジトリでは、`src/<context>/docs/adr/` も合わせて見て、コンテキストごとの決定事項を確認する。

これらのファイルが存在しない場合でも、**黙って進めてください**。欠落を指摘したり、先に生成を勧めたりしないでください。`/domain-modeling` skill（`/grill-with-docs` や `/improve-codebase-architecture` から到達可能）は、用語や意思決定が実際に解決されるときにだけ、必要に応じてこれらを作成します。

## ファイル構成

Single-context repo（ほとんどのリポジトリ）:

```
/
├── GLOSSARY.md
├── docs/adr/
│   ├── 0001-event-sourced-orders.md
│   └── 0002-postgres-for-write-model.md
└── src/
```

Multi-context repo（ルートに `GLOSSARY-MAP.md` がある場合）:

```
/
├── GLOSSARY-MAP.md
├── docs/adr/                          ← システム全体の意思決定
└── src/
    ├── ordering/
    │   ├── GLOSSARY.md
    │   └── docs/adr/                  ← コンテキストごとの意思決定
    └── billing/
        ├── GLOSSARY.md
        └── docs/adr/
```

## 用語集の語彙を使う

Issue のタイトル、リファクタ提案、仮説、テスト名などでドメイン概念の名前を使うときは、`GLOSSARY.md` で定義されている用語を優先してください。用語集が明示的に避けている同義語に流れないようにしてください。

必要な概念が用語集にまだ存在しない場合、それは次のどちらかを示しています。

- プロジェクトで使っていない言い回しを勝手に作っている（見直しが必要）
- 本当に不足している用語がある（`/domain-modeling` にメモする）

## ADR の矛盾に注意する

既存の ADR と矛盾する場合は、黙って上書きせず、明示的に指摘してください。

> _ADR-0007（event-sourced orders）と矛盾するが、再検討の価値があるため…_
