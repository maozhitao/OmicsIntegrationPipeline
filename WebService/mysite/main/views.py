from django.shortcuts import render, redirect, reverse
from .forms import Profile_Form, Query_Form
from .models import User_Profile, Query_Profile
from django.views.decorators.csrf import csrf_exempt

import json
from django.core.cache import cache
from django.http import HttpResponse, HttpResponseServerError 
import os
import os.path
import subprocess

import time
import sys

import uuid

import pandas as pd

import tempfile

def init_query_result():
    return {'id_tag': None,
            'pid': 0,
            'current_job':'get_studies',
            'progress_get_studies': 0,
            'progress_get_pub':0,
            'progress_get_tech':0,
            'progress_get_samples':0,
            'progress_filter':0,
            'progress_finalize':0}

def init_feature_table_download_result():
    return {'id_tag': None,
            'pid': 0,
            'curr_size': 0.0,
            'curr_perc': 0.0,
            'output_parsed_feature_table': 0.0}

def init_submit_job_result():
    return {'id_tag': None,
            'pid': 0,
            'curr_upload': 0.0}
            
            
def calc_query_sample_progress(query_result, uuid):
    #check current pid
    try:
        subprocess.check_output(['ps','-P',str(query_result['pid'])])
        running = True
    except:
        running = False
        

    if running:
        #Working
        result = 0.1*query_result['progress_get_studies'] +\
                 0.1*query_result['progress_get_pub'] +\
                 0.1*query_result['progress_get_tech'] +\
                 0.6*query_result['progress_get_samples'] +\
                 0.05*query_result['progress_filter'] +\
                 0.05*query_result['progress_finalize']
        if query_result['progress_get_studies'] < 1:
            status = 'Searching studies...'
        elif query_result['progress_get_pub'] < 1:
            status = 'Fetching corresponded publications...'
        elif query_result['progress_get_tech'] < 1:
            status = 'Fetching corresponded experiment approaches...'
        elif query_result['progress_get_samples'] < 1:
            status = 'Fetching corresponded samples...'
        elif query_result['progress_filter'] < 1:
            status = 'Extracting transcriptomic samples...'
        else:
            status = 'Finalizing results...'
        return result, status, ''
    else:
        #Finish
        if query_result['progress_finalize'] != 1:
            return -1, 'Error!', False #ERROR
        else:
            try:
                result = pd.read_csv(uuid+'_sample_output.csv',index_col = False)
            except:
                return 1, 'Done!', True
            return 1, 'Done!', False #SUCCESS

def calc_feature_table_download_progress(feature_table_download_result):
    #check current pid
    try:
        subprocess.check_output(['ps','-P',str(feature_table_download_result['pid'])])
        running = True
    except:
        running = False
        

    if running:
        #Working
        result = feature_table_download_result['curr_perc']*0.9 + \
                 feature_table_download_result['output_parsed_feature_table']*0.1
        return result
    else:
        #Finish
        if feature_table_download_result['curr_perc'] != 1.0:
           return -1 #ERROR
        else:
           return 1 #SUCCESS


def calc_submit_job_progress(submit_job_result):
    #check current pid
    try:
        subprocess.check_output(['ps','-P',str(submit_job_result['pid'])])
        running = True
    except:
        running = False
        

    if running:
        #Working
        result = submit_job_result['curr_upload']
        return result
    else:
        #Finish
        if submit_job_result['curr_upload'] != 1.0:
           return -1 #ERROR
        else:
           return 1 #SUCCESS

@csrf_exempt
def show_home_page(request):
    if request.method == 'GET':
        #Show the home page
        return show_home_page_get(request)
    else:
        #Submit the query
        return show_home_page_post(request)
        
def show_home_page_get(request):
    #Show the home page
    form = Query_Form()
    context = {"form": form,}
    return render(request, 'home.html', context)

def show_home_page_post(request):
    #POST: request should be from xhr
    #Submit the query
    uuid = request.GET["uuid"]
    studies = request.GET["studies"]
    species = request.GET["species"]
    query_result = init_query_result()
    #Initialize the progress file
    json.dump(query_result,open(uuid,'w'))
    #Call the internal query
    cur_subprocess = subprocess.Popen(['meta-omics',studies,species,uuid])
    query_result['pid'] = cur_subprocess.pid
    json.dump(query_result,open(uuid,'w'))
    while os.path.isfile(uuid) == False:
        #Wait until the file is created
        continue
    #Return Nothing ==> now the javascript should submit the query to check the progress
    return HttpResponse(json.dumps(None))
    
def run_refgen(request):
    uuid = request.GET["uuid"]
    species = request.GET["species"]
    subprocess.check_output(['ref-find', species, uuid+'_refgen_output.csv'])
    result = pd.read_csv(uuid+'_refgen_output.csv')
    if result.shape[0] >= 1:
        return HttpResponse(json.dumps({'available':True}))
    else:
        return HttpResponse(json.dumps({'available':False}))
    
