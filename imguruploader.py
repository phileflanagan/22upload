import requests
import base64
# import pprint


def get_pin(id):
    # resp = response type = pin
    # state = non-important in this context
    # url = imgur format for api authorize call, then url formatted with data
    resp = "pin"
    state = "ImageUploader"
    url = r"https://api.imgur.com/oauth2/authorize?client_id={cid}&response_type={resp}&state={app_state}"
    pin_url = url.format(cid=id, resp=resp, app_state=state)

    # instruct user to grab pin from url
    print("browse to the following URL and copy the pin:")
    print(pin_url)

    return pin_url


def exchange_pin_for_tokens(id, secret, pin):
    token_url = r"https://api.imgur.com/oauth2/token/"

    # Post Params
    params = {
        "client_id": id,
        "client_secret": secret,
        "grant_type": "pin",
        "pin": pin
    }

    # r = response from POST
    # j = formatted in JSON
    r = requests.post(token_url, data=params)
    j = r.json()

    # print ("The exchangeCodeForTokens API response:")
    # pprint.pprint(j)

    a_token = j['access_token']
    r_token = j['refresh_token']
    return a_token, r_token


def upload_image_anon(id, image_url):
    upload_url = r"https://api.imgur.com/3/upload"

    headers = {
        "authorization": "Client-ID " + id
    }

    # Possible parameters:
    #   album
    #   type (binary file, base64, or url)
    #   name
    #   title
    #   description
    payload = {
        "image": image_url,
        "type": "base64",
        "title": "Works!"
    }

    r = requests.post(upload_url, data=payload, headers=headers)
    j = r.json()

    # print("The UploadImage API response: ")
    # pprint.pprint(j)

    uploaded_url = j['data']['link']
    print("The uploaded image URL is: {0}".format(uploaded_url))


def upload_image(a_token, image_url):
    upload_url = r"https://api.imgur.com/3/upload"

    headers = {
        "authorization": "Bearer " + a_token
    }

    # Possible parameters:
    #   album
    #   type (binary file, base64, or url)
    #   name
    #   title
    #   description
    payload = {
        "image": image_url,
        "type": "base64",
        "title": "Works!"
    }

    r = requests.post(upload_url, data=payload, headers=headers)
    j = r.json()

    # print("The UploadImage API response: ")
    # pprint.pprint(j)

    uploaded_url = j['data']['link']
    print("The uploaded image URL is: {0}".format(uploaded_url))


#############################################
# # # # # # # MAIN CODE RUNNING # # # # # # #
#############################################
if __name__ == '__main__':
    client_id = '42c05ed32823466'
    client_secret = 'be61acf856ef14b129ff932401f740b0bc0676d7'

    # Step 0: Test Anonymous Upload
    with open("cat.jpeg", "rb") as image_file_anon:
        encoded_string_anon = base64.b64encode(image_file_anon.read())
        upload_image_anon(client_id, encoded_string_anon)

    # Step 1: Have user Get Pin
    get_pin(client_id)
    user_pin = input("Paste in pin from link and hit enter: ")

    # Step 2: Exchange Pin for Tokens
    access_token, refresh_token = exchange_pin_for_tokens(client_id, client_secret, user_pin)

    # Step 3: Upload Image (local image in this case)
    with open("22upload.jpg", "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())
        upload_image(access_token, encoded_string)

