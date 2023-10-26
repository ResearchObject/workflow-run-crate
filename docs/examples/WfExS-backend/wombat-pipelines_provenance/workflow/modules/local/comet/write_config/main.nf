process WRITE_CONFIG {
  label 'process_low'
  label 'process_single_thread'
conda (params.enable_conda ? "bioconda::comet-ms-2021010-h87f3376_1" : null)
if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://quay.io/biocontainers/comet-ms:2021010--h87f3376_1"
} else {
        container "quay.io/biocontainers/comet-ms:2021010--h87f3376_1"
}
  publishDir "${params.outdir}/comet", mode:'copy'
  
  input:
  val parameters
  val ptm_mapping
  
  output:
  path "comet.params", emit: comet_param
  
  script:

  fragments = parameters.fragment_mass_tolerance.split(' ')
  frag_tol = fragments[0] as Float
  // Binning requires half of the tolerance + transformation from ppm to Da 
  frag_tol = ((fragments[1] == "ppm") ? frag_tol*0.0005  : frag_tol/2)
  precursor = parameters.precursor_mass_tolerance.split(' ')
  prec_tol = precursor[0]
  prec_ppm = precursor[1] == "ppm" ? 2 : 0
  // converting to searchgui format
  def enzyme = parameters.enzyme.replaceAll("-", "_")

  ptm_mapping = ptm_mapping.collectEntries()

  def fixed_mods = parameters.fixed_mods.replaceAll("Protein","protein").replaceAll("Peptide","peptide").split(",").collect { mod -> ptm_mapping[mod] }
  def var_mods = parameters.variable_mods.replaceAll("Protein","protein").replaceAll("Peptide","peptide").split(",").collect { mod -> ptm_mapping[mod] }

  if (var_mods.size() > 9) {
      exit("Maximum number of variable modifications is 9")
  }
  

  fixed_map = ["protein N-term": "Nterm_protein", "protein C-term": "Cterm_protein", "peptide N-term": "Nterm_peptide", "peptide C-term": "Cterm_peptide", 
    "G": "G_glycine", "A": "A_alanine", "S": "S_serine", "P": "P_proline", "V": "V_valine", "T": "T_threonine", "C": "C_cysteine", "L": "L_leucine",
    "I": "I_isoleucine", "N": "N_asparagine", "D": "D_aspartic_acid", "K": "K_lysine", "Q": "Q_glutamine", "E": "E_glutamic_acid", "M": "M_methionine",
    "H": "H_histidine", "F": "F_phenylalanine", "R": "R_arginine", "Y": "Y_tyrosine", "W": "W_tryptophan"]
  fixed_out = ""
  if (fixed_mods[0] != null) {
    for (int i=0; i<fixed_mods.size(); i++) {
      tres = "add_" + fixed_map[fixed_mods[i].residue]
      fixed_out += tres + " = " + fixed_mods[i].mass + "\\n"
    }
  }

  String var_out = ""
  var_map = ["protein N-term": 0, "protein C-term": 1, "peptide N-term": 2, "peptide C-term": 3, "G": 0, "A": 0, "S": 0, "P": 0, "V": 0, "T": 0, "C": 0, "L": 0,
    "I": 0, "N": 0, "D": 0, "K": 0, "Q": 0, "E": 0, "M": 0, "H": 0, "F": 0, "R": 0, "Y": 0, "W": 0]
  if (var_mods[0]  != null) {
  for (int i=0; i<var_mods.size(); i++) {
    tmod = var_mods[i]
    tres = tmod.residue
    // check if tres contains "Nterm" or "Cterm"
    if (tres.contains("Nterm")) {
      tres = "n"
    } else if (tres.contains("Cterm")) {
      tres = "c"
    } 
    tentry = "variable_mod" + 0 + (i+1) + "=" + tmod.mass + " " + tres + " 0 5 " + (tres.isLowerCase() ? " 0 " : " -1 ") + var_map[tmod.residue] +
                              " 0 " + (tmod.residue.contains("Phosphorylation") ? 97-976896 : 0) + "\\n"
    var_out += tentry
  }
  }

  ionmap = ["A", "B", "C", "X", "Y", "Z", "Z1", "Z2", "NL"]
  String ions_out = ""
  all_ions = parameters.fions.split(",") +  parameters.rions.split(",")
  all_ions = all_ions.collect{ it.toUpperCase() }
  for (int i=0; i<ionmap.size(); i++) {
    ions_out += "use_" + ionmap[i] + "_ions = " + (ionmap[i] in all_ions ? "1" : "0") + "\\n"
  }


    enzymemap = ["Trypsin": 1, "Trypsin/P": 2, "Lys_C": 3, "Lys_N": 4, "Arg_C": 5, "Asp_N": 6, "CNBr": 7, "Glu_C": 8, "PepsinA": 9, "Chymotrypsin": 10, "Unspecified": 0]
    enzyme = enzymemap[enzyme]
    if (enzyme == null) {
      enzyme = enzymemap["Unspecified"]
    }
    skip_decoy = parameters.add_decoys

  isotope_range = parameters.isotope_error_range
  if (isotope_range > 3) {
    isotope_range = 3
    warning("reduced isotope error range to 3")
  }

  """
    comet -p
    mv comet.params.new comet.params
    if [ "${parameters.add_decoys}" = "${false}" ]
    then
      sed -i 's/^decoy_search.*/decoy_search = 0/' comet.params
    else
      sed -i 's/^decoy_search.*/decoy_search = 1/' comet.params
    fi
    # given in ppm
    sed -i 's/^num_threads.*/'"num_threads = ${task.cpus}"/ comet.params
    sed -i 's/^peptide_mass_tolerance.*/'"peptide_mass_tolerance = ${prec_tol}"/ comet.params
    sed -i 's/^peptide_mass_units.*/'"peptide_mass_units = ${prec_ppm}"/ comet.params
    sed -i 's/^search_enzyme_number.*/'"search_enzyme_number = ${enzyme}"/ comet.params
    # given in da and assuming high resolution
    sed -i 's/^fragment_bin_tol.*/'"fragment_bin_tol = ${frag_tol}"/ comet.params
    sed -i 's/^fragment_bin_offset.*/'"fragment_bin_offset = 0.0"/ comet.params
    # mass range
    sed -i 's/^allowed_missed_cleavage.*/'"allowed_missed_cleavage = ${parameters.allowed_miscleavages}"/  comet.params
    sed -i 's/^max_variable_mods_in_peptide.*/'"max_variable_mods_in_peptide = ${parameters.max_mods}"/ comet.params
    sed -i 's/^isotope_error.*/'"isotope_error = ${isotope_range}"/ comet.params
    sed -i 's/^precursor_charge.*/'"precursor_charge = ${parameters.min_precursor_charge} ${parameters.max_precursor_charge}"/  comet.params  
    sed -i 's/^peptide_length_range.*/'"peptide_length_range = ${parameters.min_peptide_length} ${parameters.max_peptide_length}"/  comet.params  
    insert_line=\$(grep -n use_A_ions comet.params | grep -Eo '^[^:]+' | head -n1)
    sed -i '/^use_/d' comet.params
    sed -i "\$insert_line i ${ions_out}" comet.params
    insert_line=\$(grep -n variable_mod0 comet.params | grep -Eo '^[^:]+' | head -n1)
    sed -i '/^variable_mod0/d' comet.params
    sed -i "\$insert_line i ${var_out}" comet.params
    insert_line=\$(grep -n add_Cterm_peptide comet.params | grep -Eo '^[^:]+' | head -n1)
    sed -i '/^add_/d' comet.params
    sed -i "\$insert_line i ${fixed_out}" comet.params
    """ 
}

    
