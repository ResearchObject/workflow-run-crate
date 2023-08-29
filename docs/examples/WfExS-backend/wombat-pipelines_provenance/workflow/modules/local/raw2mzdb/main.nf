process RAW2MZDB {
    label 'process_low'
    label 'process_single_thread'
    conda (params.enable_conda ? "conda-forge::python-3.8.3" : null)
    if (workflow.containerEngine == 'singularity' && !params.singularity_pull_docker_container) {
        container "docker://wombatp/proline-pipeline:v0.18"
    } else {
        container "wombatp/proline-pipeline:v0.18"
    }

  publishDir "${params.outdir}/mzdb", mode:'copy'

  input:
  path rawfile
  
  output:
  path "${rawfile.baseName}.mzDB" , emit: mzdbs
  
  script:
  """
  ls -la
  thermo2mzdb -i "${rawfile}" -o "${rawfile.baseName}.mzDB" 
  """
}
