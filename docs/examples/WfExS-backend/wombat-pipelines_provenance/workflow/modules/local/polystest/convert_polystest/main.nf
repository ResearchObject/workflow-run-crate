process CONVERT_POLYSTEST {
label 'process_low'

conda (params.enable_conda ? "bioconda::polystest-1.3.4" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://quay.io/biocontainers/polystest:1.3.4--hdfd78af_0"
} else {
        container "quay.io/biocontainers/polystest:1.3.4--hdfd78af_0"
}
  
  publishDir "${params.outdir}/polystest", mode:'copy'
  
  input:
  path exp_design 
  path pep_quant 
  path prot_quant
  
  output:
  path "stand_prot_quant_merged.csv", emit: stdprotquant
  path "stand_pep_quant_merged.csv", emit: stdpepquant
  path "exp_design.txt", emit: exp_design
  
  when:
  params.run_statistics
  
  script:
 """
  cp "${exp_design}" exp_design.txt
  Rscript $baseDir/bin/Convert2StandFormat.R
  """


}
