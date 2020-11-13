import json
import sys

ANSWER_PHRASE = "Your code here"

def clearCellAnswers(cellDict):
    # slightly unclear but it seems like the source code
    # can be formatted as either a single string or a 
    # list of strings where each line is an item in the 
    # list.  They are showing up as a list of lines on
    # my machine.
    source = cellDict["source"]
    if isinstance(source, str):
        raise("string found for source.  Examine!")
    else:
        for lineNum, line in enumerate(source):
            if ANSWER_PHRASE.lower() in line.lower():
                clearedSource = source[:lineNum + 1]
                cellDict["source"] = clearedSource
                break

def removeAnswers(answersDict):
    listOfCellsDict = answersDict["cells"]
    for cellDict in listOfCellsDict:
        if cellDict["cell_type"] == "code":
            cellDict["execution_count"] = None
            cellDict["outputs"] = []
            clearCellAnswers(cellDict)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("   usage: " + sys.argv[0] + " <input_file> <output_file>")
        exit(1)
    else:
        inputPath = sys.argv[1]
        outputPath = sys.argv[2]

        with open(inputPath, "r") as inputFd:
            notebookDict = json.load(inputFd)
            removeAnswers(notebookDict)

        with open(outputPath, "w") as outputFd:
            json.dump(notebookDict, outputFd)
