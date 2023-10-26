process MSQROB {
  label 'process_high'
  conda (params.enable_conda ? "bioconda::r-msqrob-0.7.7" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://quay.io/biocontainers/r-msqrob:0.7.7--r41hdfd78af_1"
} else {
        container "quay.io/biocontainers/r-msqrob:0.7.7--r41hdfd78af_1"
}
  
publishDir "${params.outdir}/msqrob", mode:'copy'
 
  when: parameters.run_statistics

  input:
  path exp_design
  path rawfiles
  path quant_tab
  path quant_prot_tab
  path pep_file
  path prot_file
  val parameters
  
  output:
  path "MSqRobOut.csv", emit: msqrob_prot_out
  path "stand_prot_quant_merged.csv", emit: stdprotquant
  path "stand_pep_quant_merged.csv", emit: stdpepquant
  path "exp_design.txt", emit: exp_design_final
  
  
  script:
  // no file provided
  expdesign_text = "raw_file\texp_condition\tbiorep"
  if (exp_design.getName() == "none") {
    if (rawfiles[1] != null) {
      for( int i=0; i<rawfiles.size(); i++ ) {
        biorep = i+1
        expdesign_text += "\n${rawfiles[i].getBaseName()}\tMain\tA${biorep}"
      }
    } else {
      expdesign_text += "\n${rawfiles.getBaseName()}\tMain\tA1"
    }
  }
  
  """
  echo "${expdesign_text}" > none
  cp "${exp_design}" exp_design.txt
  mv "${quant_tab}" q_input.txt
  mv "${quant_prot_tab}" q_prot.txt
  Rscript $baseDir/bin/runMSqRob.R --normalization="${parameters.normalization_method}" --min_peptides="${parameters.min_num_peptides}"
  """
}    
