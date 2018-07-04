# -*- coding: utf-8 -*-

# Copyright 2017 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Amazon Software License (the "License"). You may not use this file except in
# compliance with the License. A copy of the License is located at
#
#    http://aws.amazon.com/asl/
#
# or in the "license" file accompanying this file. This file is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, express or implied. See the License for the specific
# language governing permissions and limitations under the License.

import http.client
from urllib.parse import urlencode
from jose import jwt
import base64


class ApiAuth:

    def post_to_api(self, payload):
        auth_code = "{}:{}".format(payload['client_id'], payload['client_secret'])
        auth_code = base64.b64encode(bytes(auth_code, "utf-8")).decode("utf-8")
        del payload['client_secret']
        connection = http.client.HTTPSConnection("mansaa.auth.ap-south-1.amazoncognito.com")
        headers = {
            'content-type': "application/x-www-form-urlencoded",
            'cache-control': "no-cache",
            'Authorization': "Basic {}".format(auth_code)
        }
        print("Headers: ", headers)
        connection.request('POST', '/oauth2/token', urlencode(payload), headers)
        return connection.getresponse()

    def get_access_token(self, code, client_id, client_secret, redirect_uri):
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri
        }
        return self.post_to_api(payload)

    @staticmethod
    def get_token(grantee_token):
        resp = jwt.get_unverified_claims(grantee_token)
        return resp['sub']

    def refresh_access_token(self, refresh_token, client_id, client_secret, redirect_uri):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': client_id,
            'client_secret': client_secret,
            'redirect_uri': redirect_uri
        }
        return self.post_to_api(payload)

