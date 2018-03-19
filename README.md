# classify_paper

## 1. 概要
classify_paperは、トピックモデルを用いた新聞記事の分類を行うスクリプトである。
現在は、トピックへの自動ラベル付与機能しかない。


## 2. 依存関係

* OS: Ubuntu Server 14.04
* 言語: Python 3.6.1
* DB: PostgreSQL 9.3.6
* POSTagger: [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)

___
## 3. 環境構築

### 3.1 ライブラリの導入
ライブラリのリストであるrequirements.txtを利用し、以下のコマンドを実行すると
導入できる。

```
pip install -r requirements.txt
```
### 3.2 DBの構築

本プログラムで使用するDBは、別アプリ[paper_rails](https://github.com/Islenauto/paper_rails)
と共有している。
DBの構築手順の詳細は上記のアプリのREADMEを参照すること。


## 4. 実行方法
scriptディレクトリに様々なファイルがあるが、
"update_model.py"と"grant_label.py"以外のファイルは不要である。

### 4.1 指定した記事を用いてトピックモデルを生成したい場合
scriptディレクトリで以下のコマンドを実行。
モデルファイルがdata/に生成される。
```
python update_model.py BBC science
```

### 4.2 生成したトピックモデルにラベルを付与したいとき
下記のコマンドを実行。
結果は、result/label/にトピックごとにcsvファイルが生成される。

```
python scoring_labels.py BBC science
```


## 5. ディレクトリ構成
```
data/: モデルファイルの保存先
script/: トピックモデルの生成やラベル付与を行うためのスクリプト置き場
result/:scriptの実行結果の保存先
mylib/:scriptが参照する自作クラス置き場
```
