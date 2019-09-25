
# AutomatedOmicsCompendiumPreparationPipeline
This toolkit can prepare the compendium by collecting the samples in <a href="https://www.ncbi.nlm.nih.gov/sra">Sequencing Read Archive (SRA) </a> database.
(In the future, this toolkit will be capable to process microarray dataset from GEO and ArrayExpress database)

<div id = "usage">
<h1> How to use it </h1>
<ol>
<li> Download all <a href="#software">necessary software and toolkits</a> </li>
<li> Add all installed software to PATH environment variables </li>
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


<div id = "validation">
<h3>Validation Part</h3>
Need to be updated...
</div>