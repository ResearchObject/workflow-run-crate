process RUN_PROLINE {
label 'process_high'

conda (params.enable_conda ? "bioconda::proline_todo" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://wombatp/proline-pipeline:v0.18"
} else {
        container "wombatp/proline-pipeline:v0.18"
}
  
  publishDir "${params.outdir}/proline", mode:'copy'
  
  input:
  path rfs
  path mzdbs
  path lfq_param 
  path import_param 
  path exp_design
  
  output:
  path "proline_results/*.xlsx", emit: proline_out
  
  script:
  mem = " ${task.memory}"
  mem = mem.replaceAll(" ","")
  mem = mem.replaceAll("B","")
  """
  cp -r /proline/* .
  java8 -Xmx${mem} -cp "config:lib/*:proline-cli-0.2.0-SNAPSHOT.jar" -Dlogback.configurationFile=config/logback.xml \\
    fr.proline.cli.ProlineCLI run_lfq_workflow -i="${import_param}"  -ed="${exp_design}" -c="${lfq_param}"
  """
}
