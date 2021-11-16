# 概要
某小説サイトの連載小説のサブタイトル語彙が本文中に含まれる数をカウントするスクリプト

# 動かすのに必要なこと
- mecabのインストール  
- `pip install -r requirements.txt`の実行
- `cp .env.template .env`を行い中に必要なものを記述
  - USER_AGENT　ユーザーエージェントの設定
  - CSV_DIR　読み込むCSVファイルの指定
  - URL_COLNUM　CSVのURL列の番号
  - TITLE_COLNUM　CSVファイルのサブタイトル列の番号
