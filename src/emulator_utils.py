from os import path, getenv


def get_url_of_the_nef_emulator() -> str:
    return f"{str(getenv('NEF_IP'))}:{str(getenv('NEF_PORT'))}"


def get_folder_path_for_netapp_certificates_and_capif_api_key()->str:
    file_dir = path.dirname(path.abspath(__file__))
    capif_dirname = str(getenv("PATH_TO_CERTS"))
    certs_path = path.join(file_dir, capif_dirname)
    return certs_path


def get_capif_host()->str:
    return str(getenv("CAPIF_HOSTNAME"))


def get_capif_https_port()->int:
    return getenv("CAPIF_PORT_HTTPS")


def get_netapp_ip_and_port():
    return str(getenv("NETAPP_IP"))
