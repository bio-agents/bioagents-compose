# Automatic-Workflow-Composition

Collection of material including data files, scripts, workflows and results for the proteomics use cases described in the publication "Automated workflow composition in mass spectrometry based proteomics" (submitted).

## File structure
Configuration and data files as well scripts to run the 4 use cases and a total of 11 workflows are available in the respective _Use_case..._ folders:

- Amino acid hydropathy indices of data from liquid chromatography tandem mass spectrometry: Use_case_1-amino_acid_index
- Gene set enrichment analysis of identified proteins from an MS sample: Use_case_2-data_interpretation
- Identification and localization of post-translational modifications:	Use_case_3-PTM_identification
- Quantification of labeled iTRAQ MS data: Use_case_4-quantification

## Workflow synthesis
Automatic synthesis is based on the PROPHETS agent which can be downloaded from http://ls5-www.cs.tu-dortmund.de/projects/prophets/download.php and installed on any platform with a recent Java version. The files for the case study are available as a .zip archive (https://github.com/bio-agents/bioagentsCompose/raw/master/Automatic-Workflow-Composition/prophets-project.zip) that can be extracted and imported into PROPHETS as a new project.

## Workflow examples
The workflows of the four use cases are easily executed in the given Docker container. 

Alternatively, the bash scripts can also be adapted to run independently by adjusting the paths of the used software agents. This requires the prior installation of the required software agents.

### Run on docker
(docker needs to be installed before, see docker.com for more details)

__Get docker image__
_docker pull bioagents/automaticworkflowcomposition_

__Run workflows__   
E.g. Use case 3 workflow 1:   
_docker run -it bioagents/automaticworkflowcomposition_   
_cd UseCases/Use_case_3-PTM_identification/Workflow1_   
_bash FullPipeline_   
You can run the R scripts (if available) with _R CMD BATCH GivenRScriptName_. Download the resulting data with _docker cp_

### Build docker
__Download files__    
_git clone https://github.com/veitveit/Automatic-Workflow-Composition_

__Create docker image:__    
_docker build -t bioagents/automaticsworkflowcomposition ._  
This will take a while.   
(you need to be in the folder Automatic-Workflow-Composition)

