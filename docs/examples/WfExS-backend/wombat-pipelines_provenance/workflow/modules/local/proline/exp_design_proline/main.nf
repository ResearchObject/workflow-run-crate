process EXP_DESIGN_PROLINE {
  label 'process_low'
  label 'process_single_thread'
    conda (params.enable_conda ? "bioconda::proline_todo" : null)
    if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://wombatp/proline-pipeline:v0.18"
    } else {
        container "wombatp/proline-pipeline:v0.18"
    }
  
  publishDir "${params.outdir}/proline", mode:'copy'
  

  input:
  val mzdbs
  path exp_design
  
  output:
  path "quant_exp_design.txt" , emit: exp_design

  
  script:
if (exp_design.getName() == "none") {
    // no file provided
    exp_design_text = "mzdb_file\texp_condition"
    for( int i=0; i<mzdb.size(); i++ ) {
      exp_design_text += "\n./${mzdb[i].baseName}.mzDB\tMain"
    }
    """
    touch quant_exp_design.txt    
    echo "${exp_design_text}" >> quant_exp_design.txt
    """
  } else {
    """
    cp ${exp_design} quant_exp_design.txt
    sed -i 's/raw_file/mzdb_file/g' quant_exp_design.txt
    sed -i 's/.raw/.mzDB/g' quant_exp_design.txt
    sed -i 's/.mzML/.mzDB/g' quant_exp_design.txt
    sed -i 's/.mzml/.mzDB/g' quant_exp_design.txt
    sed -i '2,\$s|^|./|' quant_exp_design.txt
    # keep first two columns of quant_exp_design.txt
    cut -f1,2 quant_exp_design.txt > quant_exp_design.txt.tmp
    mv quant_exp_design.txt.tmp quant_exp_design.txt
    """
  }
}    
