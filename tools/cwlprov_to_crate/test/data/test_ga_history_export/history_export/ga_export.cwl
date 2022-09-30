{
    "$graph": [
        {
            "class": "Workflow",
            "cwlVersion": "v1.2.0-dev2",
            "doc": "Abstract CWL Automatically generated from the Galaxy workflow file: Workflow constructed from history 'Minimal-history'",
            "inputs": [
                {
                    "type": "File",
                    "id": "#main/queries_0|input2",
                    "format": "data",
                    "name": "dataset1_txt"
                },
                {
                    "type": "File",
                    "id": "#main/input1",
                    "format": "data",
                    "name": "dataset2_txt"
                }
            ],
            "outputs": [
                {
                    "type": "File",
                    "id": "#main/out_file1",
                    "format": "data",
                    "name": "out_file1"
                }
            ],
            "steps": {
                "2_Concatenate datasets": {
                    "in": {
                        "input1": "dataset2_txt",
                        "queries_0|input2": "dataset1_txt"
                    },
                    "out": [
                        "out_file1"
                    ],
                    "run": {
                        "class": "Operation",
                        "id": "cat1",
                        "inputs": {
                            "input1": {
                                "format": "Any",
                                "type": "File"
                            },
                            "queries_0|input2": {
                                "format": "Any",
                                "type": "File"
                            }
                        },
                        "outputs": {
                            "out_file1": {
                                "doc": "input",
                                "type": "File"
                            }
                        }
                    }
                },
                "3_Select random lines": {
                    "in": {
                        "input": "2_Concatenate datasets/out_file1"
                    },
                    "out": [
                        "out_file1"
                    ],
                    "run": {
                        "class": "Operation",
                        "id": "random_lines1",
                        "inputs": {
                            "input": {
                                "format": "Any",
                                "type": "File"
                            }
                        },
                        "outputs": {
                            "out_file1": {
                                "doc": "input",
                                "type": "File"
                            }
                        }
                    }
                }
            }
        }
    ]
}