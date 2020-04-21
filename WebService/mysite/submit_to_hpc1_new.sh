#!/bin/bash -l
gff_url=$1
input_corr=$2
knowledge_sample=$3
knowledge_gene=$4
sample_list=$5
email=$6
tag=$7
timestamp=$(date "+%Y%m%d-%H%M%S")

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
./upload_input_file.exp $sample_list
./test_new.sh "$gff_url" "$input_corr" "$knowledge_sample" "$knowledge_gene" "$sample_list" "$email" "$tag" >${timestamp}_${tag}.log 2>${timestamp}_${tag}.error
