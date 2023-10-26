//
// Get assets like general parameter files
//

//
// Run maxquant and normalyzer
//

include { RAW2MZML }                 from '../../modules/local/raw2mzml/main'  
include { WRITE_CONFIG }              from '../../modules/local/comet/write_config/main'
include { RUN_COMET }                 from '../../modules/local/comet/run_comet/main'
include { PEPTIDEPROPHET }           from '../../modules/local/tpp/peptideprophet/main'
include { PROTEINPROPHET }           from '../../modules/local/tpp/proteinprophet/main'
include { STPETER }                 from '../../modules/local/tpp/stpeter/main'
include { PROTXML2CSV }            from '../../modules/local/tpp/protxml2csv/main'
include { MERGEOUTPUT }            from '../../modules/local/tpp/mergeoutput/main'
include { ROTS }            from '../../modules/local/rots/main'

workflow TPP {
    take:
    fasta // fasta file
    raws // raw files
    parameters // map of parameters 
    exp_design // experimental design file
    ptm_mapping // map to convert from unimod to searchgui


    main:
    RAW2MZML ( raws )
    WRITE_CONFIG ( parameters, ptm_mapping )
    RUN_COMET ( RAW2MZML.out, fasta, WRITE_CONFIG.out)
    PEPTIDEPROPHET( RUN_COMET.out, fasta, RAW2MZML.out.collect(), parameters)
    PROTEINPROPHET( PEPTIDEPROPHET.out, parameters)
    STPETER( PROTEINPROPHET.out.proteinprophet_xml, RAW2MZML.out.collect(), fasta, parameters)
    PROTXML2CSV( STPETER.out, parameters )
    MERGEOUTPUT( PROTXML2CSV.out.collect(), raws.collect(), exp_design ) 
    ROTS( MERGEOUTPUT.out.stdprotquant_qc, MERGEOUTPUT.out.stdpepquant_qc, parameters )

   emit:
   MERGEOUTPUT.out.expdesign
   ROTS.out.protein_quants_rots
   ROTS.out.peptide_quants_rots
}
