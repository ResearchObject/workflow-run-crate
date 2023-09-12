//import org.yaml.snakeyaml.Yaml
process SDRFMERGE { 
      
    label 'process_medium'
    conda (params.enable_conda ? "bioconda::sdrf-pipelines=0.0.21" : null)
    if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://wombatp/maxquant-pipeline:v0.2"
    } else {
        container "wombatp/maxquant-pipeline:v0.2"
    }

    publishDir "${params.outdir}/sdrf_merge", mode:'copy'


    input:
      path sdrf
      path parameters
      path map
     

    output:
      path "sdrf_local.tsv"         , emit: sdrf_local
      path "params_out.yml"          , emit: parameters_out
      path "changed_params.txt"     , emit: changed_params


    script:
    // load parameters
    //def par_filename = file( ["${task.workDir}", "${parameters}"].join(File.separator) )
    //def par_filename = parameters
    //println(par_filename)
    //def yaml = (Map)new Yaml().load((par_filename).text)    

    """
    if [[ "$sdrf" != "sdrf.tsv" ]]
    then
	cp "${sdrf}" sdrf.tsv
    fi
    if [[ "$parameters" != "params.yml" ]] 
    then
        cp "${parameters}" params.yml
    fi
    if [[ "$map" != "params2sdrf.yml" ]]
    then
        cp "${map}" params2sdrf.yml
    fi
    # TODO change to package when available
    python $projectDir/bin/add_data_analysis_param.py > changed_params.txt
    python $projectDir/bin/sdrf2params.py
    """
}
