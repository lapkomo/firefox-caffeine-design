# 開発者向けガイド

## 概要

Firefox Caffeine は、macOS 上で Firefox のダウンロード中に sleep を抑止するための拡張機能です。

処理フローは次の通りです。

1. Firefox 拡張がダウンロード開始を検知
2. background.js が native helper を確認
3. Python ヘルパーが `caffeinate` を起動
4. ダウンロードが完了したら停止判定を実行
5. 必要に応じて通知と再試行を行う

## ディレクトリ構成

```text
firefox-caffeine-design/
├── AGENTS.md
├── README.md
├── docs/
│   └── DEVELOPMENT.md
├── extension/
│   ├── manifest.json
│   └── src/
│       ├── background.js
│       ├── popup.html
│       └── popup.js
├── native-helper/
│   └── firefox_caffeine.py
├── native_helper/
│   ├── __init__.py
│   ├── caffeinate_manager.py
│   ├── download_manager.py
│   └── notification_retry.py
├── tests/
│   ├── test_caffeinate_manager.py
│   ├── test_download_manager.py
│   ├── test_extension_manifest.py
│   ├── test_native_messaging.py
│   └── test_notification_retry.py
└── .gitignore
```

## 主要コンポーネント

### extension

- manifest は Firefox MV3 に準拠
- background.js はダウンロードイベントと native host の検証を担当
- popup.js はセットアップ状況の表示と切り替えを担当

### native_helper

- `DownloadTracker`: ダウンロードの活性状態を監視
- `CaffeinateManager`: `caffeinate` の起動と停止を管理
- `NotificationManager`: 通知や再試行ロジックを管理

### native-helper

- Firefox native messaging host のスタブ実装
- JSON を stdin で受け取り、環境情報と応答を返す

## テスト実行

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## 次の作業候補

- Firefox の native messaging host の正式な manifest 設定
- `downloads.onChanged` の本番イベント連携
- macOS 実機での smoke test
- `caffeinate` 失敗時のバックオフ再試行ポリシー
