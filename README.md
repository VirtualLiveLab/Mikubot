
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

.envを編集

[Environment Variables](#environment-variables)を参照

開発サーバーを起動

```bash
  rye run dev
```

> [!TIP]
> この開発サーバーはファイルを変更したら一度再起動しないと変更が反映されません。

## Environment Variables

このBotは以下の環境変数がないと動作しません。

`DISCORD_BOT_TOKEN`: Discord Bot Token

`LOG_CHANNEL_ID`: ログメッセージを送るチャンネルのID

`NOTION_TOKEN`: Notion Integration Token

`NOTION_DOMAIN`: Notion Domain

`SENTRY_DSN`: 本番環境の場合のみ。開発時は変更しなくてOK
