from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi, User
from evolved5g.swagger_client.models import Token
import json
from os import path


def get_capif_and_nef_credentials(key):
    dirname = path.dirname(path.abspath(__file__))
    filename = path.join(dirname, "capif_and_nef_credentials.json")
    with open(filename, "r") as f:
        capif_and_nef_credentials_json = json.load(f)
    return capif_and_nef_credentials_json[key]


def get_token_for_nef_emulator() -> Token:
    username = get_capif_and_nef_credentials("nef_user")
    password = get_capif_and_nef_credentials("nef_pwd")
    # User name and pass matches are set in the .env of the docker of NEF_EMULATOR. See
    # https://github.com/EVOLVED-5G/NEF_emulator
    configuration = swagger_client.Configuration()
    configuration.host = get_url_of_the_nef_emulator()
    api_client = swagger_client.ApiClient(configuration=configuration)
    api_client.select_header_content_type(["application/x-www-form-urlencoded"])
    api = LoginApi(api_client)
    token = api.login_access_token_api_v1_login_access_token_post("", username, password, "", "", "")
    return token


def get_api_client(token) -> swagger_client.ApiClient:
    configuration = swagger_client.Configuration()
    configuration.host = get_url_of_the_nef_emulator()
    configuration.access_token = token.access_token
    api_client = swagger_client.ApiClient(configuration=configuration)
    return api_client


def get_url_of_the_nef_emulator() -> str:
    return f"http://{get_capif_and_nef_credentials('nef_ip_and_port')}"


def get_folder_path_for_certificates_and_capif_api_key()->str:
    """
    This is the folder that was provided when you registered the NetApp to CAPIF.
    It contains the certificates and the api.key needed to communicate with the CAPIF server
    """
    current_dir = path.dirname(path.abspath(__file__))
    capif_dirname = get_capif_and_nef_credentials("capif_cert_path")
    capif_path = path.join(current_dir, capif_dirname)
    return capif_path


def get_capif_host()->str:
    return get_capif_and_nef_credentials("capif_host")


def get_capif_https_port()->int:
    return get_capif_and_nef_credentials("capif_port")


def get_netapp_ip_and_port():
    return get_capif_and_nef_credentials("netapp_ip_and_port")
