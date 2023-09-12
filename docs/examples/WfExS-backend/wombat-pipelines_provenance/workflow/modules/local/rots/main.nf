process ROTS {
label 'process_medium'
  label 'process_single_thread'
  conda (params.enable_conda ? "bioconda::bioconductor-rots::1.22.0" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "wombatp/transproteomic-pipeline:0.24"
} else {
        container "wombatp/transproteomic-pipeline:0.24"
}
  
publishDir "${params.outdir}/rots", mode:'copy'
 
 
  when:
  parameters.run_statistics

  input:
  path protein_quants
  path peptide_quants
  val parameters

  output:
  path "stand_prot_quant_merged.csv", includeInputs: true, emit: protein_quants_rots
  path "stand_pep_quant_merged.csv", includeInputs: true, emit: peptide_quants_rots

  script:
  """
  R CMD BATCH $baseDir/bin/rots_analysis_proteins.R
  R CMD BATCH $baseDir/bin/rots_analysis_peptides.R
  """
}    
