
# MikuBot

A Discord bot for VirtualLiveLab

## ローカル開発


### 事前準備
1. [このドキュメント](https://taskfile.dev/installation/) を参考に`go-task` をインストールしておくこと。
2. [このドキュメント](https://docs.astral.sh/uv/getting-started/installation/) を参考に`uv` をインストールしておくこと。

### 環境構築

リポジトリをクローン

```bash
  gh repo clone VirtualLiveLab/Mikubot
```

プロジェクトへ移動

```bash
  cd Mikubot
```

開発環境をセットアップ

```bash
  task setup
```

[Environment Variables](#environment-variables)を参照して`.env`ファイルに環境変数を設定する

> [!WARNING]
> `.env.example`を編集するわけではないことに注意。
> `.env`ファイルを編集すること。

ローカル環境でBotを起動

```bash
  task up
```

> [!TIP]
> この開発サーバーはファイルを変更したら一度再起動しないと変更が反映されない。

## Environment Variables

### ないと起動しないもの

`DISCORD_BOT_TOKEN`: Discord Developer Portalから取得したBotのトークン

### なくても起動するもの

`LOG_CHANNEL_ID`: ログメッセージを送るチャンネルのID。ない場合はログを送信しない。

`NOTION_TOKEN`: Notion Integrationのトークン。Notion APIを使用するために必要。

`NOTION_DOMAIN`: Notionワークスペースのドメイン。ここで設定したドメインのNotion Urlが送信されると検知される。

`SENTRY_DSN`: 開発時は変更しなくてOK

`DEPLOY_ENVIRONMENT`: 開発時は変更しなくてOK

`CF_ACCESS_CLIENT_ID`, `CF_ACCESS_CLIENT_SECRET`: Cloudflare AccessのクライアントIDとクライアントシークレット。`/wol` による部室PC遠隔起動に必要。

### 最小構成の`.env`の例

```sh
# 必ずセットするもの
DISCORD_BOT_TOKEN="Discord Bot Token Here"

# なくても起動するもの
LOG_CHANNEL_ID=""

NOTION_TOKEN=""
NOTION_DOMAIN=""

SENTRY_DSN=""

# PC遠隔起動機能
CF_ACCESS_CLIENT_ID=""
CF_ACCESS_CLIENT_SECRET=""
```
