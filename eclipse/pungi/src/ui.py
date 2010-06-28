import appuifw

def selectDevice(remoteAPI):
    mobileList = remoteAPI.getMobileList()
    deviceNames = []
    for device in mobileList["devices"]:
        deviceNames.append(device["name"])
    choice = appuifw.selection_list(choices = deviceNames, search_field = 1)
    if choice == None:
        raise Exception("A device must be selected")
    else:
        return mobileList["devices"][choice]["ID"]
