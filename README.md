# Automated Omics Compendium Preparation Pipeline

## Propose
This toolkit can prepare the transcriptomic compendium (a normalized, format-consistent data matrix across samples from different studies) by collecting the samples in <a href="https://www.ncbi.nlm.nih.gov/sra">Sequencing Read Archive (SRA) </a> database given the topic you are interested in and your target species.

(In the future, this toolkit will be capable to process microarray dataset from GEO and ArrayExpress database)

## Steps of preparing a transcriptomic compendium
The pipeline will do the necessary work for building transcriptomic compendium for you in five steps:<br>
<b>(To check the exact format, please read "Step-by-Step example")</b>

### 1. Metadata preparation
<h4>This step will take two user inputs to prepare all necessary metadata for sequencing data processing: </h4>
    <ol>
        <li>Sample List: The list that contains samples (experiment ID in SRA database) you are interested in.</li>
        <li>Gene Annotation File: A GFF file downloaded from NCBI genome database. This annotation file allow the pipeline to fetch reference genome sequence and extract the corresponded gene names.</li>
    </ol>
<h4>The output metadata will contain all necessary information for sequencing data processing: </h4>
    <ol>
        <li>Run information in SRA database: It contains corresponded run information for samples you are interested in. One sample (experiment ID) may contain more than one runs.</li>
        <li>Reference genome files: Files in Bowtie2 index format to allow the pipeline align the sequencing data with this reference.</li>
        <li>Reference genome sequence direction information: A BED file to allow the pipeline detect the sequencing data type (stranded or unstranded). </li>
    </ol>
    
### 2. Sequencing data download
<h4>This step will take run information input and then download all sequencing data of samples you are interested in from SRA database: </h4>
    <ul>
        <li>Run information in SRA database: Generated from step (1) and contains corresponded run information for samples you are interested in.</li>
    </ul>
<h4> The output files are downloaded and format-converted sequencing data: </h4>
    <ul>
        <li>Sequencing data: Fastq files for each run. Two files for one run if this run is paired-end data, otherwise each run will generate one fastq file.
    </ul>

### 3. Sequencing data alignment
<h4>This step will take sequencing data and reference genome files as inputs to perform sequence alignment:</h4>
    <ol>
        <li>Sequencing data: Generated from step (2). Fastq files for each run.</li>
        <li>Reference genome files: Generated from step(1). Reference genome sequence for alignment.</li>
    </ol>
<h4>The output file is alignment results is SAM format and alignment rates:</h4>
    <ol>
        <li>The alignment result files: For each run, a file contains the alignment result in SAM format is generated.</li>
        <li>Alignment rate information: Alignment rate information will be recorded (for internal use only).</li>
    </ol>

### 4. Gene expression counting
<h4>This step will take gene alignment results, sequence direction information file (BED file) and gene annotation file (GFF file) as inputs to generate the gene expression profile for each run.<br></h4>
    <ol>
        <li>The alignment result files: Files in SAM format generated from step (3) which recorded the alignment result.</li>
        <li>BED file contains sequence direction information: A file in BED format generated from step (1). With this sequence direction information, the pipeline can detect whether sequencing data is stranded or unstranded.</li>
        <li>GFF file contains gene annotation information: A file in GFF format given from users. With this information, the pipeline can generate gene expression profiles with correct gene names.</li>
    </ol>
<h4>The output file are the gene expression profiles of different runs. After perform the mapping between runs and samples with run information table (generated from step (1)), gene expression profile for each sample can be generated.</h4>
    <ol>
        <li>Gene expression profiles of different runs (for internal use only).</li>
        <li>Gene expression profiles of different samples after performing the mapping between runs and samples with run information table (for internal use only).</li>
        <li>Gene expression profile table: A table in csv format contains gene expression profiles of all samples you are interested in after concatenating all gene expression profiles of different samples.<br>
            Each row represent different genes and each column represent different samples.
        </li>
    </ol>
    
### 5. Data normalization
<h4>This step will take the gene expression profile table as input and perform normalization to reduce the error across different studies.<br></h4>
    <ul>
        <li>Gene expression profile table: Generated from step (4). A table in csv format contains gene expression profiles of all samples you are interested in</li>
    </ul>
<h4>The output file are the normalized gene expression profile table. In addition, a binary file recorded the normalized gene expression table and all parameters are saved.<br></h4>
    <ol>
        <li>Normalized gene expression profile table: A table in csv format contains normalized gene expression profiles of all samples.</li>
        <li>Compendium saved in binary format: A python object contains the normalized gene expression table and recorded parameters. It can be used for the next step -- optional validation.</li>
    </ol>
    
