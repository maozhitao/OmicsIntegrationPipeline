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
<ol>
    <li>Add the noise to the normalized data matrix in the compendium with different noise ratio.
        <ul>
            <li>The noise for adding is from random permutation results of normalized data matrix to make sure that the noise has the same distribution as the original data matrix.</li>
            <li>The noise ratio is a value between 0 and 1.
            <ul>
                <li>If noise ratio is 0, it means that there is no noise to be added.</li>
                <li>If noise ratio is 1, it means that the data matrix is totally perturbed by random permutation.</li>
                <li>If noise ratio is between 0 and 1 (0 < x < 1, x is noise ratio), it means that the data matrix will be generated from the linear combination of original data matrix and noise:<br><br>
                    x*(noise) + (1-x)*(original data matrix)
                </li>
            </ul>
        </ul>
    </li>
    <li>Randomly remove the values in the noise-added data matrix with different missing value ratio.</li>
    <li>Run the missing value imputation to fill the missing value back.<br>
        There are two approaches to impute the missing value in the pipeline:
        <ul>
            <li>K-nearest neighborhood (KNN)</li>
            <li>Missing Forest</li>
        </ul>
        The pipeline use missingpy to perform these two imputation approaches. Please refer <a href=https://pypi.org/project/missingpy/>the package description</a> for more information.
    </li>
    <li>Calculate the error between imputed values and the original values before dropping.
        <ul>
            <li>There will be a error table recording the error of values for each noise ratio. By taking the average, the pipeline can get the average error of this noise ratio.</li>
            <li>There will be a average error table recording the average error of different noise ratio for each missing value ratio. Each table can be plotted as a noise ratio vs. average error curve.</li>
        </ul>
    </li> 
</ol>

![Figure V1. Four steps of drop and impute values approach](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/images/Figure2.png)
Figure V1. Four steps of drop and impute values approach

#### Benchmark evaluation
<h4> After we get the average error curve, the next thing is the benchmark evaluation.</h4>
<ul>
    <li>We can pick a curve (for example, a curve from missing value ratio = 0.5) and then calculate the area below this curve.
        <ul>
            <li>The large area means bad compendium quality due to that high error of missing value imputation.</li>
        </ul>
    </li>
    <li>Or, we can calculate the area between the selected curve and the reference line (for example, a horizontal line with 100% error).
        <ul>
            <li>The large area means good compendium quality due to that low error of missing value imputation.</li>
        </ul>
    </li>
</ul>
<h4>Current pipeline use the second defination as the benchmark.</h4>

![Figure V2. Benchmark evaluation of drop and impute values approach](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/images/Unsupervised_validation_description.png)
Figure V2. Benchmark evaluation of drop and impute values approach. The area between 100% error horizontal line and the error curve from missing value ratio = 0.5 (orange line) is evaluated as the benchmark.

</h4>


