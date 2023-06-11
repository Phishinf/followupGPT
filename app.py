# from lxml import etree
import json
from google.oauth2.credentials import Credentials

# Import all the logic functions from logic.py
import logic

sampleBody = json.dumps(
{
  'access_token': 'ya29.a0AWY7CklDdBdYtPfTL8Qs7GqHbaa4sHMnVeT6iGM-TBvxw1KAA1OZ_t_0vREHF6GemtYFZkjaF-7Gyeu6XTUy2niPt6LhQfWrRkDIay_K3J53O9RPej4RQ8wClCdrQS6ysHz6f-q4jLieYdbXLnmN98HadaexaCgYKAU0SARASFQG1tDrpubse_XgXFto5hdqC0AjsIw0163',
  'refresh_token': '1//06MEqYl6_TOpGCgYIARAAGAYSNwF-L9IrQcNnL1avOX6xAO-z3OzGriyw3gi5PLYR7_D5nGHlPXUso3RiemAKaM5UHQPK9hCaNzQ',
  'scope': 'https://www.googleapis.com/auth/gmail.send https://www.googleapis.com/auth/gmail.readonly',
  'token_type': 'Bearer',
  'expiry_date': 1686475494517
})

sampleEvent = {'body': sampleBody}


def lambda_handler(event, context):
    print('Lambda function invoked')
    # Parse the request body
    request_body = json.loads(event['body'])

    try:
        # Get the access token from the request
        accessToken = request_body['access_token']
        if accessToken is None:
            raise CustomError(400, 'NoCredentials', 'No access token provided')
        creds = Credentials(token=accessToken)

        # Get the user's email address
        email_address = logic.get_user_email(creds)

        email_fetch_json = logic.not_replied_emails(creds)

        openai_json = logic.generate_reply(email_fetch_json)

        email_list = logic.send_email_to_all(creds, openai_json, email_address)

        res_body = {'email_sent': email_list}
        print(email_list)
        # Return the request body in the response
        response = {
            "statusCode": 200,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": json.dumps(res_body),
            "isBase64Encoded": False
        }
        print(response)
        return response
    except Exception as e:
        response = {
            "statusCode": e.statusCode,
            "headers": {
                "Content-Type": "application/json"
            },
            "body": e.code + ": " + e.message,
            "isBase64Encoded": False
        }
        print(response)
        return response


class CustomError(Exception):
    def __init__(self, status_code, code, message):
        self.status_code = status_code
        self.code = code
        self.message = message


if __name__ == "__main__":
    lambda_handler(sampleEvent, None)
