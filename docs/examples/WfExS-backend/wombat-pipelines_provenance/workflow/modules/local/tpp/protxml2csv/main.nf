process PROTXML2CSV {
  label 'process_medium'
  // TODO: add container that contains only the required R packages (XML, stringi, progress)
  conda (params.enable_conda ? "bioconda::xxx" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://wombatp/transproteomic-pipeline:0.24"
} else {
        container "wombatp/transproteomic-pipeline:0.24"
}
  
publishDir "${params.outdir}/tpp", mode:'copy'
 
 
  input:
  tuple path(stpeter), path(pepxml)
  val parameters
  
  output:
  tuple path("${stpeter.baseName}_prot.csv"), path("${stpeter.baseName}_pep.csv"), emit: protquant
  
  script:
  """
  cp "${stpeter}" StPeterOut.prot.xml 
  cp "${pepxml}" Sample.pep.xml
  Rscript $baseDir/bin/proxml2csv.R --xml=StPeterOut.prot.xml --fdr=${parameters.ident_protein_fdr} --npep ${parameters.min_num_peptides}
  mv StPeterOut.prot.xml.csv "${stpeter.baseName}_pep.csv"
  mv StPeterOut.prot.xml_summary.csv "${stpeter.baseName}_prot.csv"
  """
}    
