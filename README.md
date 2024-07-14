
# MikuBot

A Discord bot for VirtualLiveLab

## ローカル開発

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
  rye sync
```

.envをコピー

```bash
  cp .env.example .env
```

[Environment Variables](#environment-variables)を参照して`.env`ファイルに環境変数を設定する

> [!WARNING]
> `.env.example`を編集するわけではないことに注意。
> `.env`ファイルを編集すること。

開発サーバーを起動

```bash
  rye run dev
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
