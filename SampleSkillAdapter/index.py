import json
import os
import urllib.request
from urllib.request import HTTPError


def get_api_url(api_id, aws_region, resource):
    return 'https://{0}.execute-api.{1}.amazonaws.com/prod/{2}'.format(api_id, aws_region, resource)


def handler(request, context):
    try:
        print("LOG skill.index.handler.request:", request)

        # Get the Environment Variables, these are used to dynamically compose the API URI

        # Get the Region
        env_aws_default_region = os.environ.get('AWS_DEFAULT_REGION', None)
        if env_aws_default_region is None:
            print("ERROR skill.index.handler.aws_default_region is None default to us-east-1")
            env_aws_default_region = 'us-east-1'

        # Get the API ID
        env_api_id = os.environ.get('api_id', None)
        if env_api_id is None:
            print("ERROR skill.index.handler.env_api_id is None")
            return '{}'

        # Pass the requested directive to the backend Endpoint API
        url = get_api_url(env_api_id, env_aws_default_region, 'directives')
        data = bytes(json.dumps(request), encoding="utf-8")
        headers = {'Content-Type': 'application/json'}
        req = urllib.request.Request(url, data, headers)
        result = urllib.request.urlopen(req).read().decode("utf-8")
        response = json.loads(result)
        print("LOG skill.index.handler.response:", response)
        return response

    except HTTPError as error:
        print("ERROR skill.index.handler.error:", error)
        return error

    except ValueError as error:
        print("ERROR skill.index.handler.valueError:", error)
        return error
