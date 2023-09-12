process PROTEINPROPHET {
label 'process_medium'

conda (params.enable_conda ? "bioconda::tpp-5.0.0-pl5.22.0_0" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://spctools/tpp:version6.1"
} else {
        container "spctools/tpp:version6.1"
        containerOptions = '-u $(id -u):$(id -g)'

}
  
publishDir "${params.outdir}/tpp", mode:'copy'
  
input:
  path pepxml_file
  val parameters
  
output:
  tuple path("${pepxml_file.baseName}.prot.xml"), path(pepxml_file, includeInputs: true),  emit: proteinprophet_xml
  path "*.xml", emit: proteinprophet_tables
  
script:
  inference = ["unique": 0, "shared": 1, "parsimony": 0.25]
  inference = inference[parameters.protein_inference]
  """
  ProteinProphet "${pepxml_file}" "${pepxml_file.baseName}.prot.xml" MINPROB"${parameters.ident_fdr_peptide}" EXCELPEPS EXCELxx MININDEP"${inference}"
  """

}
