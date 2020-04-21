#!/bin/bash -l
studies=$1
species=$2
input_corr=$3
knowledge_sample=$4
knowledge_gene=$5
additional_filter=$6
email=$7
tag=$8
timestamp=""

echo $input_corr
echo $knowledge_sample
echo $knowledge_gene
echo $additional_filter
echo $timestamp
echo $tag
echo ${timestamp}_${tag}.log

./upload_input_file.exp $input_corr
./upload_input_file.exp $knowledge_sample
./upload_input_file.exp $knowledge_gene
./upload_input_file.exp $additional_filter
./test.sh "$studies" "$species" "$input_corr" "$knowledge_sample" "$knowledge_gene" "$additional_filter" "$email" "$tag" >${timestamp}_${tag}.log 2>${timestamp}_${tag}.error
