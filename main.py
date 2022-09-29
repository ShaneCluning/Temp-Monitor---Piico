from json import loads, dumps
import _ServerManager
from ServerBinding import ServerBinding
import _TimeManager
import _WiFiManager
import TemperatureMonitor
import gc
from _DataManager import getFileContents, writeFileContents
from machine import Pin, PWM

NTP_Controller = _TimeManager
Server = _ServerManager
WiFi_Manager = _WiFiManager
Temperature_Monitor = TemperatureMonitor
Fan_PWM = PWM(Pin(12))


def mainLoop():

    while True:
        try:
            Server.checkConnection()
            Temperature_Monitor.checkTempReads()
            WiFi_Manager.checkWiFi()
            NTP_Controller.checkNTP()
        except Exception as err:
            print("error: %s, %s" % (str(err), str(type(err).__name__)))


def startUp():
    Fan_PWM.freq(1)
    Fan_PWM.duty(1023)
    NTP_Controller.checkNTP()
    WiFi_Manager.checkWiFi()
    loadConfig()
    Server.SERVER_BINDINGS = setupServerBindings()
    Server.start()
    gc.enable()
    gc.collect()
    mainLoop()


def setupServerBindings():
    bindings = []

    newBinding = ServerBinding("Update", updateHandler)
    bindings.append(newBinding)

    newBinding = ServerBinding("GetData", getDataHandler)
    bindings.append(newBinding)

    return bindings


def loadConfig():
    config = loads(getFileContents("config.txt"))
    print("Loaded values: %s from config file: %s" % (str(config), "config.txt"))
    if "location" in config:
        Temperature_Monitor.location = config["location"]


def saveConfig():
    config_object = {
        "location": Temperature_Monitor.location,
    }
    json_string = dumps(config_object)
    # print("Writing config file with values: %s" % json_string)
    writeFileContents("config.txt", json_string)


def updateHandler(conn, url, params):
    updateConfig = False
    response_string = "OK"
    print("Got Update url: %s and params: %s" % (str(url), str(params)))
    for param in params:
        if "location" in param:
            Temperature_Monitor.location = param["location"]
            updateConfig = True
    if updateConfig:
        saveConfig()
    Server.stdResponse(conn, "text/plain", response_string)


def jsonResponseHandler(conn, object):
    Server.stdResponse(conn, "application/json", dumps(object))
    # json_string = dumps(object)
    # print("Responding with: %s" % json_string)


def getDataHandler(conn, url, params):
    print("Got Data url: %s and params: %s" % (str(url), str(params)))
    averageTemp = Temperature_Monitor.calculateAverageTemp()
    current_data_object = {
        "averageTemp": averageTemp,
        "location": Temperature_Monitor.location,
        "time": NTP_Controller.getISO8601TimeString(),
    }
    jsonResponseHandler(conn, current_data_object)


startUp()
