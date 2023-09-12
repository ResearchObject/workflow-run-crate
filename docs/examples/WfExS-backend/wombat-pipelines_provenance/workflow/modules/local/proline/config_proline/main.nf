process CONFIG_PROLINE {
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
  path zip_searches
  path param_file
  val parameters
  
  output:
  path "import_file_list.txt" , emit: import_files
  path "*{.t.xml,mzid}" , emit: xml_search_files
  path "lfq_param_file.txt", emit: lfq_param_file
  
  script:
  precursor = parameters.precursor_mass_tolerance.split(' ')
  prec_tol = precursor[0]
  prec_ppm = precursor[1]
  protein_fdr = parameters.ident_fdr_protein * 100
  peptide_fdr = parameters.ident_fdr_peptide * 100
  """
  mkdir ./searchgui_results
  for file in *.zip
  do
  unzip "\$file" -d ./searchgui_results/
  mv \$(find ./ -type f \\( -name "*.t.xml.gz" -o -name "*.mzid" \\)) ./
  gunzip *.t.xml.gz
  rm -rf ./searchgui_results/*
  done
  touch import_file_list.txt
  all_id_files=\$(find ./ -type f \\( -name "*.t.xml" -o -name "*.mzid" \\))
  for file in \$all_id_files
  do
  echo "./\$file" >> import_file_list.txt
  sed -i "s/PEPFDR/expected_fdr=${peptide_fdr}/g" "${param_file}"
  sed -i "s/PROTFDR/expected_fdr=${protein_fdr}/g" "${param_file}"
  sed -i "s/NUMPEPS/threshold=${parameters.min_num_peptides}/g" "${param_file}"
  sed -i "s/moz_tol = 5/moz_tol=${prec_tol}/g" "${param_file}"
  sed -i "s/moz_tol_unit = ppm/moz_tol_unit=${prec_ppm}/g" "${param_file}"
  done
  cp "${param_file}" lfq_param_file.txt
  """    
}    
