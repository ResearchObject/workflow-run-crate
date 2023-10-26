process RUN_SEARCHGUI {
label 'process_high'

conda (params.enable_conda ? "bioconda::searchgui-4.2.9" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://veitveit/searchgui:4.2.9--hdfd78af_0"
} else {
        container "quay.io/biocontainers/searchgui:4.2.9--hdfd78af_0"
}
  
publishDir "${params.outdir}/searchgui", mode:'copy', pattern: '*.zip'
  
  input:
  path mgffile
  path paramfile
  path fasta_decoy
  
  output:
  tuple path("${mgffile.baseName}.zip"), path(mgffile), emit: searchfiles
  
  script:

  def engine = [:]
  for (i in ["xtandem", "msgf", "ms-amanda", "tide", "comet", "myrimatch", "meta_morpheus", "andromeda"]) {
    t_engine = params.proline_engine.contains(i) ? 1 : 0
    engine.put(i, t_engine)
  }
  """
  # needed for Myrimatch, see https://github.com/compomics/searchgui/issues/245
        LANG=/usr/lib/locale/en_US
        export LC_ALL=C; unset LANGUAGE
  mkdir tmp
  mkdir log
  searchgui eu.isas.searchgui.cmd.PathSettingsCLI -temp_folder ./tmp -log ./log
  searchgui eu.isas.searchgui.cmd.SearchCLI -spectrum_files ./  -output_folder ./ -fasta_file "./${fasta_decoy}"  -id_params "./${paramfile}" -threads ${task.cpus} \\
      -xtandem ${engine["xtandem"]} -msgf ${engine["msgf"]} -comet ${engine["comet"]} -ms_amanda ${engine["ms-amanda"]} -myrimatch ${engine["myrimatch"]} \\
      -tide ${engine["tide"]} -meta_morpheus ${engine["meta_morpheus"]} -andromeda ${engine["andromeda"]}
  mv searchgui_out.zip ${mgffile.baseName}.zip
  """    
  
  }    
