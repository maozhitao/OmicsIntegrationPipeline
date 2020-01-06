

# Automated Omics Compendium Preparation Pipeline

<h1> Propose</h1>
This toolkit can prepare the transcriptomic compendium by collecting the samples in <a href="https://www.ncbi.nlm.nih.gov/sra">Sequencing Read Archive (SRA) </a> database given the topic you are interested in and your target species.

(In the future, this toolkit will be capable to process microarray dataset from GEO and ArrayExpress database)

The pipeline will do the necessary work for building transcriptomic compendium for you in five steps:

<ol>
<li>Given the topic your are interested in, the pipeline will find the corresponded experiments in SRA database.</li>
<li>Given your targeted species, the pipeline will find the corresponded reference genome sequence and mRNA annotation information.</li>
<li>Given the collected experiments (and optional experiment filter list), reference genome sequence and mRNA annotation information, the pipeline will download the RNA-seq data from SRA, and then count the reads for each mRNA to create the transcription profiles.</li>
<li>After the transcription profiles are ready, quantile normalization will be applied to reduce the batch effect among different experiments.</li>
<li>Finally, the validation module will evaluate the quality of the compendium. If additional metadata are provided (see validation part), both supervised validation and unsupervised validation will be applied. Otherwise, only unsupervised validation will be applied.</li>
</ol>

![Figure 1. The entire transcriptomic compendium pipeline](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/pipeline_20200102/images/Figure1.png)
Figure 1. The entire transcriptomic compendium pipeline

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


![Figure 2. The demonstration of unsupervised validation. The transcription profiles in the compendium are added with noise in different noise ratio and then some values are removed randomly. The imputation method then recover the values. Then the imputed values can be compared with the original values. For the high quality compendium, the difference between original value and imputed value in low noise ratio cases should be significantly lower than the difference in high noise ratio cases.](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/pipeline_20200102/images/Figure2.png)

<h3>Supervised validation</h3>
Supervised validation can provide more information of compendium quality evaluation. However, it needs more metadata curated by human. The pipeline provides two approaches for supervised validation

<ol>
<li>Correlation validation: If you know the mapping between experiments and studies (or conditions), you can provide this information to the pipeline. The assumption is that the similarity between two transcription profiles should be high if they are from the same conditions. And then the similarity between two profiles should be high (but lower than the similarity if they are from the exact same condition) if they are from the same study because many factors (tissues, sample source, etc.) are the same. The similarity should be low if they are from the different studies.<br><br>The pipeline evaluate five types of average correlations:
<ol>
<li>Average correlation among all profiles: It will calculate all pairwise correlation in the compendium. Since it calculates all pairwise correlation including the correlation between two profiles from different conditions and studies, this value should be the lowest compared with different types of average correlation.</li>
<li>Average correlation among profiles from the same conditions: It will calculate all pairwise correlation of the profiles from the same conditions. This value should be the highest because it only calculates correlations among profiles from the same conditions</li>
<li>Average correlation among profiles from the same studies: It will calculate all pairwise correlation of the profiles from the same studies.<br>
For the normal compendium, (2) should be the highest and (1) should be the lowest. <br><br>
The following two average correlations show the diversity of the compendium. <br>
</li>
<li>Average correlation across different studies: For each study, all corresponded profiles are merged into representative one by taking the average. Then average correlation among different studies are calculated.</li>
<li>Average correlation across different conditions: For each condition, all corresponded profiles are merged into representative one by taking the average. Then average correlation among different conditions are calculated.</li>
</ol>
By evaluating these five types of average correlation and compared among them, abnormal compendium can be observed. In addition, noise can be added into the compendium and these five values should decrease. <br> Figure 3. shows the entire flow of the correlation validation procedure. 
<ol>
<li>At the beginning, the compendium contains six samples from three different conditions and two different studies. </li>
<li>The correlation matrix are calculated. Three different average correlation are calculated: The average of all 36 values become the average correlation among all profiles (Black); The average of 20 values from the same studies become the average correlation among profiles from the same studies (Green); The average of 12 values from the same conditions become the average correlation among profiles from the same conditions (Orange) </li>
<li>Then, the average transcription profiles for each condition (Blue) and for each study (Red) are calculated.</li>
<li>The corresponded correlation matrices are also calculated. The average values of these correlation matrices become the average correlation across different studies/conditions.
</li>
<li>Adding noise with higher noise ratio decrease the correlation. The corresponded plot will be shown.</li>
</ol>


![Figure 3. The demonstration of correlation validation. ](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/pipeline_20200102/images/Figure3.png)
Figure 3. The demonstration of correlation validation.
</li>
 2. List item
</ol>
 1. 
 3. 

</div>