def check_progress_query_sample(request):
    uuid = request.GET["uuid"]
    studies = request.GET["studies"]
    species = request.GET["species"]
    if os.path.isfile(uuid):
        #Check result
        time.sleep(1)
        cur_result = json.load(open(uuid,'r'))
        while True:
            try:
                cur_result = json.load(open(uuid,'r'))
                break
            except:
                continue

        cur_progress, status, no_sample_warning = calc_query_sample_progress(cur_result, uuid)
        return HttpResponse(json.dumps({'cur_progress':cur_progress, 'status': status, 'no_sample_warning' : no_sample_warning})) 
    else:
        #Query did not start correctly:
        return HttpResponse(json.dumps({'cur_progress':-2}))


@csrf_exempt
def show_sample_query_result_page(request):
    if request.method == 'GET':
        return show_sample_query_result_page_get(request)
    else:
        return show_sample_query_result_page_post(request)
        
def show_sample_query_result_table(request):
    uuid = request.GET["uuid"]
    result = pd.read_csv(uuid+'_sample_output.csv',index_col = False)
    result = result.reset_index(drop=True)
    return HttpResponse(result.to_json(orient='split',index=False))
    
def show_sample_query_result_page_get(request):
    #Show the sample query result
    uuid = request.GET["uuid"]
    result = pd.read_csv(uuid+'_sample_output.csv',index_col = False)
    studies = request.GET["studies"]
    species = request.GET["species"]
    
    col_name = result.columns
    table_header = '<thead><tr>\n'
    table_header = table_header + '<th><input name="select_all" value="1" id="example-select-all" type="checkbox" checked/></th>'
    
    for i in range(len(col_name)):
        if i == 0:
            continue
        table_header = table_header + '<th>' + col_name[i] + '</th>' + '\n'
    table_header = table_header + '</tr></thead>'


    return render(request, 'show_sample_query_result.html', {'table_header': table_header, 'target_url': "'table/?uuid=" + uuid + "'",'uuid':"'"+uuid+"'"})

    
def show_sample_query_result_page_post(request):
    #Confirm the sample query selection and go to the next step (select reference genome)
    uuid = request.GET["uuid"]
    result = pd.read_csv(uuid+'_sample_output.csv',index_col = False)
    #Obtain the datatable from the website
    tmp = request.POST.get('data')
    tmp = tmp.split(',')
    tmp = [int(e) for e in tmp]
    tmp = bytearray(tmp)
    tmp = tmp.decode('utf-8')
    tmp = json.loads(tmp)
    tmp = tmp['data']

    new_result_list = []
    for i in range(len(tmp)):
        new_result_list.append(pd.Series(tmp[str(i)]))

    new_result = pd.concat(new_result_list,axis=1)
    new_result.columns = result.columns
    result = new_result
    result.to_csv(uuid+'_sample_output.csv',index = False)
    #Return Nothing ==> now the javascript should redirect the page to the next step
    return HttpResponse(json.dumps(None))
    
@csrf_exempt
def update_sample_selection(request):
    #User upload the csv file and then update the sample selection
    uuid = request.GET["uuid"]
    result = pd.read_csv(uuid+'_sample_output.csv',index_col = False)
    if request.method == 'POST':
        #Obtain the file from user
        tmp_file = tempfile.NamedTemporaryFile(delete=False)
        for chunk in request.FILES['table_file_for_update'].chunks():
            tmp_file.write(chunk)
        tmp_file.close()
        new_result = pd.read_csv(tmp_file.name,index_col = False, engine='python')
        os.unlink(tmp_file.name)

        for i in range(len(new_result.columns)):
            if i == 0:
                continue
            if new_result.columns[i] != result.columns[i]:
                raise Exception
        result = new_result
        result.to_csv(uuid+'_sample_output.csv',index=False)
        #Return Nothing ==> now the javascript should refresh the page
        return HttpResponse(json.dumps(None))
    else:
        #This should not happen
        raise Exception
    

@csrf_exempt
def show_refgen_query_result_page(request):
    if request.method == 'GET':
        return show_refgen_query_result_page_get(request)
    else:
        return show_refgen_query_result_page_post(request)
        
def show_refgen_query_result_table(request):
    uuid = request.GET["uuid"]
    result = pd.read_csv(uuid+'_refgen_output.csv')
    result = result.reset_index(drop=True)
    return HttpResponse(result.to_json(orient='split',index=False))
    
