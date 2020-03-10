# Step-by-step example
<h4>This example provides a step-by-step example to make a Salmonella example compendium.</h4>

## Necessary files in this example:
There are some necessary files for compendium building and supervised validation.
<ol>
    <li>Sample list files (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/SalmonellaExampleSampleList.csv>SalmonellaExampleSampleList.csv</a>)
        <ul>
            <li>The samples (SRA experiment IDs in SRA database) you are interested in for building a compendium.</li>
        </ul>
    </li>
    <li>Gene annotation files of reference genome (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/GCF_000006945.2_ASM694v2> GCF_000006945.2_ASM694v2 </a>)
        <ul>
            <li>A gff file contains metadata information including gene names and positions of all chromosome and plasmid.</li>
            <li>The pipeline will fetch all corresponded sequence from NCBI database using this metadata.</li>
        </ul>
    </li>
    <li>Supervised validation (knowledge capture validation) files:
        <ol>
            <li>fur gene mutant vs wildtype
                <ul>
                    <li>Selected sample list (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/Input_KnowledgeCapture_fur.csv>Input_KnowledgeCapture_fur.csv</a>) </li>
                    <li>Selected gene list (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/Input_KnowledgeCapture_fur_related_genes.csv>Input_KnowledgeCapture_fur_related_genes.csv</a>) </li>
                </ul>
            </li>
            <li>hfq gene mutant vs wildtype
                <ul>
                    <li>Selected sample list (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/Input_KnowledgeCapture_hfq.csv>Input_KnowledgeCapture_hfq.csv</a>) </li>
                    <li>Selected gene list (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/Input_KnowledgeCapture_hfq_related_genes.csv>Input_KnowledgeCapture_hfq_related_genes.csv</a>) </li>
                </ul>
            </li>
        </ol>
    </li>
    <li>Supervised validation (published data comparison) files:
        <ul>
            <li><a href=https://www.sciencedirect.com/science/article/pii/S1931312813004113">Reference compendium for comparison.</a>
                <ul>
                    <li>Original dataset (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/SampleTable_GoldenStandard.csv>SampleTable_GoldenStandard.csv</a>) </li>
                    <li>Format refined dataset (<a href = https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TestFiles/SampleTable_STM_GoldenStandard.csv>SampleTable_STM_GoldenStandard.csv</a>) </li>
                </ul>
            </li>
        </ul>
    </li>
</ol>

## 0. Installation
Please make sure you have installed all the packages, software and set the environment variables correctly. (<a href=https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/tree/Pipeline_20200307>Please refer the main description.</a>)

## 1. Parameters configurations (t_utilities/t_parameters.py)
This step shows you how to modify some important variables which is necessary for building and validating a compendium. To configure the parameters, please open the parameter setting file. (<a href=https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/TranscriptomicPipelines/t_utilities/t_parameters.py>t_utilities/t_parameters.py</a>)
<br>There are two classes: 
<ul>
    <li>TranscriptomicConstants: It records the constants, especially some option strings inside the pipeline.</li>
    <li>TranscriptomicParameters: It records the parameters. Some options can be found in the class TranscriptomicConstants.</li>
</ul>

### 1.1 Parallel options
There are four time consuming procedures which can be run in parallel:
<ol>
    <li>Reference genome building (corresponded parameter: self.s_value_extraction_refbuild_parameters_parallel_mode)</li>
    <li>Sequencing value extraction (corresponded parameter: self.s_value_extraction_parallel_parameters_parallel_mode)</li>
    <li>Sample mapping (corresponded parameter: self.s_sample_mapping_parallel_parameters_parallel_mode)</li>
    <li>Missing value imputation (corresponded parameter: self.p_imputation_rfimpute_parallel_parameters_parallel_mode)</li>
</ol>

There are two options for parallelization:
<ol>
    <li>local(corresponded option: self.constants.parallel_option_local): The pipeline will run in parallel in the local machine.</li>
    <li>slurm(corresponded option: self.constants.parallel_option_slurm): The pipeline will submit the job to the computation node in cluster via slurm.</li>
</ol>

If you do not have slurm installed in your computer, please change the option as follows in this file:
```
self.s_value_extraction_refbuild_parameters_parallel_mode = self.constants.parallel_option_local
...
self.s_value_extraction_parallel_parameters_parallel_mode = self.constants.parallel_option_local
...
self.s_sample_mapping_parallel_parameters_parallel_mode = self.constants.parallel_option_local
...
self.p_imputation_rfimpute_parallel_parameters_parallel_mode = self.constants.parallel_option_local
```
