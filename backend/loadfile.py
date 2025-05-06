'''
This file is used to load the .txt files into the program and "parse" them to be used.
'''
import pandas as pd

def buildProcessesDF(filelike):
    df = pd.read_csv(filelike, sep=',', header=None, names=["pid", "bt", "at", "priority"])
    df["pid"] = df["pid"].astype(str).str.strip()
    for col in ["bt", "at", "priority"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")  
        df[col] = df[col].fillna(0).astype(int)            

    return df.to_dict(orient="records")

def buildResourcesDF(filelike):
    df = pd.read_csv(filelike, sep=',', header=None, names=["recurso", "contador"])
    return df.to_dict(orient="records")

def buildActionsDF(filelike):
    df = pd.read_csv(filelike, sep=',', header=None, names=["pid", "accion", "recurso", "ciclo"])
    return df.to_dict(orient="records")


'''buildProcessesDF('examples/processes.txt')
buildResourcesDF('examples/resources.txt')
buildActionsDF('examples/actions.txt')'''