### 6. Optional validation (Please read the document about validation and step-by-step examples for more information.)
<h4>This optional step will estimate the quality of normalized gene expression table. Unsupervised approaches and supervised approaches are provided.</h4>

![Figure 1. The entire transcriptomic compendium pipeline](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/images/Figure1.png)
Figure 1. The entire transcriptomic compendium pipeline



## Configuration before using
<h4> To use this pipeline, you have to download the entire directory, install all required software and python packages. <h4>

### Download the entire directory
Please clone the entire repository into your computer.

### Install all required software
Required software have to be installed.

#### 1. Python 3.6 or later (NOTE: This version does not support Python 2 anymore)
<h4>Please download and install python 3 by following the instructions in official website:<br>
( https://www.python.org/downloads/ )</h4>
    <ul>
        <li>Tested in Python 3.6 </li>
    </ul>
    
#### 2. sratoolkit 2.9.6 or later
<h4>Please download and install sratoolkit by following the instructions in official website:<br>
( https://ncbi.github.io/sra-tools/install_config.html )</h4>
    <ul>
        <li>Tested with sratoolkit 2.9.6 </li>
        <li>Please make sure the toolkit location is specified in your $PATH variable. To add the toolkit location:
            <ul>
                <li>Linux: Use export command:
                
                    
    export PATH=<your_toolkit_location>:$PATH
                    
                    
</li>
                
<li>Windows 10: please follow these steps:
        <ol>
            <li>Open "Control Panel".</li>
            <li>Click "System".</li>
            <li>Click "About", and then click "System info" at the bottom of the page. </li>
            <li>Click "Advanced system settings" at the right of the system info page. </li>
            <li>Click "Environment Variables..." Button in advanced system settings window. </li>
            <li>Now you can add the toolkit location to PATH variable in Windows 10.</li>
        </ol>
</li>
</ul>
</li>
</ul>

#### 3. Bowtie 2.3.4 or later
<h4>Please download and install Bowtie2 by following the instructions in official website:<br>
( http://bowtie-bio.sourceforge.net/bowtie2/index.shtml )</h4>
    <ul>
        <li>Tested with Bowtie 2.3.4</li>
        <li>Please make sure the toolkit location is specified in your $PATH variable. (As installing sratoolkit)</li>
    </ul>

### Install all required Python packages
Required python packages have to be installed.

#### 1. biopython
<h4>Please install biopython by following the instructions in official website:<br>
( https://biopython.org/wiki/Download )</h4>
    <ul>
        <li>Tested with biopython 1.74</li>
    </ul>

#### 2. pandas
<h4>Please install pandas by following the instructions in official website:<br>
( https://pandas.pydata.org/docs/getting_started/install.html#installing-pandas )</h4>
    <ul>
        <li>Tested with pandas 0.25.0</li>
    </ul>
    
#### 3. RSeQC
<h4>Please install RSeQC by following the instructions in official website:<br>
( http://rseqc.sourceforge.net/#download-rseqc )</h4>
    <ul>
        <li>Tested with RSeQC 3.0.0</li>
        <li>Please make sure the location of 'infer_experiment.py' is specified in your $PATH variable. (As installing sratoolkit)</li>
            <ul>
                <li>(Example location: '~/.local/bin')</li>
            </ul>
    </ul>
    
#### 4. HTSeq
<h4>Please install HTSeq by following the instructions in official website:<br>
( https://htseq.readthedocs.io/en/master/ )</h4>
    <ul>
        <li>Tested with HTSeq 0.11.2</li>
        <li>Please make sure the location of 'htseq-count' is specified in your $PATH variable. (As installing sratoolkit)</li>
            <ul>
                <li>(Example location: '~/.local/bin')</li>
            </ul>
    </ul>
    
### Testing after install and configure your computer
<h4>After you added these path to PATH variable, you should be capable to run the following program in any directory:</h4>
<ul>
    <li>prefetch</li>
    <li>bowtie2</li>
    <li>infer_experiment.py</li>
    <li>htseq_count</li>
</ul>
<h4>If you failed to run these four programs, please make sure that you located these four programs correctly and added the correct path to PATH variables before you run this pipeline.</h4>

    
## How to use it
<h4>Please refer step-by-step example for more information</h4>

### Building compendium script (Main script)
<h4>This script is the main script and will take sample list and a gene annotation file as inputs to build the compendium</h4>

#### Input
This script takes two input files and one additional argument:
<ul>
    <li> Input files:
        <ol>
            <li>Sample List: A file in csv format with one column with name "Experiment". (Please refer figure 1).(<a href="https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/SalmonellaExampleSampleList.csv">Example</a>)</li>
            <li>Gene Annotation: A file in gff3 format downloaded from NCBI genome database. (Please refer figure 1)(<a href="ftp://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/006/945/GCA_000006945.2_ASM694v2/GCA_000006945.2_ASM694v2_genomic.gff.gz">Example (need decompression)</a>)</li>
        </ol>
    </li>
    <li> One additional argument:
        <ul>
            <li>Compendium name: The name you want. The pipeline will create a directory with this name and store all results in this directory.</li>
        </ul>
    </li>
</ul>

#### Output
This script will generate a directory with specified compendium name and many files in the directory. There are two the most important files:
<ul>
    <li>Normalized Data Matrix (Filename: '(Compendium Name)_NormalizedDataMatrix.csv'): A table in csv format contains normalized gene expression profiles of all samples. Each row represent different genes and each column represent different samples. (Please refer step (5) and figure 1)</li>
    <li>Compendium saved in binary format (Filename: '(Compendium Name)_projectfile.bin'): A python object contains the normalized gene expression table and recorded parameters. It can be used for optional validation. (Please refer step (5) and figure 1)</li>
</ul>

<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/raw/Pipeline_20200307/SalmonellaExample.tar.gz>Salmonella compendium example including validation results (need decompression)</a>
#### Usage

```
python build_compendium_script.py <sample list file path> <gene annotation file path> <compendium name>
```

### Unsupervised validation script
<h4>Please refer step-by-step example and validation description for more information</h4>

#### Input
This script takes only one input: Your compendium name.

#### Output
This script will generate two files in your compendium directory.
<ul>
    <li></li>
    <li></li>
</ul>



<div id = "validation">
<h1>Validation Part</h1>
To evaluate the quality of the compendium, unsupervised and supervised approach are applied:

<h3>Unsupervised validation</h3>
Unsupervised validation evaluate the model quality without additional information from the metadata. The assumption is that the high quality data collected from the same species contains general gene expression pattern regardless of the culture conditions.
Therefore, after intentionally remove partial data, the remain part of the data should be capable to recover the missing part.


![Figure 2. The demonstration of unsupervised validation. The transcription profiles in the compendium are added with noise in different noise ratio and then some values are removed randomly. The imputation method then recover the values. Then the imputed values can be compared with the original values. For the high quality compendium, the difference between original value and imputed value in low noise ratio cases should be significantly lower than the difference in high noise ratio cases.](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/pipeline_20200102/images/Figure2.png)
Figure 2. The demonstration of unsupervised validation. The transcription profiles in the compendium are added with noise in different noise ratio and then some values are removed randomly. The imputation method then recover the values. Then the imputed values can be compared with the original values. For the high quality compendium, the difference between original value and imputed value in low noise ratio cases should be significantly lower than the difference in high noise ratio cases.

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
<li>Knowledge capture: If you know the genes that expressed significantly different in two specific conditions, you can provide the list of the genes and two sample lists of these two specific conditions. The pipeline will check whether the selected genes expressed significantly different in two specific conditions. <br> For example, we know that fur gene in Salmonella can regulate flagellar genes, SPI1 genes and SPI2 genes (<a href="https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5001712/">PMC5001712</a>). In addition, we know that samples SRX1638996 and SRX1638997 are wildtype and SRX1638999 is fur mutant. By providing these three information: gene list, sample list of wildtype conditions and sample list of fur mutant, the pipeline will be capable to verify whether the compendium capture the information. The procedures are shown in figure 4:

<ol>
<li>Samples from two sample list of two different conditions are selected.</li>
<li>The average profiles of these two conditions will be calculated.</li>
<li>The absolute log fold change between these two conditions will be calculated.</li>
<li>The corresponded rank will be calculated.</li>
<li>Given the genes that expressed significantly different in these two specific conditions. We can pick the rank of the specified genes.</li>
<li>The cumulative density function (cdf) of the rank of selected genes can be plotted. The baseline will be the diagonal line, which is the cdf of uniform distribution. The cumulative density function from good compendium should be significantly different then uniform distribution. (Significant p-value should be obtained by performing Kolmogorov–Smirnov test (K-S test))</li>
</ol>

![Figure 4. The demonstration of knowledge capture validation. ](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/pipeline_20200102/images/Figure4.png)
Figure 4. The demonstration of knowledge capture validation.
</li>
</ol>


</div>