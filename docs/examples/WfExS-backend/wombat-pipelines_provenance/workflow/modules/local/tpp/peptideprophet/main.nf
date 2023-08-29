process PEPTIDEPROPHET {
label 'process_medium'

conda (params.enable_conda ? "bioconda::tpp-5.0.0-pl5.22.0_0" : null)
if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container "docker://spctools/tpp:version6.1"
} else {
        container "spctools/tpp:version6.1"
        containerOptions = '-u $(id -u):$(id -g)'
}
  
  publishDir "${params.outdir}/tpp", mode:'copy'
  
  input:
  path pepxml_file
  path fasta
  path mzml
  val parameters
  
  output:
  path("${pepxml_file.baseName}.interact.pep.xml"), emit: peptideprophet
  
  script:
  enzymemap = ["trypsin": "", "trypsin/p": "", "lys_c": "-eN", "lys_n": "-eL", "arg_c": "-eN", "asp_n": "-eA", "cnbr": "-eM", "glu_c": "-eG", "pepsina": "-eN", "chymotrypsin": "-eC", "unspecified": "-eN"]
  enzyme = enzymemap[parameters.enzyme.toLowerCase()]
  
  """
#  cp ${pepxml_file} t
#  cp t ${pepxml_file}
  xinteract -N"${pepxml_file.baseName}.interact.pep.xml" -p"${parameters.ident_fdr_psm}" ${enzyme} -l"${parameters.min_peptide_length}" -THREADS=${task.cpus} -PPM -O -D"${fasta}" "${pepxml_file}"
  """

  

  }    
