process MZDB2MGF {
    label 'process_low'
    label 'process_single_thread'
    conda (params.enable_conda ? "conda-forge::python-3.8.3" : null)
    if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://wombatp/proline-pipeline:v0.18"
    } else {
        container "wombatp/proline-pipeline:v0.18"
    }

  
  publishDir "${params.outdir}/mgf", mode:'copy'


  input:
  path mzdbfile
  
  output:
  path "${mzdbfile.baseName}.mgf" , emit: mgfs
  
  script:
  """
  mzdb2mgf -i "${mzdbfile}" -o "${mzdbfile.baseName}.mgf" 
  """
}