def show_refgen_query_result_page_get(request):
    #Show the refgen query result
    uuid = request.GET["uuid"]
    result = pd.read_csv(uuid+'_refgen_output.csv')
    studies = request.GET["studies"]
    species = request.GET["species"]
    
    col_name = result.columns
    table_header = '<thead><tr>\n'
    
    for i in range(len(col_name)):
        if i == 0:
            continue
        table_header = table_header + '<th>' + col_name[i] + '</th>' + '\n'
    table_header = table_header + '</tr></thead>'
    return render(request, 'show_refgen_query_result.html', {'table_header': table_header, 'target_url': "'table/?uuid=" + uuid + "'",'uuid':"'"+uuid+"'"})

    
def show_refgen_query_result_page_post(request):
    #Confirm the refgen selection and go to the next step (download and show feature table)
    #Start downloading the feature table
    uuid = request.GET["uuid"]
    ftpurl = request.GET["ftpurl"]
    
    query_result = init_feature_table_download_result()
    json.dump(query_result,open(uuid,'w'))

    cur_subprocess = subprocess.Popen(['python3','download_parse_featuretable.py',ftpurl,uuid])
    query_result['pid'] = cur_subprocess.pid
    json.dump(query_result,open(uuid,'w'))
    while os.path.isfile(uuid) == False:
        #Wait until the file is created
        continue
    #Return Nothing ==> now the javascript should submit the query to check the progress
    return HttpResponse(json.dumps(None))
    
    
def check_progress_download_feature_table(request):
    uuid = request.GET["uuid"]
    studies = request.GET["studies"]
    species = request.GET["species"]
    ftpurl = request.GET["ftpurl"]

    target_file = uuid + ".csv"

    if os.path.isfile(uuid):
        #Check result
        time.sleep(1)
        cur_result = json.load(open(uuid,'r'))
        while True:
            try:
                cur_result = json.load(open(uuid,'r'))
                break
            except:
                continue
        
        cur_progress = calc_feature_table_download_progress(cur_result)
        return HttpResponse(json.dumps({'cur_progress':cur_progress})) 
        
    else:
        #Should not happen
        raise Exception
        
@csrf_exempt
def show_feature_table_page(request):
    if request.method == 'GET':
        return show_feature_table_page_get(request)
    else:
        return show_feature_table_page_post(request)
        
def show_feature_table_page_get(request):
    uuid = request.GET["uuid"]
    studies = request.GET["studies"]
    species = request.GET["species"]
    
    result = pd.read_csv(uuid+'_parsed.csv',index_col=False)
    col_name = result.columns 
    table_header = '<thead><tr>\n'
    
    for i in range(len(col_name)):
        table_header = table_header + '<th>' + col_name[i] + '</th>' + '\n'
    table_header = table_header + '</tr></thead>'
    return render(request, 'show_feature_table_result.html', {'table_header': table_header, 'target_url': "'table/?uuid=" + uuid + "'",'uuid':"'"+uuid+"'"})


def show_feature_table_page_post(request):
    uuid = request.GET["uuid"]
    #Submit the job to the cluster
    if len(request.FILES) == 3:
        tmp_corr_file = uuid+'_corr_file.csv'
        tmp_knowledge_capture_sample_file = uuid+'_knowledge_capture_sample_file.csv'
        tmp_knowledge_capture_gene_file = uuid+'_knowledge_capture_gene_file.csv'

        with open(tmp_corr_file,'wb') as fp:
            for chunk in request.FILES['cor_file'].chunks():
                fp.write(chunk)

        with open(tmp_knowledge_capture_sample_file,'wb') as fp:
            for chunk in request.FILES['knowledge_capture_sample_file'].chunks():
                fp.write(chunk)

        with open(tmp_knowledge_capture_gene_file,'wb') as fp:
            for chunk in request.FILES['knowledge_capture_gene_file'].chunks():
                fp.write(chunk)

        try:
            email = request.POST['email']
            gff_url = request.POST['gff_url']
        except:
            raise Exception

        print(gff_url)
        print(tmp_corr_file)
        print(tmp_knowledge_capture_sample_file)
        print(tmp_knowledge_capture_gene_file)
        print(email)
        subprocess.Popen([
            './submit_to_hpc1_new.sh',
            gff_url,
            tmp_corr_file,
            tmp_knowledge_capture_sample_file,
            tmp_knowledge_capture_gene_file,
            uuid+'_sample_output.csv',
            email,
            uuid
            ])
            
        #Return Nothing ==> now the javascript should check the progress
        return HttpResponse(json.dumps(None))
    else:
        raise Exception
    
    
def show_feature_table(request):
    uuid = request.GET["uuid"]
    result = pd.read_csv(uuid+'_parsed.csv',index_col=False)
     
    return HttpResponse(result.to_json(orient='split',index=False))
    
def check_progress_submit_job(request):
    pass

def show_submitted_page(request):
    return render(request, 'submitted.html', {'user_pr': ''})



