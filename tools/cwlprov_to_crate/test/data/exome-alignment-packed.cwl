{
    "$graph": [
        {
            "class": "Workflow",
            "id": "#main",
            "label": "alignment_workflow",
            "doc": "Exome Alignment Workflow\n",
            "requirements": [
                {
                    "class": "MultipleInputFeatureRequirement"
                }
            ],
            "inputs": [
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "doc": "List of paired-end input FASTQ files",
                    "id": "#main/fastq_files"
                },
                {
                    "type": "string",
                    "doc": "Parsing header which should correlate to FASTQ files",
                    "id": "#main/readgroup"
                },
                {
                    "type": "File",
                    "doc": "Compress FASTA files with the reference genome chromosomes",
                    "id": "#main/reference_fasta"
                },
                {
                    "type": "string",
                    "doc": "Sample name",
                    "id": "#main/sample_name"
                }
            ],
            "steps": [
                {
                    "run": "#bwa-index.cwl",
                    "in": [
                        {
                            "source": "#main/gunzip/output",
                            "id": "#main/bwa_index/reference_genome"
                        }
                    ],
                    "out": [
                        "#main/bwa_index/output"
                    ],
                    "id": "#main/bwa_index"
                },
                {
                    "run": "#bwa-mem.cwl",
                    "in": [
                        {
                            "source": "#main/readgroup",
                            "id": "#main/bwa_mem/read_group"
                        },
                        {
                            "source": "#main/bwa_index/output",
                            "id": "#main/bwa_mem/reference_genome"
                        },
                        {
                            "source": "#main/sample_name",
                            "id": "#main/bwa_mem/sample_name"
                        },
                        {
                            "source": "#main/cutadapt/output",
                            "id": "#main/bwa_mem/trimmed_fastq"
                        }
                    ],
                    "out": [
                        "#main/bwa_mem/output"
                    ],
                    "id": "#main/bwa_mem"
                },
                {
                    "run": "#cutadapt.cwl",
                    "in": [
                        {
                            "source": "#main/fastq_files",
                            "id": "#main/cutadapt/raw_sequences"
                        }
                    ],
                    "out": [
                        "#main/cutadapt/output"
                    ],
                    "id": "#main/cutadapt"
                },
                {
                    "run": "#gunzip.cwl",
                    "in": [
                        {
                            "source": "#main/reference_fasta",
                            "id": "#main/gunzip/reference_genome"
                        }
                    ],
                    "out": [
                        "#main/gunzip/output"
                    ],
                    "id": "#main/gunzip"
                },
                {
                    "run": "#picard_dictionary.cwl",
                    "in": [
                        {
                            "source": "#main/gunzip/output",
                            "id": "#main/picard_dictionary/reference_genome"
                        }
                    ],
                    "out": [
                        "#main/picard_dictionary/output"
                    ],
                    "id": "#main/picard_dictionary"
                },
                {
                    "run": "#picard_markduplicates.cwl",
                    "in": [
                        {
                            "source": "#main/samtools_sort/output",
                            "id": "#main/picard_markduplicates/alignments"
                        }
                    ],
                    "out": [
                        "#main/picard_markduplicates/output"
                    ],
                    "id": "#main/picard_markduplicates"
                },
                {
                    "run": "#samtools_faidx.cwl",
                    "in": [
                        {
                            "source": "#main/gunzip/output",
                            "id": "#main/samtools_faidx/sequences"
                        }
                    ],
                    "out": [
                        "#main/samtools_faidx/output"
                    ],
                    "id": "#main/samtools_faidx"
                },
                {
                    "run": "#samtools_sort.cwl",
                    "in": [
                        {
                            "source": "#main/bwa_mem/output",
                            "id": "#main/samtools_sort/bam_unsorted"
                        }
                    ],
                    "out": [
                        "#main/samtools_sort/output"
                    ],
                    "id": "#main/samtools_sort"
                }
            ],
            "https://schema.org/author": [
                {
                    "class": "https://schema.org/Person",
                    "https://schema.org/identifier": "https://orcid.org/0000-0003-4929-1219",
                    "https://schema.org/email": "mailto:laura.rodriguez@bsc.es",
                    "https://schema.org/name": "Laura Rodr\u00edguez-Navas"
                }
            ],
            "https://schema.org/dateCreated": "2021-02-19",
            "https://schema.org/license": "https://spdx.org/licenses/Apache-2.0",
            "outputs": [
                {
                    "type": "File",
                    "outputSource": "#main/picard_markduplicates/output",
                    "doc": "Sorted aligned BAM file",
                    "id": "#main/sorted_bam"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#bwa-index.cwl",
            "label": "bwa_index",
            "requirements": [
                {
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "quay.io/biocontainers/bwa:0.7.17--h84994c4_5",
                    "class": "DockerRequirement"
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
                    "id": "#bwa-index.cwl/bwa-index/algorithm"
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
                    "id": "#bwa-index.cwl/bwa-index/block_size"
                },
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 4
                    },
                    "id": "#bwa-index.cwl/bwa-index/reference_genome"
                }
            ],
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
                    "id": "#bwa-index.cwl/bwa-index/output"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#bwa-mem.cwl",
            "label": "bwa_mem",
            "requirements": [
                {
                    "listing": [
                        {
                            "entry": "$(inputs.trimmed_fastq)"
                        },
                        {
                            "entry": "$(inputs.reference_genome)"
                        }
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "quay.io/biocontainers/bwa:0.7.17--h84994c4_5",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "bwa",
                "mem",
                "-M",
                "-p"
            ],
            "inputs": [
                {
                    "type": "string",
                    "default": "@RG\\\\tID:H947YADXX\\\\tSM:NA12878\\\\tPL:ILLUMINA",
                    "inputBinding": {
                        "position": 2,
                        "prefix": "-R"
                    },
                    "id": "#bwa-mem.cwl/bwa-mem/read_group"
                },
                {
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
                    ],
                    "id": "#bwa-mem.cwl/bwa-mem/reference_genome"
                },
                {
                    "type": "string",
                    "id": "#bwa-mem.cwl/bwa-mem/sample_name"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "2",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "-t"
                    },
                    "id": "#bwa-mem.cwl/bwa-mem/threads"
                },
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 4
                    },
                    "id": "#bwa-mem.cwl/bwa-mem/trimmed_fastq"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.sam"
                    },
                    "id": "#bwa-mem.cwl/bwa-mem/output"
                }
            ],
            "stdout": "$(inputs.sample_name).sam"
        },
        {
            "class": "CommandLineTool",
            "id": "#cutadapt.cwl",
            "label": "cutadapt2",
            "requirements": [
                {
                    "listing": [
                        {
                            "entry": "$(inputs.raw_sequences)"
                        },
                        {
                            "entry": "$(inputs.adaptors_file)"
                        }
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "quay.io/biocontainers/cutadapt:1.18--py36h14c3975_1",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "cutadapt",
                "--interleaved"
            ],
            "arguments": [
                {
                    "position": 1,
                    "prefix": "-j",
                    "valueFrom": "0"
                },
                {
                    "position": 2,
                    "prefix": "--error-rate",
                    "valueFrom": "0.2"
                },
                {
                    "position": 3,
                    "prefix": "--overlap",
                    "valueFrom": "6"
                },
                {
                    "position": 4,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.raw_sequences[0].basename + \".trimmed.fastq.gz\")"
                }
            ],
            "inputs": [
                {
                    "type": [
                        "null",
                        "File"
                    ],
                    "inputBinding": {
                        "position": 10,
                        "prefix": "-a"
                    },
                    "id": "#cutadapt.cwl/cutadapt2/adaptors_file"
                },
                {
                    "type": {
                        "type": "array",
                        "items": "File"
                    },
                    "inputBinding": {
                        "position": 20,
                        "prefix": "",
                        "separate": false
                    },
                    "id": "#cutadapt.cwl/cutadapt2/raw_sequences"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.trimmed.fastq.gz"
                    },
                    "id": "#cutadapt.cwl/cutadapt2/output"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#gunzip.cwl",
            "label": "gunzip",
            "requirements": [
                {
                    "listing": [
                        "$(inputs.reference_genome)"
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "alpine:3.9",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "gunzip"
            ],
            "arguments": [
                "-c",
                "-v"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#gunzip.cwl/gunzip/reference_genome"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "streamable": true,
                    "id": "#gunzip.cwl/gunzip/output",
                    "outputBinding": {
                        "glob": "$(inputs.reference_genome.nameroot)"
                    }
                }
            ],
            "stdout": "$(inputs.reference_genome.nameroot)"
        },
        {
            "class": "CommandLineTool",
            "id": "#picard_dictionary.cwl",
            "label": "picard_markduplicates",
            "requirements": [
                {
                    "listing": [
                        {
                            "entry": "$(inputs.reference_genome)"
                        }
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "quay.io/biocontainers/picard:2.22.2--0",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "picard",
                "CreateSequenceDictionary"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "R=",
                        "separate": false
                    },
                    "id": "#picard_dictionary.cwl/picard_markduplicates/reference_genome"
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
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.dict"
                    },
                    "id": "#picard_dictionary.cwl/picard_markduplicates/output"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#picard_markduplicates.cwl",
            "label": "picard_markduplicates",
            "requirements": [
                {
                    "listing": [
                        {
                            "entry": "$(inputs.alignments)"
                        }
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "quay.io/biocontainers/picard:2.22.2--0",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "picard",
                "MarkDuplicates"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 2,
                        "prefix": "INPUT=",
                        "separate": false
                    },
                    "id": "#picard_markduplicates.cwl/picard_markduplicates/alignments"
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
                    "valueFrom": "$(inputs.alignments.nameroot).metrics.txt",
                    "separate": false
                },
                {
                    "position": 3,
                    "prefix": "OUTPUT=",
                    "valueFrom": "$(inputs.alignments.nameroot).md.bam",
                    "separate": false
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.md.bam"
                    },
                    "secondaryFiles": [
                        "^.bai"
                    ],
                    "id": "#picard_markduplicates.cwl/picard_markduplicates/output"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#samtools_faidx.cwl",
            "label": "samtools-faidx",
            "doc": "Indexing a FASTA file",
            "requirements": [
                {
                    "listing": [
                        {
                            "entry": "$(inputs.sequences)"
                        }
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "quay.io/biocontainers/samtools:1.5--2",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "samtools",
                "faidx"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#samtools_faidx.cwl/samtools-faidx/sequences"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.fa"
                    },
                    "secondaryFiles": [
                        ".fai"
                    ],
                    "id": "#samtools_faidx.cwl/samtools-faidx/output"
                }
            ]
        },
        {
            "class": "CommandLineTool",
            "id": "#samtools_sort.cwl",
            "label": "samtools_sort",
            "doc": "Sort a BAM file",
            "requirements": [
                {
                    "listing": [
                        {
                            "entry": "$(inputs.bam_unsorted)"
                        }
                    ],
                    "class": "InitialWorkDirRequirement"
                },
                {
                    "class": "InlineJavascriptRequirement"
                }
            ],
            "hints": [
                {
                    "dockerPull": "quay.io/biocontainers/samtools:1.5--2",
                    "class": "DockerRequirement"
                }
            ],
            "baseCommand": [
                "samtools",
                "sort"
            ],
            "inputs": [
                {
                    "type": "File",
                    "inputBinding": {
                        "position": 2
                    },
                    "id": "#samtools_sort.cwl/samtools-sort/bam_unsorted"
                },
                {
                    "type": [
                        "null",
                        "string"
                    ],
                    "default": "8",
                    "inputBinding": {
                        "position": 1,
                        "prefix": "--threads"
                    },
                    "id": "#samtools_sort.cwl/samtools-sort/threads"
                }
            ],
            "arguments": [
                {
                    "position": 2,
                    "prefix": "-o",
                    "valueFrom": "$(inputs.bam_unsorted.nameroot).sorted.bam"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "outputBinding": {
                        "glob": "*.sorted.bam"
                    },
                    "id": "#samtools_sort.cwl/samtools-sort/output"
                }
            ]
        }
    ],
    "cwlVersion": "v1.0",
    "$schemas": [
        "http://edamontology.org/EDAM_1.18.owl",
        "https://schema.org/version/latest/schemaorg-current-https.rdf"
    ],
    "$namespaces": {
        "s": "https://schema.org/",
        "edam": "http://edamontology.org/"
    }
}
