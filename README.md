

# Automated Omics Compendium Preparation Pipeline

<h1> Propose</h1>
This toolkit can prepare the compendium by collecting the samples in <a href="https://www.ncbi.nlm.nih.gov/sra">Sequencing Read Archive (SRA) </a> database.
(In the future, this toolkit will be capable to process microarray dataset from GEO and ArrayExpress database)

![Figure 1. The entire transcriptomic compendium pipeline](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/pipeline_20200102/images/Figure1.png)


<div id = "usage">
<h1> How to use it </h1>
<ol>
<li> Download all <a href="#software">necessary software and toolkits</a> </li>
<li> Add all installed software to <a href="#path_env">PATH environment variables</a> </li>
<li> Download the entire directory of this project </li>
<li> Prepare a list of experiment ID you would like to collect (<a href="https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/master/TestFiles/input_exp1.txt">example</a>)</li>
<li> Download the template files from NCBI genome database in GFF3 format (<a href="https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/master/TestFiles/LT2.gff3">example</a>) </li>
<li> Prepare a list of templates for alignment (<a href="https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/master/TestFiles/input_template1.txt">example</a>) </li>
<li> Configure the parameter set in <a href="https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/master/TranscriptomicPipelines/t_utilities/t_parameters.py">t_utilities/t_parameters.py</a></li>
<li> Execute the main program: <a href="https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/master/TranscriptomicPipelines/transcriptomic_pipeline.py">transcriptomic_pipeline.py</a> &lt;experiment_idlist_file&gt; &lt;template_list_file&gt; </li>
<li> For the validation part, please refer <a href="#validation">validation part</a></li>
</ol>
</div>

<div id = "software">
<h3>Required Software</h3>
<ol>
<li>Python3 (>=3.6.9) or Python2 (>=2.7.1)</li>
<li>sratoolkit (>=2.9.6) </li>
</ol>

<h3>Required Packages</h3>
<ol>
<li>biopython (>=1.74)</li>
<li>pandas (>=0.25.0)</li>
<li>RSeQC (For Python3: >=3.0.0, For Python2: 2.6.4)</li>
<li>HTSeq (>=0.11.2) </li>
</ol>
</div>

<div id = "path_env">
<h3>PATH environment variable settings</h3>
You should add all path of installed toolkits to PATH environment variables <br>
(Especially when you do not have root privileges and you install or compile the software/toolkits manually): <br>
Here are the example path of those installed software/toolkits:
<ol>
<li> sratoolkit: ~/sratoolkit.2.9.6-1-ubuntu64/bin/ </li>
<li> RSeQC: ~/.local/lib/python2.7/site-packages/RSeQC-2.6.4-py2.7.egg/EGG-INFO/scripts/ </li>
<li> HTSeq: ~/.local/lib/python2.7/site-packages/HTSeq-0.6.1p1-py2.7-linux-x86_64.egg/EGG-INFO/scripts/</li>
</ol>
After you added these path to PATH variable, you should be capable to run the following program in any directory:
<ul>
<li>prefetch</li>
<li>infer_experiment.py</li>
<li>htseq_count</li>
</ul>
If you failed to run these three program, please make sure that you located these three programs correctly and added the correct path to PATH variables before you run this pipeline.
</div>

<div id = "validation">
<h1>Validation Part</h1>
To evaluate the quality of the compendium, unsupervised and supervised approach are applied:

<h3>Unsupervised validation</h3>
Unsupervised validation evaluate the model quality without additional information from the metadata. The assumption is that the high quality data collected from the same species contains general gene expression pattern regardless of the culture conditions.
Therefore, after intentionally remove partial data, the remain part of the data should be capable to recover the missing part.
</div>

![Figure 2. The demonstration of unsupervised validation. The transcription profiles in the compendium are added with noise in different noise ratio and then some values are removed randomly. The imputation method then recover the values. Then the imputed values can be compared with the original values. For the high quality compendium, the difference between original value and imputed value in low noise ratio cases should be significantly lower than the difference in high noise ratio cases.](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/pipeline_20200102/images/Figure2.png)


