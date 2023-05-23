from evolved5g import swagger_client
from evolved5g.swagger_client import LoginApi
from evolved5g.swagger_client.models import Token
from os import path, getenv


def get_token_for_nef_emulator() -> Token:
    username = str(getenv("NEF_USER"))
    password = str(getenv("NEF_PASS"))
    configuration = swagger_client.Configuration()
    configuration.host = get_url_of_the_nef_emulator()
    configuration.verify_ssl = False
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
    return f"{str(getenv('NEF_IP'))}:{str(getenv('NEF_PORT'))}"


def get_folder_path_for_netapp_certificates_and_capif_api_key()->str:
    current_dir = path.dirname(path.abspath(__file__))
    capif_dirname = str(getenv("PATH_TO_CERTS"))
    certs_path = path.join(current_dir, capif_dirname)
    return certs_path


def get_capif_host()->str:
    return str(getenv("CAPIF_HOSTNAME"))


def get_capif_https_port()->int:
    return getenv("CAPIF_PORT_HTTPS")


def get_netapp_ip_and_port():
    return str(getenv("NETAPP_IP"))
