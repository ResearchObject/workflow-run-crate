process PREPARE_FILES { 
    publishDir "${params.outdir}/prepare_files"
    label 'process_medium'
    conda (params.enable_conda ? "conda-forge::python-3.8.3" : null)
    if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://wombatp/maxquant-pipeline:dev"
    } else {
        container "wombatp/maxquant-pipeline:dev"
    }


    input:
      path sdrf
      path parameters
      path exp_design
      path raws
      path mzmls
      path map
     

    output:
      path "sdrf_temp.tsv" , includeInputs:true         , emit: sdrf_local
      path "exp_design.txt" , includeInputs:true	    , emit: exp_design
      path "params.yml" , includeInputs:true		    , emit: params
      path "*.version.txt" , includeInputs:true          , emit: version
      path "{*.raw,*.RAW}" , includeInputs:true	, optional:true   , emit: raws
      path "{*.mzml,*.mzML}" , includeInputs:true, optional:true	    , emit: mzmls


    script:
    """
    if [[ "$map" != "params2sdrf.yml" ]]
    then
        cp "${map}" params2sdrf.yml
    fi
    if [[ "$sdrf" != "no_sdrf" ]] 
    then    
        if [[ "$sdrf" != "sdrf_local.tsv" ]]
        then
	    cp "${sdrf}" sdrf_local.tsv
        fi
    fi	
    if [[ "$exp_design" != "no_exp_design" ]] 
    then    
       if [[ "$exp_design" != "exp_design.txt" ]] 
       then
	     cp "${exp_design}" exp_design.txt
       fi
    else
        if [[ "$sdrf" == "no_sdrf" ]] 
        then
            printf "raw_file\texp_condition" >> exp_design.txt
	    for a in $raws
	    do
	        printf "\n\$a\tA" >> exp_design.txt
	    done
        else 
	    $baseDir/bin/sdrf2exp_design.py
        fi        
    fi
    if [[ "$sdrf" == "no_sdrf" ]] 
    then
	$baseDir/bin/exp_design2sdrf.py
    fi
    if [ "$raws" == "no_raws" ] && [ "$mzmls" == "no_mzmls" ]
    then
        # Download all files from column file uri		
        echo "Downloading raw files from column file uri\n"
	for a in \$(awk -F '\t' -v column_val='comment[file uri]' '{ if (NR==1) {val=-1; for(i=1;i<=NF;i++) { if (\$i == column_val) {val=i;}}} if(val != -1) { if (NR!=1) print \$val} } ' "$sdrf")
	do
            echo "Downloading \$a\n"
	    wget -c -T 100 -t 5 "\$a"
        done
    fi

    if [[ "$parameters" == "no_params" ]]
    then
	printf "params:\n  None:  \nrawfiles: None\nfastafile: None" >  params.yml
    elif [[ "$parameters" != "params.yml" ]] 
    then
        cp "${parameters}" params.yml
    fi
    echo "See workflow version" > prepare_files.version.txt
    cp sdrf_local.tsv sdrf_temp.tsv
    """
}
