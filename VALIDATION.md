# Validation of the compendium
<h4>Before you read this part, please make sure you read the <a href=https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/tree/Pipeline_20200307>main documentation first.</a></h4>
<h4>Please read step-by-step example for more information. </h4>
It is important to validate and check the quality of the compendium. There are one supervised approach and three unsupervised approaches to check the quality or validate the compendium you built.

## An unsupervised approach -- Drop and impute values approach
<h4>Unsupervised approaches can evaluate one or more benchmarks of the compendium you built based on several assumptions. Users do not have to provide additional information to obtain the benchmark.</h4>

### Assumptions
<h4>Based on the following two assumtpions, drop and impute values approach can evaluate a benchmark to evaluate the quality of the compendium.</h4>
<ol>
    <li>A good compendium should capture the pattern of gene expression profiles. Therefore, even if some values are dropped, we still can recover these missing values by applying missing value imputation.</li>
    <li>If a compendium is perturbed, it is more difficult to recover the missing values and yield larger error.</li>
</ol>

### Steps
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

### Benchmark evaluation
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
<h4>Current pipeline use the second defination as the benchmark. Since the noise ratio should be between 0 and 1 and typically error will not exceed 100%, the area will be between 0% and 100%.</h4>

![Figure V2. Benchmark evaluation of drop and impute values approach](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/images/Unsupervised_validation_description.png)
Figure V2. Benchmark evaluation of drop and impute values approach. The area between 100% error horizontal line and the error curve from missing value ratio = 0.5 (orange line) is evaluated as the benchmark.

### Benchmark comparison with reference compendium
After you got the benchmark with 49.35%, you want to know whether 49.35% is high enough to prove the compendium quality. To check whether this value is high enough, you need to fine one reference compendium with good quality and then evalute its benchmark and then make the comparison.

<h4>Reference compendium with good quality</h4>
For this Salmonella example compendium with 709 samples, it includes <a href=https://www.sciencedirect.com/science/article/pii/S1931312813004113">one small, published compendium</a> with 26 samples across different conditions and we can use this as a reference compendium.
<ul>
    <li>The benchmark of the Salmonella example compendium (with 709 samples) is about 49.35%. (it varies due to the randomness of validation procedures)</li>
    <li>The benchmark of the reference compendium (with 26 samples) is about 55.51%.</li>
    <li>The benchmark of the subset of Salmonella example compendium (with 26 samples in the reference compendium) is about 58.7%.</li>
</ul>
In conclusion, the benchmark of the subset of Salmonella example compendium is comparable with the benchmark of the refeernece compendium. <br>
You may also observed that for the high missing value ratio (0.99), the imputation error of the entire Salmonella example compendium is lower than the reference compendium or the subset compendium. It may implies that capture more samples can capture more information for recovering the missing values in this validation procedure.

![Figure V3. Benchmark comparison results](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/images/Unsupervised_validation_comparison.png)
Figure V3. Benchmark comparison results. (A) The results of the entire Salmonella example compendium with 709 samples. (B) The results of the reference compendium. (C) The results of the subset of Salmonella example compendium contains the samples in the reference compendium.


## An Supervised approach -- Correlation validation
<h4>Supervised approaches need additional information from users. For correlation validation, it needs samples-studies-conditions mapping table.</h4>

### Assumptions
<h4>Based on the following three assumtpions, correlation validation can perform simple validation of the compendium. (Currently there is no benchmark to evaluate overall quality, just observation and simple validation)</h4>
<ol>
    <li>The average correlation among samples within the same condition should be higher than the average correlation among samples within the same study.</li>
    <li>The average correlation among samples within the same study should be higher than the average correlation among samples in the entire compendium.</li>
    <li>The average correlation among different conditions or different studies should not be too high. (Otherwise the compendium may have low diversity)</li>
</ol>

### Steps (Correlation validation)
<h4>There are four steps for correlation validation approach to check the average correlation among samples within the same condition, study or the entire compendium (Figure V4(A)):</h4>
<ol>
    <li>Add the noise to the normalized data matrix in the compendium with different noise ratio.
        <ul>
            <li>Same as the adding noise step in drop and impute values approach</li>
        </ul>
    </li>
    <li>Read the samples-studies-conditions mapping table and group the samples by conditions or studies.
        <ul>
            <li>It need one user input: samples-studies-conditions table (Please refer the main document and step-by-step example).</li>
        </ul>
    </li>
    <li>For each group, evaluate the correlation matrix.
        <ul>
            <li>The group with just only one sample will be skipped.</li>
        </ul>
    </li>
    <li>Take the average values in lower half part of the correlation matrix from all groups.
        <ul>
            <li>One average correlation will be evaluated for each noise ratio and then a noise ratio vs. correlation curve can be plotted.</li>
            <li>Three lines with different grouping approaches (group by conditions, studies, or the entire compendium) will be plotted.</li>
        </ul>
    </li>
</ol>

### Steps (Correlation validation for checking diversity)
<h4>There are three steps for correlation validation approach to check the diversity among conditions and studies after adding the noise to normalized data matrix with different noise ratio. (Figure V4(B)):</h4>
<ol>
    <li>Read the samples-studies-conditions mapping table and group the samples by conditions or studies.
        <ul>
            <li>It need one user input: samples-studies-conditions table (Please refer the main document and step-by-step example).</li>
        </ul>
    </li>
    <li>For each group, merge the gene expression by taking the average.
    </li>
    <li>Calculate the correlation matrix among groups and take the average of the lower half part of the correlation matrix.
        <ul>
            <li>One average correlation will be evaluated for each noise ratio and then a noise ratio vs. correlation curve can be plotted.</li>
            <li>Two lines with different grouping approaches (group by conditions and studies) will be plotted.</li>
        </ul>
    </li>
</ol>

### Evaluation and observation of the correlation validation results
<h4>There are several points to simply validate the compendium based on the results: (Figure V4)</h4>
<ol>
    <li>For correlation validation, the correlation curve from grouping by conditions (the green curve) should be higher than the curve from grouping by studies (the orange curve).</li>
    <li>For correlation validation, the correlation curve from grouping by studies (the orange curve) should be higher than the curve from the entire compendium (the blue curve).</li>
    <li>For checking diversity, the correlation curve among different studies or conditions (the red and purple curve) should not be too high.</li>
</ol>

![Figure V4. Evaluation and observation of the correlation validation results.](https://github.com/bigghost2054/AutomatedOmicsCompendiumPreparationPipeline/blob/Pipeline_20200307/images/SalmonellaExample_CorrelationValidationResults.png)
Figure V4. Evaluation and observation of the correlation validation results.
