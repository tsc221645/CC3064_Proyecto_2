'''
This file is used to load the .txt files into the program and "parse" them to be used.
'''
import pandas as pd

#This function builds the processes provided by the .txt file
def buildProcessesDF(filepath):
    print("Build Processes")
    processes_df = pd.read_csv(filepath, sep=',',header=0)
    print(processes_df)


# This function builds the resources provided by the .txt file
def buildResourcesDF(filepath):
    print("Build Resources")
    resources_df = pd.read_csv(filepath, sep=',',header=0)
    print(resources_df)


# this function builds the actions provided by the .txt file
def buildActionsDF(filepath):
    print("Build Actions")
    actions_df = pd.read_csv(filepath, sep=',',header=0)
    print(actions_df)


buildProcessesDF('examples/processes.txt')
buildResourcesDF('examples/resources.txt')
buildActionsDF('examples/actions.txt')