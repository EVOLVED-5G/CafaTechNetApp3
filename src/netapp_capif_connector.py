from evolved5g.sdk import CAPIFInvokerConnector
import emulator_utils
from os import getenv


def capif_connector(capif_netapp_username, capif_netapp_password):

    netapp_ip_and_port = emulator_utils.get_netapp_ip_and_port()

    capif_path_for_certs_and_api_key = emulator_utils.get_folder_path_for_certificates_and_capif_api_key()
    capif_host = emulator_utils.get_capif_host()
    capif_https_port = emulator_utils.get_capif_https_port()

    capif_connector = CAPIFInvokerConnector(folder_to_store_certificates=capif_path_for_certs_and_api_key,
                                            capif_host=capif_host,
                                            capif_http_port=str(getenv("capif_port_http")),
                                            capif_https_port=capif_https_port,
                                            capif_netapp_username=capif_netapp_username,
                                            capif_netapp_password=capif_netapp_password,
                                            capif_callback_url=f"{netapp_ip_and_port}/capifcallbacks",
                                            description= "cafatech netapp_description",
                                            csr_common_name="CAFA-NetApp-3",
                                            csr_organizational_unit="CAFA Tech ou",
                                            csr_organization="CAFA Tech",
                                            crs_locality="Tallinn",
                                            csr_state_or_province_name="Tallinn",
                                            csr_country_name="ET",
                                            csr_email_address="test@example.com"
                                            )

    capif_connector.register_and_onboard_netapp()


