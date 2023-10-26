process RUN_COMET {
label 'process_high'

conda (params.enable_conda ? "bioconda::comet-ms-2021010-h87f3376_1" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://quay.io/biocontainers/comet-ms:2021010--h87f3376_1"
} else {
        container "quay.io/biocontainers/comet-ms:2021010--h87f3376_1"
      containerOptions = '-u $(id -u):$(id -g)'
}
  
publishDir "${params.outdir}/comet", mode:'copy'
  
  input:
  path mzmlfile
  path fasta
  path comet_param
  
  output:
  path "${mzmlfile.baseName}.pep.xml", emit: comet
  
  script:
  
  """
   comet -P"${comet_param}" -N"${mzmlfile.baseName}" -D"${fasta}" "${mzmlfile}"
  """    
  
  }    
