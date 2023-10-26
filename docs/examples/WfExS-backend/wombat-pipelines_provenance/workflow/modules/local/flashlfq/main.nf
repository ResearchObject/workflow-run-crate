// When running docker, you might need to use sudo sysctl -w vm.max_map_count=262144 as mono might fail
// Also a dirty fix for setting the environmental variables
process FLASHLFQ {
  label 'process_high'
  conda (params.enable_conda ? "bioconda::flashlfq-1.2.4" : null)
  if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
        container "docker://quay.io/biocontainers/flashlfq:1.2.4--hdfd78af_0"
  } else {
        container "quay.io/biocontainers/flashlfq:1.2.4--hdfd78af_0"
  }
  
  publishDir "${params.outdir}/flashlfq", mode:'copy'
 
  input:
  path peptideshaker_out
  path mzmlfiles
  val parameters
  path exp_design
  
  output:
  path "QuantifiedPeaks.tsv", emit: flashlfq_peaks
  path "QuantifiedPeptides.tsv", emit: flashlfq_peptides
  path "QuantifiedProteins.tsv", emit: flashlfq_proteins
  
  script:
  // check if parameters.protein_inference is set to "unique" or "shared"
  def protein_inference = false
  if (parameters.protein_inference.equals("shared")) {
        protein_inference = true
  } else {
        if (!parameters.protein_inference.equals("unique")) {
        error "Protein inference must be set to 'shared' or 'unique'"
        }
  }


  if (workflow.containerEngine == 'singularity'|| workflow.containerEngine == 'apptainer') {
  """
  first_line=""
  # avoid exp_design ending with .txt
  mv "${exp_design}" exp_design.tsv
  for file in *.txt
  do
    echo \$file
    tail -n +2 "\$file" >> tlfq_ident.tabular
    first_line=\$(head -n1 "\$file")
  done
  # Use awk to add 3 new columns rep, frac, trep with ones to exp_design file
  #awk 'NR==1{print \$0"\trep\tfrac\ttrep"} NR>1{print \$0"\t1\t1\t1"}' "exp_design.tsv" > ExperimentalDesign.tsv
  cp exp_design.tsv ExperimentalDesign.tsv
  
  # Remove .raw and .mzml from file names in first column of ExperimentalDesign.tsv
  sed -i 's/.mzML//g' ExperimentalDesign.tsv
  sed -i 's/.raw//g' ExperimentalDesign.tsv
  sed       -i 's/.Raw//g' ExperimentalDesign.tsv
  sed -i 's/.RAW//g' ExperimentalDesign.tsv
  # Add first line to tlfq_ident.tabular
  echo "\$first_line" | cat - tlfq_ident.tabular > lfq_ident.tabular
  # Needed as path is overwritten when running with singularity
  PATH=\$PATH:/usr/local/lib/dotnet:/usr/local/lib/dotnet/tools
  CONDA_PREFIX=/usr/local FlashLFQ --idt "lfq_ident.tabular" --rep "./" --out ./ --mbr ${parameters.enable_match_between_runs} --ppm ${parameters.precursor_mass_tolerance} --sha ${protein_inference} --thr ${task.cpus}
  """
  } else {
  """
  first_line=""
  # avoid exp_design ending with .txt
  mv "${exp_design}" exp_design.tsv
  for file in *.txt
  do
    echo \$file
    tail -n +2 "\$file" >> tlfq_ident.tabular
    first_line=\$(head -n1 "\$file")
  done
  # Use awk to add 3 new columns rep, frac, trep with ones to exp_design file
  #awk 'NR==1{print \$0"\trep\tfrac\ttrep"} NR>1{print \$0"\t1\t1\t1"}' "exp_design.tsv" > ExperimentalDesign.tsv
  cp exp_design.tsv ExperimentalDesign.tsv
  
  # Remove .raw and .mzml from file names in first column of ExperimentalDesign.tsv
  sed -i 's/.mzML//g' ExperimentalDesign.tsv
  sed -i 's/.raw//g' ExperimentalDesign.tsv
  sed       -i 's/.Raw//g' ExperimentalDesign.tsv
  sed -i 's/.RAW//g' ExperimentalDesign.tsv
  # Add first line to tlfq_ident.tabular
  echo "\$first_line" | cat - tlfq_ident.tabular > lfq_ident.tabular
  FlashLFQ --idt "lfq_ident.tabular" --rep "./" --out ./ --mbr ${parameters.enable_match_between_runs} --ppm ${parameters.precursor_mass_tolerance} --sha ${protein_inference} --thr ${task.cpus}
  """
  }
  
}    
