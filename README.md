
# AutomatedOmicsCompendiumPreparationPipeline
<h3>Required Software</h3>
<ol>
<li>Python (>=3.6.5)</li>
<li>Perl (For Windows Only) (Strawberry Perl >= 5.30) </li>
</ol>

<h3>Required Packages</h3>
<ol>
<li>biopython (>=1.72)</li>
<li>pandas (>=0.22.0)</li>


#
<h3>Update</h3>
<ul>
<li>07/18/2019 Update: Create the new repository</li>
<li>07/18/2019 21:20 Update: (TEST) Create the directories and files</li>
<li>07/22/2019 01:43 Update: Metadata definitions</li>
<li>07/23/2019 Gene Annotation Data Definition and SRA metadata download implementation</li>
</ul>



<h4>07/23/2019 Update</h4>
<ol>
<li>Gene Annotation Data Definition</li>
<li>SRA metadata download implementation<br>
    <ol>
    <li>Fetch SRA runinfo by SRA ids (DONE)</li>
    <li>Fetch FASTA file(s) by gene annotation (GFF3) file(s) and merge them into one file (DONE)</li>
    <li>Build bowtie2index by merged fasta file (ONGOING)</li>
    </ol>
</ol>