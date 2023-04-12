# Mikubot

TOKEN等はGithub ActionsのSecretsに格納しDockerでBuildする際に環境変数に加えています。



### memo

#### コンテナのアップデート
`gcloud compute instances update-container [コンテナ名] --container-image [GCR]:[タグ名]`
