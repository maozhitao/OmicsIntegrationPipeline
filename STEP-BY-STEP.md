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