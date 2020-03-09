# Validation of the compendium
<h4>Before you read this part, please make sure you read the <a href=https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/tree/Pipeline_20200307>main documentation first.</a></h4>
<h4>Please read step-by-step example for more information. </h4><br>
It is important to validate and check the quality of the compendium. There are one supervised approach and three unsupervised approaches to check the quality or validate the compendium you built.

## Unsupervised approaches
<h4>Unsupervised approaches can evaluate one or more benchmarks of the compendium you built based on several assumptions. Users do not have to provide additional information to obtain the benchmark.</h4>

### Drop and impute values approach

#### Assumptions
<h4>Based on the following two assumtpions, drop and impute values approach can evaluate a benchmark to evaluate the quality of the compendium.</h4>
<ol>
    <li>A good compendium should capture the pattern of gene expression profiles. Therefore, even if some values are dropped, we still can recover these missing values by applying missing value imputation.</li>
    <li>If a compendium is perturbed, it is more difficult to recover the missing values and yield larger error.</li>
</ol>

#### Steps
<h4>There are four steps for drop and impute values approach:</h4>


![Figure V1. Drop and impute values approach](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/images/Figure2.png)
Figure V1. Drop and impute values approach
