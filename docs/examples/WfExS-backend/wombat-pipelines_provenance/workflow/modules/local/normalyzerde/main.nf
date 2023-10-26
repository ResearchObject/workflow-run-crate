process NORMALYZERDE {
    label 'process_medium'
//    label 'process_single_thread'
    publishDir "${params.outdir}/normalyzerde", mode:'copy'
    conda (params.enable_conda ? "bioconda:bionconductor-normalyzerde=1.14.0" : null)
    if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://computationalproteomics/normalyzerde:1.14.0"
    } else {
        container "computationalproteomics/normalyzerde:1.14.0"
    }

    input:
      path maxquant
      path exp_file
      path comp_file
      val parameters
  
    when:
      parameters.run_statistics

    output:
	path "Normalyzer_design.tsv" , emit: exp_design
	path "NormalyzerProteins/*"   , emit:  normalyzer_proteins
	path "NormalyzerPeptides/*"   , emit:  normalyzer_peptides
        path "stand_prot_quant_merged.csv"    , emit: std_prots
        path "stand_pep_quant_merged.csv"    , emit: std_peps
        path "exp_design_calcb.tsv"    , emit: std_exp_design


    script:
    """
    cp "proteinGroups.txt" protein_file.txt
    cp "peptides.txt" peptide_file.txt
    Rscript $baseDir/bin/runNormalyzer.R --comps="${params.comps}" --method="${parameters.normalization_method}" --exp_design="${exp_file}" --comp_file="${comp_file}"
    """

}
