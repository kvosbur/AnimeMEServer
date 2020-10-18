

class HTTPResponse:

    @staticmethod
    def makeResponse(responseCode, message, statusCode, data):
        return {"message": message,
                "statusCode": statusCode,
                "data": data}, responseCode

    @staticmethod
    def makeResponseMinimal(responseCode, message):
        return {"message": message}, responseCode
