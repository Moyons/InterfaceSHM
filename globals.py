import socket

def initialize():
    global maxDatasetsChart, maxDatasets
    global threadComm
    global sock
    global connected
    global testDone
    global infoTest
    global HOST

    HOST = ""
    infoTest = ""
    testDone = False
    connected = False
    sock = socket.socket()
    threadComm = ""
    maxDatasetsChart = 3
    maxDatasets = 8

