#!/usr/bin/python

from __future__ import print_function, unicode_literals
from PyInquirer import style_from_dict, Token, prompt, Separator
from dateutil.parser import parse
from pprint import pprint
import os
import sys
import json


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
# Variables contains all the columns in csv
variables = firstLine.split(",")
variables[-1] = variables[-1].strip()

secondLine = infile.readline()

typesOf = secondLine.split(",")
typesOf[-1] = typesOf[-1].strip()


def determinar_tipo(i, valor):
    try:
        int(valor)
    except ValueError:
        pass
    else:
        return "Int"
    try:
        float(valor)
    except ValueError:
        pass
    else:
        return "Float"
    try:
        parse(valor)
    except ValueError:
        return "String"
    else:
        return "Date"


typesOf = list(map(determinar_tipo, enumerate(typesOf), typesOf))


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

typesOfInputs = []

for i in inputs:
    index = variables.index(i)
    typesOfInputs.append(typesOf[index])


# Create JSON for web


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

outputIndex = variables.index(output)
typeOfOutput = typesOf[outputIndex]

jsonData = {}
jsonData["inputs"] = []
for i in range(len(inputs)):
    jsonData["inputs"].append({
        "name": inputs[i],
        "type": typesOfInputs[i]
    })
jsonData["output"] = {
    "name": output,
    "type": typeOfOutput
}

with open('web/public/form.json', 'w') as outfile:
    json.dump(jsonData, outfile)

# Function to format text


def createObj(v, t):
    return "\"{}\": {{\"value\": 0,\"type\": \"{}\"}}".format(v, t)


def enumerate(v):
    return "\"{}\"".format(v)

# Create Prediction Req Entity


fin = open("entitiesTemplates/createPredictionReqEntity.sh", "rt")
fout = open("entities/createPredictionReqEntity.sh", "wt")
for line in fin:
    if "inputs" in line:
        fout.write(",".join(map(createObj, inputs, typesOfInputs)))
    else:
        fout.write(line)
fin.close()
fout.close()

os.system("sudo chmod +x ./entities/createPredictionReqEntity.sh")


# Create Predictions Res Entity

fin = open("entitiesTemplates/createPredictionResEntity.sh", "rt")
fout = open("entities/createPredictionResEntity.sh", "wt")
for line in fin:
    if "inputs" in line:
        fout.write(",".join(map(createObj, inputs, typesOfInputs)))
    else:
        fout.write(line)
fin.close()
fout.close()

os.system("sudo chmod +x ./entities/createPredictionResEntity.sh")


# Subscription Req Predictions Tickets

fin = open("entitiesTemplates/subscribeReqPredictionTicket.sh", "rt")
fout = open("entities/subscribeReqPredictionTicket.sh", "wt")
for line in fin:
    if "inputs" in line:
        fout.write(",".join(map(enumerate, inputs)))
    else:
        fout.write(line)
fin.close()
fout.close()

os.system("sudo chmod +x ./entities/subscribeReqPredictionTicket.sh")


# Subscription Res Predictions Tickets

fin = open("entitiesTemplates/subscribeResPredictionTicket.sh", "rt")
fout = open("entities/subscribeResPredictionTicket.sh", "wt")
for line in fin:
    if "inputs" in line:
        fout.write(",".join(map(enumerate, inputs)))
    else:
        fout.write(line)
fin.close()
fout.close()

os.system("sudo chmod +x ./entities/subscribeResPredictionTicket.sh")


# Subscription Req Predictions Tickets

fin = open("entitiesTemplates/subscribeResPredictionTicketDraco.sh", "rt")
fout = open("entities/subscribeResPredictionTicketDraco.sh", "wt")
for line in fin:
    if "inputs" in line:
        fout.write(",".join(map(enumerate, inputs)))
    else:
        fout.write(line)
fin.close()
fout.close()

os.system("sudo chmod +x ./entities/subscribeResPredictionTicketDraco.sh")


# Modify Training Job

# TO DO: all types
def strucFields(v, t):
    return "StructField(\"{}\", {}Type)".format(v, t)


fin = open("prediction-job/src/main/scala/org/fiware/cosmos/orion/spark/connector/prediction/TrainingJobTemplate.scala", "rt")
# output file to write the result to
fout = open("prediction-job/src/main/scala/org/fiware/cosmos/orion/spark/connector/prediction/TrainingJob.scala", "wt")

for line in fin:
    if "StructFields" in line:
        fout.write(",".join(map(strucFields, variables, typesOf)))
    elif "outputColumn" in line:
        fout.write(".withColumnRenamed(\"{}\",\"label\")".format(output))
    elif "inputsColumn" in line:
        fout.write(".setInputCols(Array({}))".format(
            ",".join(map(enumerate, inputs))))
    else:
        fout.write(line)

fin.close()
fout.close()


def typesEnum(v, t):
    return "{}: {}".format(v, t)


def toStringVars(v, t):
    if t == "Int":
        return "\"{0}\": {{ \"value\":${{{0}}}, \"type\": \"Integer\"}}".format(v)
    else:
        return "\"{0}\": {{ \"value\":${{{0}}}, \"type\": \"{1}\"}}".format(v, t)


def inputsVars(v, t):
    return "val {0} = ent.attrs(\"{0}\").value.toString.to{1}".format(v, t)


def predictionResponse(n, t):
    return "pred.get({}).toString.to{}".format(n, t)


fin = open("prediction-job/src/main/scala/org/fiware/cosmos/orion/spark/connector/prediction/PredictionJobTemplate.scala", "rt")
# output file to write the result to
fout = open("prediction-job/src/main/scala/org/fiware/cosmos/orion/spark/connector/prediction/PredictionJob.scala", "wt")

for line in fin:
    if "inputs" in line:
        fout.write(",".join(map(typesEnum, inputs, typesOfInputs)))
    elif "inputsParameter" in line:
        fout.write(",".join(map(toStringVars, inputs, typesOfInputs)))
    elif "inputsEnum" in line:
        fout.write(".setInputCols(Array({}))".format(
            ",".join(map(enumerate, inputs))))
    elif "inputsVars" in line:
        fout.write(".setInputCols(Array({}))".format(
            "\n".join(map(inputsVars, inputs))))
    elif "predictionResponse" in line:
        fout.write(
            ",".join(map(predictionResponse, enumerate(inputs), typesOfInputs)))
    else:
        fout.write(line)

fin.close()
fout.close()
# print("inputs", inputs)
# print("output", output)


os.system("sudo docker-compose up")
