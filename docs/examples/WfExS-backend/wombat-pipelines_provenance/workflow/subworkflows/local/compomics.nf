//
// Get assets like general parameter files
//

//
// Run maxquant and normalyzer
//

include { RAW2MZML }                 from '../../modules/local/raw2mzml/main'  
include { CREATE_DECOY_DATABASE }                      from '../../modules/local/searchgui/create_decoy_database/main'
include { PREPARE_SEARCHGUI }                      from '../../modules/local/searchgui/prepare_searchgui/main'
include { RUN_SEARCHGUI }                     from '../../modules/local/searchgui/run_searchgui/main'
include { RUN_PEPTIDESHAKER }                     from '../../modules/local/peptideshaker/run_peptideshaker/main'
include { PEPTIDESHAKER_REPORT }                     from '../../modules/local/peptideshaker/peptideshaker_report/main'
include { FLASHLFQ }                     from '../../modules/local/flashlfq/main'
include { MSQROB }                     from '../../modules/local/msqrob/main'
 
workflow COMPOMICS {
    take:
    fasta // fasta file
    raws // raw files
    parameters // map of parameters 
    exp_design // experimental design file
    ptm_mapping // map to convert from unimod to searchgui


    main:
    RAW2MZML ( raws )
    def add_decoys = ('add_decoys' in parameters) ? parameters['add_decoys'] : true
    CREATE_DECOY_DATABASE ( fasta , add_decoys )
    PREPARE_SEARCHGUI ( parameters, ptm_mapping.collect() )
    RUN_SEARCHGUI ( RAW2MZML.out, PREPARE_SEARCHGUI.out,  CREATE_DECOY_DATABASE.out.ifEmpty(fasta) )
    RUN_PEPTIDESHAKER ( RUN_SEARCHGUI.out,  CREATE_DECOY_DATABASE.out.ifEmpty(fasta) )
    PEPTIDESHAKER_REPORT ( RUN_PEPTIDESHAKER.out )
    FLASHLFQ ( PEPTIDESHAKER_REPORT.out.peptideshaker_tsv_file_filtered.collect(), RAW2MZML.out.collect(), parameters, exp_design )
    MSQROB ( exp_design, raws.collect(), FLASHLFQ.out.flashlfq_peptides, FLASHLFQ.out.flashlfq_proteins, 
             PEPTIDESHAKER_REPORT.out.peptideshaker_peptide_file.collect(), PEPTIDESHAKER_REPORT.out.peptideshaker_protein_file.collect() , parameters)

    emit:
    MSQROB.out.exp_design_final
    MSQROB.out.stdpepquant
    MSQROB.out.stdprotquant
    MSQROB.out.msqrob_prot_out
}
