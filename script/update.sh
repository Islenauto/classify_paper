#!/bin/zsh

category=("world" "science" "business" "technology" "sports" "entertainment")
for cate in ${category}
do
	python updatedata.py BBC $cate
done
