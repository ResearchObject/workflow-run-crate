{
    "class": "CommandLineTool",
    "baseCommand": "echo",
    "stdout": "output.txt",
    "inputs": [
        {
            "type": "Any",
            "inputBinding": {
                "prefix": "--in-any"
            },
            "id": "#main/in_any"
        },
        {
            "type": {
                "type": "array",
                "items": "string"
            },
            "inputBinding": {
                "position": 1
            },
            "id": "#main/in_array"
        },
        {
            "type": "boolean",
            "inputBinding": {
                "prefix": "--in-bool"
            },
            "id": "#main/in_bool"
        },
        {
            "type": "double",
            "inputBinding": {
                "prefix": "--in-double"
            },
            "id": "#main/in_double"
        },
        {
            "type": {
                "type": "enum",
                "symbols": [
                    "#main/in_enum/A",
                    "#main/in_enum/B"
                ]
            },
            "inputBinding": {
                "prefix": "--in-enum"
            },
            "id": "#main/in_enum"
        },
        {
            "type": "float",
            "inputBinding": {
                "prefix": "--in-float"
            },
            "id": "#main/in_float"
        },
        {
            "type": "int",
            "inputBinding": {
                "prefix": "--in-int"
            },
            "id": "#main/in_int"
        },
        {
            "type": "long",
            "inputBinding": {
                "prefix": "--in-long"
            },
            "id": "#main/in_long"
        },
        {
            "type": [
                "int",
                "float",
                "null"
            ],
            "default": 9.99,
            "inputBinding": {
                "prefix": "--in-multi"
            },
            "id": "#main/in_multi"
        },
        {
            "type": {
                "type": "record",
                "name": "#main/in_record/in_record",
                "fields": [
                    {
                        "type": "string",
                        "inputBinding": {
                            "prefix": "--in-record-A"
                        },
                        "name": "#main/in_record/in_record/in_record_A"
                    },
                    {
                        "type": "string",
                        "inputBinding": {
                            "prefix": "--in-record-B"
                        },
                        "name": "#main/in_record/in_record/in_record_B"
                    }
                ]
            },
            "id": "#main/in_record"
        },
        {
            "type": "string",
            "inputBinding": {
                "prefix": "--in-str"
            },
            "id": "#main/in_str"
        }
    ],
    "id": "#main",
    "outputs": [
        {
            "type": "File",
            "id": "#main/cl_dump",
            "outputBinding": {
                "glob": "output.txt"
            }
        }
    ],
    "cwlVersion": "v1.0"
}