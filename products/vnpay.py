
import hashlib
import hmac
import urllib.parse


class vnpay:
    request_data = {}
    response_data = {}

    def __init__(self):
        self.request_data = {}
        self.response_data = {}

    def get_payment_url(self, vnpay_payment_url, secret_key):
        inputData = sorted(self.request_data.items())
        queryString = ""
        hasData = ""
        seq = 0
        for key, val in inputData:
            if seq == 1:
                queryString = queryString + "&" + key + "=" + urllib.parse.quote(str(val))
            else:
                seq = 1
                queryString = key + "=" + urllib.parse.quote(str(val))

        hashValue = self.__hmacsha512(secret_key, queryString)
        return vnpay_payment_url + "?" + queryString + "&vnp_SecureHash=" + hashValue

    def validate_response(self, secret_key):
        vnp_SecureHash = self.response_data.get('vnp_SecureHash')
        # Remove hash params
        if 'vnp_SecureHash' in self.response_data:
            self.response_data.pop('vnp_SecureHash')

        if 'vnp_SecureHashType' in self.response_data:
            self.response_data.pop('vnp_SecureHashType')

        inputData = sorted(self.response_data.items())
        hasData = ""
        seq = 0
        for key, val in inputData:
            if str(key).startswith('vnp_'):
                if seq == 1:
                    hasData = hasData + "&" + str(key) + "=" + urllib.parse.quote(str(val))
                else:
                    seq = 1
                    hasData = str(key) + "=" + urllib.parse.quote(str(val))

        hashValue = self.__hmacsha512(secret_key, hasData)

        print(f'Validate response hash: {hashValue} vs {vnp_SecureHash}')

        return vnp_SecureHash == hashValue

    @staticmethod
    def __hmacsha512(key, data):
        byteKey = key.encode('utf-8')
        byteData = data.encode('utf-8')
        return hmac.new(byteKey, byteData, hashlib.sha512).hexdigest()
