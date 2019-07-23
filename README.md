
# AutomatedOmicsCompendiumPreparationPipeline
Required Python Version: 3.6.5

Required Packages:

biopython (>=1.72)

pandas (>=0.22.0)


#
07/18/2019 Update: Create the new repository

07/18/2019 21:20 Update: (TEST) Create the directories and files

07/22/2019 01:43 Update: Metadata definitions

07/23/2019 Update:
1. Gene Annotation Data Definition
2. SRA metadata download implementation

     2a. Fetch SRA runinfo by SRA ids (DONE)
     
     2b. Fetch FASTA file(s) by gene annotation (GFF3) file(s) and merge them into one file (DONE)
     
     2c. Build bowtie2index by merged fasta file (ONGOING)