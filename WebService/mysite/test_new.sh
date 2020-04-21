#!/home/cetan/.local/bin/expect
set gff_url [lindex $argv 0]
set input_corr [lindex $argv 1]
set knowledge_sample [lindex $argv 2]
set knowledge_gene [lindex $argv 3]
set sample_list [lindex $argv 4]
set email [lindex $argv 5]
set tag [lindex $argv 6]
set timestamp [timestamp -format %Y-%m-%d_%H:%M]

eval spawn ssh -i /home/cetan/HPCAccounts_Private_OpenSSH bigghost@hpc1.engr.ucdavis.edu
expect ":"
send "284ejo3ejo3KEKE\r"
expect ":"
send "echo $email\r"
expect ":"
send "cd ~/TranscriptomePipelineTest/TranscriptomicPipelines/\r"
expect ":"
send "./take_webservice_input_new.sh '$gff_url' $input_corr $knowledge_sample $knowledge_gene $sample_list $email $tag >${timestamp}_${tag}.log 2>${timestamp}_${tag}.error & \r\r"
expect ":"
send "logout\r"
interact
exit
