{
    "$graph": [
        {
            "class": "Workflow",
            "requirements": [
                {
                    "class": "ScatterFeatureRequirement"
                }
            ],
            "inputs": [
                {
                    "type": {
                        "type": "array",
                        "items": "string"
                    },
                    "id": "#main/messages"
                }
            ],
            "steps": [
                {
                    "run": "#echo.cwl",
                    "scatter": "#main/echo/msg",
                    "in": [
                        {
                            "source": "#main/messages",
                            "id": "#main/echo/msg"
                        }
                    ],
                    "out": [],
                    "id": "#main/echo"
                }
            ],
            "id": "#main",
            "outputs": []
        },
        {
            "class": "CommandLineTool",
            "baseCommand": "echo",
            "inputs": [
                {
                    "type": "string",
                    "inputBinding": {
                        "position": 1
                    },
                    "id": "#echo.cwl/msg"
                }
            ],
            "outputs": [],
            "id": "#echo.cwl"
        }
    ],
    "cwlVersion": "v1.0"
}