# classify_paper

## 1. 概要
classify_paperは、トピックモデルを用いた新聞記事の分類・推薦を行うプログラムである。
現在は、トピックへの自動ラベル付与機能しかない。

---
---

## 2. 依存関係

* OS: Ubuntu Server 14.04
* 言語: Python 3.6.1
* DB: PostgreSQL 9.3.6
* POSTagger: [TreeTagger](http://www.cis.uni-muenchen.de/~schmid/tools/TreeTagger/)

___
---
---

## 3. DBの構築

本プログラムで使用するDBは、別アプリ[paper_rails](https://github.com/Islenauto/paper_rails)
と共有している。
DBの構築手順の詳細は上記のアプリのREADMEを参照すること。
