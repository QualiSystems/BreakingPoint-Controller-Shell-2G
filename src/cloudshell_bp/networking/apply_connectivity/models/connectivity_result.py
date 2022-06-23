class ConnectivityActionResult(object):
    def __init__(self):
        self.actionId = ""
        self.type = ""
        self.infoMessage = ""
        self.errorMessage = ""
        self.success = True
        self.updatedInterface = ""


class ConnectivitySuccessResponse(ConnectivityActionResult):
    def __init__(self, action, result_string):
        ConnectivityActionResult.__init__(self)
        self.type = action.type
        self.actionId = action.actionId
        self.errorMessage = None
        self.updatedInterface = action.actionTarget.fullName
        self.infoMessage = result_string
        self.success = True


class ConnectivityErrorResponse(ConnectivityActionResult):
    def __init__(self, action, error_string):
        ConnectivityActionResult.__init__(self)
        self.type = action.type
        self.actionId = action.actionId
        self.infoMessage = None
        self.updatedInterface = action.actionTarget.fullName
        self.errorMessage = error_string
        self.success = False
