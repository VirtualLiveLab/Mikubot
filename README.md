# Mikubot

VLL Discord サーバーのためのBot

~~TOKEN等はGithub ActionsのSecretsに格納しDockerでBuildする際に環境変数に加えています。~~

イメージに焼き付けたくなかったので実行時に`--env`オプションで渡してます。

<details>
<summary>開発者向け</summary>

### `poetry`と`pre-commit`を使用するようになりました

pipではなくpoetryを使用するようになりました。また、pre-commitを使用して
デプロイ用`requirements.txt`の自動生成を行うようになりました。

```bash
git clone <this repo>
cd <this repo>
poetry install
poetry run pre-commit install
```

### 依存ライブラリを更新しました

`discord.py v1.7.3`及び`dislash.py`は今後利用できなくなる可能性があるため、`discord.py v2`ベースですべて書き直しました。

### ファイル分割

単一ファイルにすべての処理が書かれていたものを[Cog and Extension](https://discordpy.readthedocs.io/ja/latest/ext/commands/extensions.html)ベースのファイル分割に変更しました。

起動時にファイル探索をし、**app/\*\*/cog.py** というファイル名のExtensionが自動で読み込まれます。

### スニペット

VSCode向けの新規Cog作成スニペットを追加してあります。

### CI

- `pre-commit`を使用して、基本的なコードチェックを行っています。`requirements.txt`の更新を忘れるとCIが失敗します。
  - Pull Request内であれば修正を自動でコミットしてくれます。
- Dockerイメージのビルドまでを事前にテストしています。(起動確認はしていません)
- typoチェッカーも回しています。

### ビルド・デプロイ

GitHub Actionsでイメージをビルドして、ConoHa VPS上へ自動デプロイする設定になっています。

</details>
