
# AutomatedOmicsCompendiumPreparationPipeline
07242019 Note: So far this version does not support Windows. Please use Ubuntu subsystem if you use Windows. (The testing will be in Ubuntu subsystem)


<h3>Required Software</h3>
<ol>
<li>Python (>=3.6.9)</li>
<li>sratoolkit (>=2.9.6) </li>
</ol>

<h3>Required Packages</h3>
<ol>
<li>biopython (>=1.74)</li>
<li>pandas (>=0.25.0)</li>
<li>RSeQC (>=3.0.0)</li>
<li>HTSeq (>=0.11.2) </li>
</ol>


#
<h3>Update</h3>
<ul>
<li>07/18/2019 Update: Create the new repository</li>
<li>07/18/2019 21:20 Update: (TEST) Create the directories and files</li>
<li>07/22/2019 01:43 Update: Metadata definitions</li>
<li>07/23/2019 Gene Annotation Data Definition and SRA metadata download implementation</li>
<li>07/24/2019 Use more set/get methods, wrapper of bowtie2-build, and compatability of the toolkit (sratoolkit) and packages (RSeQC and HTSeq) </li>
</ul>



<h4>07/24/2019 Update</h4>
<ol>
<li>Gene Annotation Data Definition</li>
<li>SRA metadata download implementation<br>
    <ol>
    <li>Fetch SRA runinfo by SRA ids (DONE)</li>
    <li>Fetch FASTA file(s) by gene annotation (GFF3) file(s) and merge them into one file (DONE)</li>
    <li>Build bowtie2index by merged fasta file (DONE)</li>
    <li>Integration of toolkit (sratoolkit) (ONGOING) </li>
    <li>Integration of packages (RSeQC and HTSeq) (ONGOING) </li>
    <li></li>
    </ol>
</ol>