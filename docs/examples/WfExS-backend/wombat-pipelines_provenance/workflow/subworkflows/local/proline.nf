//
// Get assets like general parameter files
//
ch_proline_parameters = Channel.fromPath("$projectDir/assets/lfq_param_file_template.txt")

//
// Run maxquant and normalyzer
//

include { RAW2MZDB }                 from '../../modules/local/raw2mzdb/main'  
include { MZDB2MGF }                      from '../../modules/local/mzdb2mgf/main'
include { CREATE_DECOY_DATABASE }                      from '../../modules/local/searchgui/create_decoy_database/main'
include { PREPARE_SEARCHGUI }                      from '../../modules/local/searchgui/prepare_searchgui/main'
include { RUN_SEARCHGUI }                     from '../../modules/local/searchgui/run_searchgui/main'
include { CONFIG_PROLINE }                    from '../../modules/local/proline/config_proline/main'
include { EXP_DESIGN_PROLINE}                   from '../../modules/local/proline/exp_design_proline/main'
include { RUN_PROLINE }                      from '../../modules/local/proline/run_proline/main'
include { POLYSTEST }                     from '../../modules/local/polystest/run_polystest/main'
include { CONVERT_POLYSTEST }                     from '../../modules/local/polystest/convert_polystest/main'
 
workflow PROLINE {
    take:
    fasta // fasta file
    raws // raw files
    parameters // map of parameters 
    exp_design // experimental design file
    ptm_mapping // map to convert from unimod to searchgui


    main:
    RAW2MZDB ( raws )
    MZDB2MGF ( RAW2MZDB.out )

    def add_decoys = ('add_decoys' in parameters) ? parameters['add_decoys'] : true
    CREATE_DECOY_DATABASE ( fasta , add_decoys )
    PREPARE_SEARCHGUI ( parameters, ptm_mapping.collect() )
    RUN_SEARCHGUI ( MZDB2MGF.out, PREPARE_SEARCHGUI.out,  CREATE_DECOY_DATABASE.out.ifEmpty(fasta) )
    CONFIG_PROLINE ( RUN_SEARCHGUI.out.searchfiles.collect{ it[0] }, ch_proline_parameters, parameters)
    EXP_DESIGN_PROLINE ( RAW2MZDB.out.collect() , exp_design )
    RUN_PROLINE ( CONFIG_PROLINE.out.xml_search_files, RAW2MZDB.out.mzdbs.collect(), CONFIG_PROLINE.out.lfq_param_file,  
                  CONFIG_PROLINE.out.import_files, EXP_DESIGN_PROLINE.out.exp_design  )
    POLYSTEST ( EXP_DESIGN_PROLINE.out.exp_design, RUN_PROLINE.out, parameters )
    CONVERT_POLYSTEST ( EXP_DESIGN_PROLINE.out.exp_design, POLYSTEST.out.polystest_pep,  POLYSTEST.out.polystest_prot )

    emit:
    CONVERT_POLYSTEST.out.exp_design
    CONVERT_POLYSTEST.out.stdpepquant
    CONVERT_POLYSTEST.out.stdprotquant
    POLYSTEST.out.polystest_prot
    POLYSTEST.out.polystest_pep
}
