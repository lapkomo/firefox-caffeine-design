# Firefox Caffeine

Firefox Caffeine は、macOS でダウンロード中のシステムスリープを防止する Firefox 拡張機能です。

複数のダウンロードが同時に進行している場合でも、最後のダウンロードが完了するまで睡眠抑止を継続します。

## 機能概要

- ダウンロード開始時に自動でスリープ抑止を有効化
- 同時進行中のダウンロード数を追跡
- 最後のダウンロード完了時に自動で停止
- 失敗やキャンセル時にも状態を正しく更新
- Native Messaging を利用して Firefox と Python ヘルパーを連携

## アーキテクチャ

- `extension/`: Firefox 拡張機能本体
  - `manifest.json`: MV3 の定義
  - `src/background.js`: ダウンロード監視と native host 連携
  - `src/popup.html`, `src/popup.js`: 設定 UI
- `native_helper/`: Python ベースのヘルパー
  - `download_manager.py`: ダウンロード状態管理
  - `caffeinate_manager.py`: `caffeinate` の起動・停止
  - `notification_retry.py`: 通知と再試行
- `tests/`: Python のユニットテスト

## 前提条件

- Firefox
- macOS
- Python 3
- `caffeinate` コマンド（macOS 標準付属）

## インストール手順

1. Firefox で開発版の拡張機能をロード
2. Firefox の設定から開発者モードを有効化
3. `extension/` を Firefox の拡張機能として読み込む
4. 初回セットアップ時にヘルパーの状態を確認
5. ダウンロード開始時にスリープ抑止が自動で有効化されることを確認

## native helper の導入

`native-helper/firefox_caffeine.py` は native messaging host として機能します。実運用では、Firefox の native-messaging-hosts 配下に配置してください。

一般的な配置先:

- `~/.mozilla/native-messaging-hosts/`

詳細なセットアップ手順は [docs/DEVELOPMENT.md](./docs/DEVELOPMENT.md) を参照してください。

## 開発

```bash
python -m unittest discover -s tests -p 'test_*.py'
```

## 注意事項

- 実運用時は Firefox のネイティブホスト設定と、対応する manifest の設定を正しく揃える必要があります。
- `caffeinate` の利用可否は helper のプローブで確認されます。
- 失敗時の再試行は自動ではなく、状態管理の基盤として機能します。
