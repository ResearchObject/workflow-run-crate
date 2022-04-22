{
    "class": "CommandLineTool",
    "baseCommand": [
        "echo",
        "-n",
        "{\"answer\": 42}"
    ],
    "stdout": "cwl.output.json",
    "inputs": [],
    "id": "#main",
    "outputs": [
        {
            "type": "int",
            "id": "#main/answer"
        }
    ],
    "cwlVersion": "v1.0"
}