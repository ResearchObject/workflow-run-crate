{
    "$graph": [
        {
            "class": "CommandLineTool",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/biocontainers/bwa:0.7.17--h84994c4_5"
                },
                {
                    "class": "InitialWorkDirRequirement",
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }
                    ]
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 10500,
                    "tmpdirMin": 10500
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "ramMin": 4000,
                    "coresMin": 1
                }
            ],
            "baseCommand": [
                "bwa",
                "index"
            ],
            "inputs": [
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "inputBinding": {
                        "prefix": "-a"
                    },
                    "doc": "BWT construction algorithm: bwtsw or is (Default: auto)\n",
                    "id": "#bwa-index.cwl/algorithm"
                },
                {
                    "type": [
                        "null",
                        "int"
                    ],
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-b"
                    },
                    "id": "#bwa-index.cwl/block_size"
                },
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 4
                    },
                    "id": "#bwa-index.cwl/reference_genome"
                }
            ],
            "id": "#bwa-index.cwl",
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.fa"
                    },
                    "secondaryFiles": [
                        ".amb",
                        ".ann",
                        ".bwt",
                        ".pac",
                        ".sa"
                    ],
                    "id": "#bwa-index.cwl/output"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "bwa",
                "mem",
                "-M",
                "-p"
            ],
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "MultipleInputFeatureRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/biocontainers/bwa:0.7.17--h84994c4_5"
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 10500,
                    "tmpdirMin": 10700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 4,
                    "ramMin": 4000
                }
            ],
            "inputs": [
                {
                    "id": "#bwa-mem.cwl/trimmed_fastq",
                    "type": "File",
                    "inputBinding": {
                        "position": 4
                    }
                },
                {
                    "id": "#bwa-mem.cwl/reference_genome",
                    "type": "File",
                    "inputBinding": {
                        "position": 3
                    },
                    "secondaryFiles": [
                        ".amb",
                        ".ann",
                        ".bwt",
                        ".pac",
                        ".sa"
                    ]
                },
                {
                    "id": "#bwa-mem.cwl/sample_name",
                    "type": "string"
                },
                {
                    "id": "#bwa-mem.cwl/threads",
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "2",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-t"
                    },
                    "doc": "-t INT        number of threads [1]"
                },
                {
                    "id": "#bwa-mem.cwl/read_group",
                    "type": "string",
                    "default": "@RG\\\\tID:H947YADXX\\\\tSM:NA12878\\\\tPL:ILLUMINA",
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-R"
                    }
                }
            ],
            "stdout": "$(inputs.sample_name).sam",
            "arguments": [
                {
                    "position": 2,
                    "prefix": "-M"
                },
                {
                    "position": 2,
                    "prefix": "-p"
                }
            ],
            "outputs": [
                {
                    "id": "#bwa-mem.cwl/aligned_sam",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.sam"
                    }
                }
            ],
            "id": "#bwa-mem.cwl"
        },
        {
            "class": "CommandLineTool",
            "id": "#cutadapt-v.1.18.cwl",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/biocontainers/cutadapt:1.18--py36h14c3975_1"
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 2500,
                    "tmpdirMin": 2500
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 4,
                    "ramMin": 4000
                }
            ],
            "baseCommand": [
                "cutadapt",
                "--interleaved"
            ],
            "arguments": [
                {
                    "position": 4,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.raw_sequences[0].basename + \".trimmed.fastq.gz\")"
                },
                {
                    "position": 3,
                    "prefix": "--overlap",
                    "valueFrom": "6"
                },
                {
                    "position": 1,
                    "prefix": "-j",
                    "valueFrom": "0"
                },
                {
                    "position": 2,
                    "prefix": "--error-rate",
                    "valueFrom": "0.2"
                }
            ],
            "inputs": [
                {
                    "id": "#cutadapt-v.1.18.cwl/cutadapt2/raw_sequences",
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "inputBinding": {
                        "position": 20,
                        "prefix": "",
                        "separate": false
                    }
                },
                {
                    "id": "#cutadapt-v.1.18.cwl/cutadapt2/adaptors_file",
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "position": 10,
                        "prefix": "-a"
                    }
                }
            ],
            "outputs": [
                {
                    "id": "#cutadapt-v.1.18.cwl/cutadapt2/trimmed_fastq",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.trimmed.fastq.gz"
                    }
                }
            ],
            "label": "cutadapt"
        },
        {
            "class": "CommandLineTool",
            "id": "#gatk-base_recalibration.cwl",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                },
                {
                    "class": "InitialWorkDirRequirement",
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        },
                        {
                            "entry": "$(inputs.dict)"
                        }
                    ]
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 4,
                    "ramMin": 4000
                }
            ],
            "baseCommand": [
                "java",
                "-jar",
                "/usr/GenomeAnalysisTK.jar",
                "-T",
                "BaseRecalibrator"
            ],
            "inputs": [
                {
                    "id": "#gatk-base_recalibration.cwl/gatk-base_recalibration/reference_genome",
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-R"
                    },
                    "secondaryFiles": [
                        ".fai"
                    ]
                },
                {
                    "id": "#gatk-base_recalibration.cwl/gatk-base_recalibration/dict",
                    "type": "File"
                },
                {
                    "id": "#gatk-base_recalibration.cwl/gatk-base_recalibration/unzipped_known_sites_file",
                    "type": "File"
                },
                {
                    "id": "#gatk-base_recalibration.cwl/gatk-base_recalibration/input",
                    "type": "File",
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-I"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                },
                {
                    "id": "#gatk-base_recalibration.cwl/gatk-base_recalibration/known_indels_file",
                    "type": "File"
                },
                {
                    "id": "#gatk-base_recalibration.cwl/gatk-base_recalibration/threads",
                    "type": [
                        "null",
                        "string"
                    ]
                }
            ],
            "arguments": [
                {
                    "position": 0,
                    "prefix": "-dt",
                    "valueFrom": "NONE"
                },
                {
                    "position": 0,
                    "prefix": "-nct",
                    "valueFrom": "$(inputs.threads)"
                },
                {
                    "position": 0,
                    "prefix": "--knownSites",
                    "valueFrom": "$(inputs.known_indels_file)"
                },
                {
                    "position": 0,
                    "prefix": "--knownSites",
                    "valueFrom": "$(inputs.unzipped_known_sites_file)"
                },
                {
                    "position": 3,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.input.nameroot).recalibrated.grp"
                }
            ],
            "outputs": [
                {
                    "id": "#gatk-base_recalibration.cwl/gatk-base_recalibration/br_model",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.grp"
                    }
                }
            ],
            "label": "gatk3-base_recalibration"
        },
        {
            "class": "CommandLineTool",
            "id": "#gatk-base_recalibration_print_reads.cwl",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                },
                {
                    "class": "InitialWorkDirRequirement",
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        },
                        {
                            "entry": "$(inputs.dict)"
                        },
                        {
                            "entry": "$(inputs.br_model)"
                        }
                    ]
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 8,
                    "ramMin": 8000
                }
            ],
            "baseCommand": [
                "java",
                "-jar",
                "/usr/GenomeAnalysisTK.jar",
                "-T",
                "PrintReads"
            ],
            "inputs": [
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/gatk_base_recalibration_print_reads/reference_genome",
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-R"
                    },
                    "secondaryFiles": [
                        ".fai"
                    ]
                },
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/gatk_base_recalibration_print_reads/dict",
                    "type": "File"
                },
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/gatk_base_recalibration_print_reads/input",
                    "type": [
                        "File"
                    ],
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-I"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                },
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/gatk_base_recalibration_print_reads/br_model",
                    "type": [
                        "File"
                    ],
                    "inputBinding": {
                        "position": 4,
                        "prefix": "-BQSR"
                    }
                }
            ],
            "arguments": [
                {
                    "position": 0,
                    "prefix": "-dt",
                    "valueFrom": "NONE"
                },
                {
                    "position": 3,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.input.nameroot).bqsr.bam"
                }
            ],
            "outputs": [
                {
                    "id": "#gatk-base_recalibration_print_reads.cwl/gatk_base_recalibration_print_reads/bqsr_bam",
                    "type": "File",
                    "outputBinding": {
                        "glob": "$(inputs.input.nameroot).bqsr.bam"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }
            ],
            "label": "gatk-base_recalibration_print_reads"
        },
        {
            "class": "CommandLineTool",
            "id": "#gatk-haplotype_caller.cwl",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                },
                {
                    "class": "InitialWorkDirRequirement",
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        },
                        {
                            "entry": "$(inputs.dict)"
                        }
                    ]
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 4,
                    "ramMin": 4000
                }
            ],
            "baseCommand": [
                "java",
                "-jar",
                "/usr/GenomeAnalysisTK.jar",
                "-T",
                "HaplotypeCaller",
                "--never_trim_vcf_format_field"
            ],
            "inputs": [
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/reference_genome",
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-R"
                    },
                    "secondaryFiles": [
                        ".fai"
                    ]
                },
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/dict",
                    "type": "File"
                },
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/input",
                    "type": "File",
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-I"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                },
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/chromosome",
                    "type": [
                        "null",
                        "string"
                    ],
                    "inputBinding": {
                        "position": 3,
                        "prefix": "-L"
                    }
                },
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/ploidy",
                    "type": [
                        "null",
                        "int"
                    ],
                    "inputBinding": {
                        "position": 5,
                        "prefix": "-ploidy"
                    }
                },
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/gqb",
                    "type": [
                        "null",
                        {
                            "type": "array",
                            "items": "int",
                            "inputBinding": {
                                "prefix": "--GVCFGQBands"
                            }
                        }
                    ],
                    "inputBinding": {
                        "position": 12
                    }
                },
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/threads",
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "2"
                }
            ],
            "arguments": [
                {
                    "position": 0,
                    "prefix": "--num_cpu_threads_per_data_thread",
                    "valueFrom": "$(inputs.threads)"
                },
                {
                    "position": 0,
                    "prefix": "-dt",
                    "valueFrom": "NONE"
                },
                {
                    "position": 0,
                    "prefix": "-rf",
                    "valueFrom": "BadCigar"
                },
                {
                    "position": 0,
                    "prefix": "-ERC",
                    "valueFrom": "GVCF"
                },
                {
                    "position": 0,
                    "prefix": "-variant_index_type",
                    "valueFrom": "LINEAR"
                },
                {
                    "position": 0,
                    "prefix": "-variant_index_parameter",
                    "valueFrom": "128000"
                },
                {
                    "position": 0,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.input.nameroot).vcf.gz"
                }
            ],
            "outputs": [
                {
                    "id": "#gatk-haplotype_caller.cwl/gatk_haplotypecaller/gvcf",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.gz"
                    },
                    "secondaryFiles": [
                        ".tbi"
                    ]
                }
            ],
            "label": "gatk3-haplotypecaller"
        },
        {
            "class": "CommandLineTool",
            "id": "#gatk-ir.cwl",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                },
                {
                    "class": "InitialWorkDirRequirement",
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        },
                        {
                            "entry": "$(inputs.dict)"
                        }
                    ]
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 8,
                    "ramMin": 8000
                }
            ],
            "baseCommand": [
                "java",
                "-jar",
                "/usr/GenomeAnalysisTK.jar",
                "-T",
                "IndelRealigner"
            ],
            "inputs": [
                {
                    "id": "#gatk-ir.cwl/ir/input",
                    "type": [
                        "File",
                        {
                            "type": "array",
                            "items": "File"
                        }
                    ],
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-I"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                },
                {
                    "id": "#gatk-ir.cwl/ir/rtc_intervals",
                    "type": "File",
                    "inputBinding": {
                        "position": 3,
                        "prefix": "-targetIntervals"
                    }
                },
                {
                    "id": "#gatk-ir.cwl/ir/reference_genome",
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-R"
                    },
                    "secondaryFiles": [
                        ".fai"
                    ]
                },
                {
                    "id": "#gatk-ir.cwl/ir/dict",
                    "type": "File"
                }
            ],
            "arguments": [
                {
                    "position": 5,
                    "prefix": "-dt",
                    "valueFrom": "NONE"
                },
                {
                    "position": 6,
                    "prefix": "--maxReadsForRealignment",
                    "valueFrom": "200000"
                },
                {
                    "position": 10,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.input.nameroot).realigned.bam"
                }
            ],
            "outputs": [
                {
                    "id": "#gatk-ir.cwl/ir/realigned_bam",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.realigned.bam"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                }
            ],
            "label": "ir"
        },
        {
            "class": "CommandLineTool",
            "id": "#gatk3-rtc.cwl",
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "broadinstitute/gatk3:3.6-0"
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 12500,
                    "tmpdirMin": 12500
                },
                {
                    "class": "InitialWorkDirRequirement",
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        },
                        {
                            "entry": "$(inputs.dict)"
                        },
                        {
                            "entry": "$(inputs.known_indels)"
                        }
                    ]
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 4,
                    "ramMin": 8000
                }
            ],
            "baseCommand": [
                "java",
                "-jar",
                "/usr/GenomeAnalysisTK.jar",
                "-T",
                "RealignerTargetCreator"
            ],
            "inputs": [
                {
                    "id": "#gatk3-rtc.cwl/rtc/input",
                    "type": "File",
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-I"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                },
                {
                    "id": "#gatk3-rtc.cwl/rtc/rtc_intervals_name",
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "rtc_intervals.list"
                },
                {
                    "id": "#gatk3-rtc.cwl/rtc/reference_genome",
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-R"
                    },
                    "secondaryFiles": [
                        ".fai"
                    ]
                },
                {
                    "id": "#gatk3-rtc.cwl/rtc/known_indels",
                    "type": "File",
                    "inputBinding": {
                        "position": 4,
                        "prefix": "--known"
                    }
                },
                {
                    "id": "#gatk3-rtc.cwl/rtc/dict",
                    "type": "File"
                }
            ],
            "arguments": [
                {
                    "position": 5,
                    "prefix": "-dt",
                    "valueFrom": "NONE"
                },
                {
                    "position": 3,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.rtc_intervals_name)"
                }
            ],
            "outputs": [
                {
                    "id": "#gatk3-rtc.cwl/rtc/rtc_intervals_file",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.list"
                    }
                }
            ],
            "label": "rtc"
        },
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "gunzip"
            ],
            "arguments": [
                "-c",
                "-v"
            ],
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "jlaitinen/lftpalpine"
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7500
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 2,
                    "ramMin": 5000
                }
            ],
            "inputs": [
                {
                    "id": "#gunzip.cwl/reference_file",
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "inputBinding": {
                        "position": 2
                    }
                }
            ],
            "outputs": [
                {
                    "id": "#gunzip.cwl/unzipped_fasta",
                    "type": "File",
                    "streamable": true,
                    "outputBinding": {
                        "glob": "$(inputs.reference_file[0].nameroot)"
                    }
                }
            ],
            "stdout": "$(inputs.reference_file[0].nameroot)",
            "id": "#gunzip.cwl"
        },
        {
            "class": "CommandLineTool",
            "baseCommand": [
                "gunzip"
            ],
            "arguments": [
                "-c"
            ],
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "jlaitinen/lftpalpine"
                },
                {
                    "class": "ResourceRequirement",
                    "coresMin": 2,
                    "ramMin": 2000,
                    "outdirMin": 12500,
                    "tmpdirMin": 12500
                }
            ],
            "inputs": [
                {
                    "id": "#gunzip_known_sites.cwl/input",
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    }
                }
            ],
            "outputs": [
                {
                    "id": "#gunzip_known_sites.cwl/output",
                    "type": "File",
                    "outputBinding": {
                        "glob": "$(inputs.input.nameroot)"
                    }
                }
            ],
            "stdout": "$(inputs.input.nameroot)",
            "id": "#gunzip_known_sites.cwl"
        },
        {
            "class": "CommandLineTool",
            "id": "#picard_dictionary.cwl",
            "baseCommand": [
                "picard",
                "CreateSequenceDictionary"
            ],
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/biocontainers/picard:2.18.25--0"
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 4,
                    "ramMin": 4000
                }
            ],
            "inputs": [
                {
                    "id": "#picard_dictionary.cwl/picard_markduplicates/reference_genome",
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "R=",
                        "separate": false
                    }
                }
            ],
            "arguments": [
                {
                    "position": 2,
                    "prefix": "O=",
                    "separate": false,
                    "valueFrom": "$(inputs.reference_genome.nameroot).dict"
                }
            ],
            "outputs": [
                {
                    "id": "#picard_dictionary.cwl/picard_markduplicates/dict",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.dict"
                    }
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#picard_markduplicates.cwl",
            "baseCommand": [
                "picard",
                "MarkDuplicates"
            ],
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/biocontainers/picard:2.18.25--0"
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 4,
                    "ramMin": 4000
                }
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 2,
                        "prefix": "INPUT=",
                        "separate": false
                    },
                    "id": "#picard_markduplicates.cwl/picard_markduplicates/input"
                }
            ],
            "arguments": [
                {
                    "position": 0,
                    "prefix": "OPTICAL_DUPLICATE_PIXEL_DISTANCE=",
                    "valueFrom": "100",
                    "separate": false
                },
                {
                    "position": 0,
                    "prefix": "TAGGING_POLICY=",
                    "valueFrom": "All",
                    "separate": false
                },
                {
                    "position": 0,
                    "prefix": "CREATE_INDEX=",
                    "valueFrom": "true",
                    "separate": false
                },
                {
                    "position": 0,
                    "prefix": "REMOVE_DUPLICATES=",
                    "valueFrom": "true",
                    "separate": false
                },
                {
                    "position": 0,
                    "prefix": "TAG_DUPLICATE_SET_MEMBERS=",
                    "valueFrom": "true",
                    "separate": false
                },
                {
                    "position": 0,
                    "prefix": "ASSUME_SORT_ORDER=",
                    "valueFrom": "coordinate",
                    "separate": false
                },
                {
                    "position": 1,
                    "prefix": "METRICS_FILE=",
                    "valueFrom": "$(inputs.input.nameroot).metrics.txt",
                    "separate": false
                },
                {
                    "position": 3,
                    "prefix": "OUTPUT=",
                    "valueFrom": "$(inputs.input.nameroot).md.bam",
                    "separate": false
                }
            ],
            "outputs": [
                {
                    "id": "#picard_markduplicates.cwl/picard_markduplicates/md_bam",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.md.bam"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ]
                },
                {
                    "id": "#picard_markduplicates.cwl/picard_markduplicates/output_metrics",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.metrics.txt"
                    }
                }
            ],
            "label": "picard-MD"
        },
        {
            "class": "CommandLineTool",
            "id": "#samtools_index.cwl",
            "baseCommand": [
                "samtools",
                "faidx"
            ],
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/biocontainers/samtools:1.3.1--5"
                },
                {
                    "class": "InitialWorkDirRequirement",
                    "listing": [
                        {
                            "entry": "$(inputs.input)"
                        }
                    ]
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 8,
                    "ramMin": 8000
                }
            ],
            "inputs": [
                {
                    "id": "#samtools_index.cwl/fastq_index/input",
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    }
                }
            ],
            "outputs": [
                {
                    "id": "#samtools_index.cwl/fastq_index/index_fai",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.fa"
                    },
                    "secondaryFiles": [
                        ".fai"
                    ]
                }
            ],
            "label": "samtools-faidx"
        },
        {
            "class": "CommandLineTool",
            "id": "#samtools_sort_bam.cwl",
            "baseCommand": [
                "samtools",
                "sort"
            ],
            "requirements": [
                {
                    "class": "InlineJavascriptRequirement"
                },
                {
                    "class": "DockerRequirement",
                    "dockerPull": "quay.io/biocontainers/samtools:1.3.1--5"
                },
                {
                    "class": "ResourceRequirement",
                    "outdirMin": 7500,
                    "tmpdirMin": 7700
                }
            ],
            "hints": [
                {
                    "class": "ResourceRequirement",
                    "coresMin": 8,
                    "ramMin": 8000
                }
            ],
            "inputs": [
                {
                    "id": "#samtools_sort_bam.cwl/BAM_index/input",
                    "type": "File",
                    "inputBinding": {
                        "position": 2
                    }
                },
                {
                    "id": "#samtools_sort_bam.cwl/BAM_index/threads",
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "8",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "--threads"
                    }
                }
            ],
            "arguments": [
                {
                    "position": 2,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.input.nameroot).sorted.bam"
                }
            ],
            "outputs": [
                {
                    "id": "#samtools_sort_bam.cwl/BAM_index/sorted_bam",
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.sorted.bam"
                    }
                }
            ],
            "label": "samtools-bam_sort"
        },
        {
            "class": "Workflow",
            "label": "RD_Connect",
            "requirements": [
                {
                    "class": "MultipleInputFeatureRequirement"
                }
            ],
            "inputs": [
                {
                    "type": "string",
                    "doc": "Label of the chromosome to be used for the analysis. By default all the chromosomes are used",
                    "id": "#main/chromosome"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "doc": "List of paired-end input FASTQ files",
                    "id": "#main/fastq_files"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "int"
                    },
                    "default": [
                        20,
                        25,
                        30,
                        35,
                        40,
                        45,
                        50,
                        70,
                        90,
                        99
                    ],
                    "doc": "Exclusive upper bounds for reference confidence GQ bands (must be in [1, 100] and specified in increasing order)",
                    "id": "#main/gqb"
                },
                {
                    "type": "File",
                    "doc": "VCF file correlated to reference genome assembly with known indels",
                    "id": "#main/known_indels_file"
                },
                {
                    "type": "File",
                    "doc": "VCF file correlated to reference genome assembly with know sites (for instance dbSNP)",
                    "id": "#main/known_sites_file"
                },
                {
                    "type": "string",
                    "default": "@RG\\tID:Seq01p\\tSM:Seq01\\tPL:ILLUMINA\\tPI:330",
                    "doc": "Parsing header which should correlate to FASTQ files",
                    "id": "#main/readgroup_str"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "doc": "Compress FASTA files with the reference genome chromosomes",
                    "id": "#main/reference_genome"
                },
                {
                    "type": "string",
                    "default": "ABC3",
                    "doc": "Sample name",
                    "id": "#main/sample_name"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/gatk_haplotype_caller/gvcf",
                    "doc": "unannotated gVCF output file from the mapping and variant calling pipeline",
                    "id": "#main/gvcf"
                },
                {
                    "type": "File",
                    "outputSource": "#main/picard_markduplicates/output_metrics",
                    "doc": "Several metrics about the result",
                    "id": "#main/metrics"
                }
            ],
            "steps": [
                {
                    "id": "#main/unzipped_known_sites",
                    "in": [
                        {
                            "source": "#main/known_sites_file",
                            "id": "#main/unzipped_known_sites/input"
                        }
                    ],
                    "out": [
                        "#main/unzipped_known_sites/output"
                    ],
                    "run": "#gunzip_known_sites.cwl"
                },
                {
                    "id": "#main/unzipped_known_indels",
                    "in": [
                        {
                            "source": "#main/known_indels_file",
                            "id": "#main/unzipped_known_indels/input"
                        }
                    ],
                    "out": [
                        "#main/unzipped_known_indels/output"
                    ],
                    "run": "#gunzip_known_sites.cwl"
                },
                {
                    "id": "#main/gunzip",
                    "in": [
                        {
                            "id": "#main/gunzip/reference_file",
                            "source": [
                                "#main/reference_genome"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/gunzip/unzipped_fasta"
                        }
                    ],
                    "run": "#gunzip.cwl"
                },
                {
                    "id": "#main/picard_dictionary",
                    "in": [
                        {
                            "id": "#main/picard_dictionary/reference_genome",
                            "source": [
                                "#main/gunzip/unzipped_fasta"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/picard_dictionary/dict"
                        }
                    ],
                    "run": "#picard_dictionary.cwl"
                },
                {
                    "id": "#main/cutadapt2",
                    "in": [
                        {
                            "id": "#main/cutadapt2/raw_sequences",
                            "source": [
                                "#main/fastq_files"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/cutadapt2/trimmed_fastq"
                        }
                    ],
                    "run": "#cutadapt-v.1.18.cwl"
                },
                {
                    "id": "#main/bwa_index",
                    "in": [
                        {
                            "id": "#main/bwa_index/reference_genome",
                            "source": [
                                "#main/gunzip/unzipped_fasta"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/bwa_index/output"
                        }
                    ],
                    "run": "#bwa-index.cwl"
                },
                {
                    "id": "#main/samtools_index",
                    "in": [
                        {
                            "id": "#main/samtools_index/input",
                            "source": [
                                "#main/gunzip/unzipped_fasta"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/samtools_index/index_fai"
                        }
                    ],
                    "run": "#samtools_index.cwl"
                },
                {
                    "id": "#main/bwa_mem",
                    "in": [
                        {
                            "id": "#main/bwa_mem/sample_name",
                            "source": [
                                "#main/sample_name"
                            ]
                        },
                        {
                            "id": "#main/bwa_mem/trimmed_fastq",
                            "source": [
                                "#main/cutadapt2/trimmed_fastq"
                            ]
                        },
                        {
                            "id": "#main/bwa_mem/read_group",
                            "source": [
                                "#main/readgroup_str"
                            ]
                        },
                        {
                            "id": "#main/bwa_mem/reference_genome",
                            "source": [
                                "#main/bwa_index/output"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/bwa_mem/aligned_sam"
                        }
                    ],
                    "run": "#bwa-mem.cwl"
                },
                {
                    "id": "#main/samtools_sort",
                    "in": [
                        {
                            "id": "#main/samtools_sort/input",
                            "source": [
                                "#main/bwa_mem/aligned_sam"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/samtools_sort/sorted_bam"
                        }
                    ],
                    "run": "#samtools_sort_bam.cwl"
                },
                {
                    "id": "#main/picard_markduplicates",
                    "in": [
                        {
                            "id": "#main/picard_markduplicates/input",
                            "source": [
                                "#main/samtools_sort/sorted_bam"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/picard_markduplicates/md_bam"
                        },
                        {
                            "id": "#main/picard_markduplicates/output_metrics"
                        }
                    ],
                    "run": "#picard_markduplicates.cwl",
                    "label": "picard-MD"
                },
                {
                    "id": "#main/gatk3-rtc",
                    "in": [
                        {
                            "id": "#main/gatk3-rtc/input",
                            "source": [
                                "#main/picard_markduplicates/md_bam"
                            ]
                        },
                        {
                            "id": "#main/gatk3-rtc/reference_genome",
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        },
                        {
                            "id": "#main/gatk3-rtc/dict",
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        },
                        {
                            "id": "#main/gatk3-rtc/known_indels",
                            "source": [
                                "#main/unzipped_known_indels/output"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/gatk3-rtc/rtc_intervals_file"
                        }
                    ],
                    "run": "#gatk3-rtc.cwl",
                    "label": "gatk3-rtc"
                },
                {
                    "id": "#main/gatk-ir",
                    "in": [
                        {
                            "id": "#main/gatk-ir/input",
                            "source": [
                                "#main/picard_markduplicates/md_bam"
                            ]
                        },
                        {
                            "id": "#main/gatk-ir/rtc_intervals",
                            "source": [
                                "#main/gatk3-rtc/rtc_intervals_file"
                            ]
                        },
                        {
                            "id": "#main/gatk-ir/reference_genome",
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        },
                        {
                            "id": "#main/gatk-ir/dict",
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/gatk-ir/realigned_bam"
                        }
                    ],
                    "run": "#gatk-ir.cwl",
                    "label": "gatk-ir"
                },
                {
                    "id": "#main/gatk-base_recalibration",
                    "in": [
                        {
                            "id": "#main/gatk-base_recalibration/reference_genome",
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        },
                        {
                            "id": "#main/gatk-base_recalibration/dict",
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        },
                        {
                            "id": "#main/gatk-base_recalibration/input",
                            "source": [
                                "#main/gatk-ir/realigned_bam"
                            ]
                        },
                        {
                            "id": "#main/gatk-base_recalibration/unzipped_known_sites_file",
                            "source": [
                                "#main/unzipped_known_sites/output"
                            ]
                        },
                        {
                            "id": "#main/gatk-base_recalibration/known_indels_file",
                            "source": [
                                "#main/unzipped_known_indels/output"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/gatk-base_recalibration/br_model"
                        }
                    ],
                    "run": "#gatk-base_recalibration.cwl",
                    "label": "gatk-base_recalibration"
                },
                {
                    "id": "#main/gatk-base_recalibration_print_reads",
                    "in": [
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/reference_genome",
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        },
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/dict",
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        },
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/input",
                            "source": [
                                "#main/gatk-ir/realigned_bam"
                            ]
                        },
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/br_model",
                            "source": [
                                "#main/gatk-base_recalibration/br_model"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/gatk-base_recalibration_print_reads/bqsr_bam"
                        }
                    ],
                    "run": "#gatk-base_recalibration_print_reads.cwl",
                    "label": "gatk-base_recalibration_print_reads"
                },
                {
                    "id": "#main/gatk_haplotype_caller",
                    "in": [
                        {
                            "id": "#main/gatk_haplotype_caller/reference_genome",
                            "source": [
                                "#main/samtools_index/index_fai"
                            ]
                        },
                        {
                            "id": "#main/gatk_haplotype_caller/dict",
                            "source": [
                                "#main/picard_dictionary/dict"
                            ]
                        },
                        {
                            "id": "#main/gatk_haplotype_caller/input",
                            "source": [
                                "#main/gatk-base_recalibration_print_reads/bqsr_bam"
                            ]
                        },
                        {
                            "id": "#main/gatk_haplotype_caller/chromosome",
                            "source": [
                                "#main/chromosome"
                            ]
                        },
                        {
                            "id": "#main/gatk_haplotype_caller/gqb",
                            "source": [
                                "#main/gqb"
                            ]
                        }
                    ],
                    "out": [
                        {
                            "id": "#main/gatk_haplotype_caller/gvcf"
                        }
                    ],
                    "run": "#gatk-haplotype_caller.cwl",
                    "label": "gatk-haplotype_caller"
                }
            ],
            "id": "#main",
            "https://schema.org/author": [
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "https://orcid.org/0000-0001-7893-2404",
                    "https://schema.org/email": "mailto:raul.tonda@cnag.crg.cat",
                    "https://schema.org/name": "Raul Tonda"
                },
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "https://orcid.org/0000-0003-0807-2570",
                    "https://schema.org/email": "mailto:leslie.matalonga@cnag.crg.eu",
                    "https://schema.org/name": "Leslie Matalonga"
                },
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "https://orcid.org/0000-0003-1687-2754",
                    "https://schema.org/email": "mailto:varma@ebi.ac.uk",
                    "https://schema.org/name": "Susheel Varma"
                }
            ],
            "https://schema.org/contributor": [
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "http://orcid.org/0000-0002-7681-6415",
                    "https://schema.org/email": "mailto:jarno.laitinen@csc.fi",
                    "https://schema.org/name": "Jarno Laitinen"
                },
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/email": "mailto:aniewielska@ebi.ac.uk",
                    "https://schema.org/name": "Ania Niewielska"
                },
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "https://orcid.org/0000-0002-3468-0652",
                    "https://schema.org/email": "mailto:alexander.kanitz@unibas.ch",
                    "https://schema.org/name": "Alex Kanitz"
                },
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "https://orcid.org/0000-0002-4806-5140",
                    "https://schema.org/email": "mailto:jose.m.fernandez@bsc.es",
                    "https://schema.org/name": "Jos\u00e9 M. Fern\u00e1ndez"
                },
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "https://orcid.org/0000-0003-4929-1219",
                    "https://schema.org/email": "mailto:laura.rodriguez@bsc.es",
                    "https://schema.org/name": "Laura Rodr\u00edguez-Navas"
                }
            ],
            "https://schema.org/citation": "https://dx.doi.org/10.1002/humu.23114",
            "https://schema.org/codeRepository": "https://github.com/inab/Wetlab2Variations/",
            "https://schema.org/dateCreated": "2019-03-06",
            "https://schema.org/license": "https://spdx.org/licenses/Apache-2.0"
        }
    ],
    "cwlVersion": "v1.0",
    "$schemas": [
        "https://schema.org/version/latest/schemaorg-current-https.rdf",
        "http://edamontology.org/EDAM_1.18.owl"
    ],
    "$namespaces": {
        "s": "https://schema.org/",
        "edam": "http://edamontology.org/"
    }
}
