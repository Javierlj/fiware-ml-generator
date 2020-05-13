#!/usr/bin/python

from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from pprint import pprint
import os
import sys


style = style_from_dict({
    Token.Separator: '#cc5454',
    Token.QuestionMark: '#673ab7 bold',
    Token.Selected: '#cc5454',  # default
    Token.Pointer: '#673ab7 bold',
    Token.Instruction: '',  # default
    Token.Answer: '#f44336 bold',
    Token.Question: '',
})


csv = sys.argv[1]
os.system("cp " + csv + " ./data.csv")
infile = open('data.csv', 'r')
firstLine = infile.readline()
variables = firstLine.split(",")
variables[-1] = variables[-1].strip()

secondLine = infile.readline()
typesOf = secondLine.split(",")
typesOf[-1] = typesOf[-1].strip()

typesOf = map(lambda x: "Float" if x.isdigit() else "String", typesOf)

# print("variables", variables)
# print("typesOf", typesOf)

questionsInput = [
    {
        'type': 'checkbox',
        'message': 'Select input variables',
        'name': 'Input',
        'choices': map(lambda x: {"name": x}, variables),
        'validate': lambda answer: 'You must choose at least one input.'
        if len(answer) == 0 else True
    },

]

answersInput = prompt(questionsInput, style=style)
inputs = answersInput["Input"]

outputVariables = [x for x in variables if x not in inputs]

questionsOutput = [
    {
        'type': 'list',
        'message': 'Select output variables',
        'name': 'Output',
        'choices': map(lambda x: {"name": x}, outputVariables
                       ),
    }
]


answersOutput = prompt(questionsOutput, style=style)

output = answersOutput["Output"]


def createObj(n):
    return "\""+str(n) + """\": {
"value": 0,
"type": "String"
},\n"""

# Create Prediction Req Entity


# input file
fin = open("entitiesTemplates/createPredictionReqEntity.sh", "rt")
# output file to write the result to
fout = open("entities/createPredictionReqEntity.sh", "wt")
# for each line in the input file
for line in fin:
        # read replace the string and write to output file
    if "inputs" in line:
        fout.write("".join(map(createObj, inputs)))
    else:
        fout.write(line)
# close input and output files
fin.close()
fout.close()

# Create Predictions Res Entity

# input file
fin = open("entitiesTemplates/createPredictionResEntity.sh", "rt")
# output file to write the result to
fout = open("entities/createPredictionResEntity.sh", "wt")
# for each line in the input file
for line in fin:
        # read replace the string and write to output file
    if "inputs" in line:
        fout.write("".join(map(createObj, inputs)))
    else:
        fout.write(line)
# close input and output files
fin.close()
fout.close()


def enumerate(n):
    return "\""+str(n) + "\",\n"


# Subscription Req Predictions Tickets

fin = open("entitiesTemplates/subscribeReqPredictionTicket.sh", "rt")
# output file to write the result to
fout = open("entities/subscribeReqPredictionTicket.sh", "wt")
# for each line in the input file
for line in fin:
        # read replace the string and write to output file
    if "inputs" in line:
        fout.write("".join(map(enumerate, inputs)))
    else:
        fout.write(line)
# close input and output files
fin.close()
fout.close()

# Subscription Res Predictions Tickets

fin = open("entitiesTemplates/subscribeResPredictionTicket.sh", "rt")
# output file to write the result to
fout = open("entities/subscribeResPredictionTicket.sh", "wt")
# for each line in the input file
for line in fin:
        # read replace the string and write to output file
    if "inputs" in line:
        fout.write("".join(map(enumerate, inputs)))
    else:
        fout.write(line)
# close input and output files
fin.close()
fout.close()

# Subscription Req Predictions Tickets

fin = open("entitiesTemplates/subscribeResPredictionTicketDraco.sh", "rt")
# output file to write the result to
fout = open("entities/subscribeResPredictionTicketDraco.sh", "wt")
# for each line in the input file
for line in fin:
        # read replace the string and write to output file
    if "inputs" in line:
        fout.write("".join(map(enumerate, inputs)))
    else:
        fout.write(line)
# close input and output files
fin.close()
fout.close()


# print("inputs", inputs)
# print("output", output)


os.system("sudo docker-compose up")
