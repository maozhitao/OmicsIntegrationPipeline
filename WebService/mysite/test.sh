#!/home/cetan/.local/bin/expect
set studies [lindex $argv 0]
set species [lindex $argv 1]
set input_corr [lindex $argv 2]
set knowledge_sample [lindex $argv 3]
set knowledge_gene [lindex $argv 4]
set additional_filter [lindex $argv 5]
set email [lindex $argv 6]
set tag [lindex $argv 7]
set timestamp [timestamp -format %Y-%m-%d_%H:%M]

eval spawn ssh -i /home/cetan/HPCAccounts_Private_OpenSSH bigghost@hpc1.engr.ucdavis.edu
expect ":"
send "284ejo3ejo3KEKE\r"
expect ":"
send "echo $email\r"
expect ":"
send "cd ~/TranscriptomePipelineTest/TranscriptomicPipelines/\r"
expect ":"
send "./take_webservice_input.sh '$studies' '$species' $input_corr $knowledge_sample $knowledge_gene $additional_filter $email $tag >${timestamp}_${tag}.log 2>${timestamp}_${tag}.error & \r\r"
expect ":"
send "logout\r"
interact
exit
