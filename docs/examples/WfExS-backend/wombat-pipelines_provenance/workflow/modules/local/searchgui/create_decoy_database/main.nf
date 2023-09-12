process CREATE_DECOY_DATABASE {
  label 'process_low'
  label 'process_single_thread'
    conda (params.enable_conda ? "bioconda::searchgui-4.0.41" : null)
    if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://veitveit/searchgui:4.2.9--hdfd78af_0"
    } else {
        container "quay.io/biocontainers/searchgui:4.2.9--hdfd78af_0"
    }
  
  publishDir "${params.outdir}/decoy_database", mode:'copy'
  

  input:
  path fasta
  val run
  
  output:
  path "${fasta.baseName}_concatenated_target_decoy.fasta" , emit: fasta_with_decoy

  when:
  run

  
  script:
  """
  searchgui eu.isas.searchgui.cmd.FastaCLI -in ${fasta} -decoy
  """    
}    
