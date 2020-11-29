import json
import sys

LINE_LENGTH = 80

def createBoundedHeader(line, fd):
    borderTop = "/**" + "*" * len(line) + "**\n"
    borderBottom = " **" + "*" * len(line) + "**/\n"
    fd.write(borderTop)
    fd.write(" * " + line + " *\n")
    fd.write(borderBottom)

def linedHeader(line, fd):
    asteriskLen = round((LINE_LENGTH - len(line) - 4) / 2)
    output = "/" + "*" * asteriskLen + " " + line
    output += " " + "*" * asteriskLen + "/\n"
    fd.write(output)

def convertLineOfMarkdown(markdown, fd):
    '''Input is a string of markdown'''
    while len(markdown) > 0:
        if len(markdown) > LINE_LENGTH:
            for i in range(LINE_LENGTH, -1, -1):
                if markdown[i] == " " or markdown[i] == "\n": break
            line = "// " + markdown[:i] + "\n"
            markdown = markdown[i + 1:]
        else:
            line = "// " + markdown + "\n"
            markdown = ""
        fd.write(line)

def convertMarkdown(data, fd):
    for line in data:
        if line == "\n":
            fd.write("\n")
        elif line.startswith("#### "):
            fd.write("// " + line)
        elif line.startswith("### "):
            createBoundedHeader(line[4:].rstrip(), fd)
        elif line.startswith("## "):
            linedHeader(line[3:].rstrip(), fd)
        else:
            convertLineOfMarkdown(line, fd)
    fd.write("\n")

def convertCode(data, fd):
    '''Input is a string of code or a list of strings for each line.'''
    if len(data) != 1:
        fd.write("(\n")
        for line in data:
            fd.write(line)
        fd.write("\n)")
    else:
        fd.write(data[0])
    fd.write("\n\n")

def parseJSON(notebook, fd):
    cellsList = notebook["cells"]
    for cellDict in cellsList:
        name = cellDict["cell_type"]
        data = cellDict["source"]
        if name == "markdown":
            convertMarkdown(data, fd)
        elif name == "code":
            convertCode(data, fd)
        else:
            raise("Notebook contains data other than markdown" +
            " code cells")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("   usage: " + sys.argv[0] + " <input_file> <output_file>")
        exit(1)
    else:
        inputPath = sys.argv[1]
        outputPath = sys.argv[2]

        with open(inputPath, "r") as inputFd:
            notebookDict = json.load(inputFd)
            with open(outputPath, "w") as outputFd:
                parseJSON(notebookDict, outputFd)
