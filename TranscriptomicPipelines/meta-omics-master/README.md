# Meta-Omics: An Appilication for Omics Metadata Integration

Life science experiment data are various and distributed among many databases. Therefore, providing clean and integrated metadata for biologists is important and useful. Meta-omics intends to integrate metadata retrieved from different databases and classify these metadata based on their omics types, minimizing human efforts in data collection.

## Installation

First, clone the package to your machine:
```
git clone git@github.com:fangzhouli/meta-omics.git
```
Then go to the package directory to install:
```
pip install meta-omics
```

## Usage

After the installation, you can run the application in the command-line interface by using 'meta-omics' command followed by a string of a disease.
```
meta-omics 'ischaemic heart disease'
```
The amount of time depends on the disease, and after the application finishes running, it will generate a CSV file in the directory where you have executed the command.

## Format

Each row of the output file is an experiment metadata. For each experiment, Meta-omics collects metadata listed below if available:

- source        : Database the experiment retrieved from
- accession     : Accession ID of experiment
- title         : Title of the experiment
- description   : Abstract of the experiment
- pmid          : PMID of the publication associated with the experiment
- pub_title     : Title of the publication
- pub_date      : Date of the publication
- pub_author    : Author(s) of the publication
- tech_acc      : Accession ID of technologies used in the experiment
- tech_name     : Name of technologies
- sample_acc    : Accession ID for samples used in the experiment
- species       : Species studied in the experiment
- exp_type      : Experiment types provided by the source

## Credits

- ChengEn Tan, as the Project Supervisor
- Minseung Kim, as the Technology Advisor
- Ilias Tagkopoulos, as the Principal Investigator

## Future Work

### Database

Currently, Meta-omics has only integrated GEO (Gene Expression Omnibus) metadata. Meta-omics will continually integrate more databases, such as ArrayExpress, SRA (Sequence Read Archive), etc.

### Omics

Meta-omics is dedicated to extract transcriptomics data, and we plan to add microbiomics data in the future.

### NLP (Natural Languange Processing)

Meta-omics will utilize NLP techniques to achieve two novel features. First, Meta-omics will use NLP to curate patients metadata by mining experiment abstract and publication. Second, Meta-omics will practice NLP to filter the metadata retrieved from databases to provide cleaner metadata, furthering the minimization of human efforts.

### UI (User Interface)

Currently, Meta-omics is designed as a command-line interface software. In the future, we will provide more user-friendly GUI.