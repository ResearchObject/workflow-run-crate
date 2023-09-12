process POLYSTEST {
  label 'process_high'

  conda (params.enable_conda ? "bioconda::polystest-1.3.4" : null)
  if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://quay.io/biocontainers/polystest:1.3.4--hdfd78af_0"
  } else {
        container "quay.io/biocontainers/polystest:1.3.4--hdfd78af_0"
  }
  
  publishDir "${params.outdir}/polystest", mode:'copy'
  
  when:
  parameters.run_statistics

  input:
  path exp_design
  path proline_res
  val parameters
  
  output:
  path "polystest_prot_res.csv", emit: polystest_prot
  path "polystest_pep_res.csv", emit: polystest_pep
  
  script:
  """
  convertProline=\$(which runPolySTestCLI.R)
  
  echo \$convertProline
  convertProline=\$(dirname \$convertProline)
  
  echo \$convertProline
  Rscript \${convertProline}/convertFromProline.R ${exp_design} ${proline_res}
  
  sed -i "s/threads: 2/threads: ${task.cpus}/g" pep_param.yml
  sed -i "s/threads: 2/threads: ${task.cpus}/g" prot_param.yml
  
  runPolySTestCLI.R pep_param.yml
  runPolySTestCLI.R prot_param.yml
  """

}
