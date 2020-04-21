#submitjob.py
#Upload the file to remote server and then start the data processing
import pysftp
import json
import sys
import subprocess
import copy
#Upload files:
def update_progress(uuid, val):
    cur_result = json.load(open(uuid,'r'))
    cur_result['curr_upload'] = val
    json.dump(cur_result,open(uuid,'w'))


if __name__ == '__main__':
    target_dir = '/home/bigghost/TranscriptomePipelineTest/WebService/mysite'
    try:
        srv = pysftp.Connection(host="hpc1.engr.ucdavis.edu",username="bigghost",private_key_pass="284ejo3ejo3KEKE",private_key="~/HPCAccounts_Private_OpenSSH")
        command = ["ssh", "-i", "~/HPCAccounts_Private_OpenSSH", "bigghost@hpc1.engr.ucdavis.edu"]
        remote_command = 'cd TranscriptomePipelineTest/TranscriptomicPipelines/ && srun'
        
        running_time = "96:00:00"
        remote_command = remote_command + ' --time ' + running_time + ' ' #Specify time

        uuid = sys.argv[1]
        remote_command = remote_command + ' -J ' + uuid + ' ' #Specify job name

        main_program_name = "transcriptomic_pipeline_website.py"
        remote_command = remote_command + ' python ' + main_program_name + ' ' #Main Program
       
        gff_url = sys.argv[2]
        remote_command = remote_command + ' ' + gff_url #GFF URL

        sample_table = sys.argv[3]
        with srv.cd(target_dir):
            srv.put(sample_table)
            remote_command = remote_command + ' ' + target_dir + '/' + sample_table + ' '
            update_progress(uuid, 0.2)

            if len(sys.argv) >= 5:
                corr_table = sys.argv[4]
                srv.put(corr_table)
                remote_command = remote_command + ' ' + target_dir + '/' + corr_table + ' '
            update_progress(uuid, 0.4)

            if len(sys.argv) >= 6:
                knowledge_capture_sample_table = sys.argv[5]
                srv.put(knowledge_capture_sample_table)
                remote_command = remote_command + ' ' + target_dir + '/' + knowledge_capture_sample_table + ' '
            update_progress(uuid, 0.6)

            if len(sys.argv) >= 7:
                knowledge_capture_gene_table = sys.argv[6]
                srv.put(knowledge_capture_gene_table)
                remote_commnd = remote_command + ' ' + target_dir + '/' + knowledge_capture_gene_table + ' '
            update_progress(uuid, 0.8)

        check_command = copy.copy(command)
        total_command = command.append(remote_command)
        proc = subprocess.Popen(total_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.stdin.write('284ejo3ejo3KEKE\n')
        proc.stdin.flush()

        stdout, stderr = proc.communicate()
        print(stdout)
        print(stderr)
        update_progress(uuid, 0.9)

        check_command.append('squeue -n '+ uuid + '-h')
        proc = subprocess.Popen(check_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        proc.stdin.write('284ejo3ejo3KEKE\n')
        proc.stdin.flush()

        stdout, stderr = proc.communicate()
        print(stdout)
        print(stderr)
        if len(stdout) > 0:
            update_progress(uuid, 1)
        else:
            update_progress(uuid, -3)




    except:
        update_progress(uuid, -1)
        return
