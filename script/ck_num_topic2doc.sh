#!/bin/zsh

categories=("world" "science" "business" "technology" "sports" "entertainment")
num_samples=(100 200 300 400 500 600 700)

for category in ${categories}
do   
    echo "**$category**"
    echo "num_sample,ave_num_topic" 
    for num_sample in ${num_samples}
    do
        python ck_num_topic2doc.py BBC $category $num_sample
    done
done
