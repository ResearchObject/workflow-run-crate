process RUN_PEPTIDESHAKER {
label 'process_high'

conda (params.enable_conda ? "bioconda::peptideshaker-2.2.6" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://veitveit/peptide-shaker:2.2.23--hdfd78af_0"
} else {
        container "quay.io/biocontainers/peptide-shaker:2.2.23--hdfd78af_0"
}
  
publishDir "${params.outdir}/peptideshaker", mode:'copy'
  
  input:
  tuple path( searchgui_zip ), path( mzmlfile )
  path fasta_decoy
  
  output:
  path "${mzmlfile.baseName}.psdb", emit: peptideshakerfiles
  

script:
  mem = "${task.memory}"
  mem = mem.replaceAll(" ","")
  mem = mem.replaceAll("B","")
  """
  mkdir tmp
  mkdir log    
  unzip "${searchgui_zip}" searchgui.par
  peptide-shaker eu.isas.peptideshaker.cmd.PathSettingsCLI  -temp_folder ./tmp -log ./log
  peptide-shaker eu.isas.peptideshaker.cmd.PeptideShakerCLI -spectrum_files "./${mzmlfile}"  -identification_files "./${searchgui_zip}"  -id_params ./searchgui.par \\
      -fasta_file "./${fasta_decoy}" -reference "wombat" -out "./${mzmlfile.baseName}.psdb" -threads ${task.cpus} -Xmx${mem}
  """    
  
  }    
