process STPETER {
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
  tuple path(protxml), path(pepxml)
  path mzmls
  path fasta
  val parameters
  
  output:
  tuple path("${protxml.baseName}_stpeter.prot.xml"), path(pepxml, includeInputs: true), emit: stpeter_output
  
  script:
  fragments = parameters.fragment_mass_tolerance.split(' ')
  frag_tol = fragments[0] as Float
  // Binning requires half of the tolerance + transformation from ppm to Da 
  frag_tol = ((fragments[1] == "ppm") ? frag_tol*0.0005  : frag_tol/2)  
  """
  cp "${protxml}" stpeter_in.prot.xml
  StPeter -f ${parameters.ident_fdr_psm} -t ${frag_tol} stpeter_in.prot.xml
  cp stpeter_in.prot.xml "${protxml.baseName}_stpeter.prot.xml"
  """

  }    
