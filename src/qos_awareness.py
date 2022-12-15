from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import QosAwareness
import emulator_utils
from evolved5g.swagger_client import UsageThreshold
from os import getenv

netapp_id = "CAFA-NetApp-3"


def get_qos_awareness():
    nef_url = emulator_utils.get_url_of_the_nef_emulator()
    token = emulator_utils.get_token_for_nef_emulator()
    capif_path_for_certs_and_api_key = emulator_utils.get_folder_path_for_certificates_and_capif_api_key()
    capif_host = emulator_utils.get_capif_host()
    capif_https_port = emulator_utils.get_capif_https_port()
    qos_awareness = QosAwareness(nef_url, token.access_token, capif_path_for_certs_and_api_key, capif_host, capif_https_port)
    return qos_awareness


def create_quaranteed_bit_rate_subscription_for_discrete_automation(equipment_id):
    
    qos_awareness = get_qos_awareness()
    
    read_and_delete_all_existing_subscriptions()

    network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS

    notification_destination = str(getenv("callback_address"))

    discrete_automation = QosAwareness.GBRQosReference.DISCRETE_AUTOMATION
    
    gigabyte = 1024 * 1024 * 1024
    usage_threshold = UsageThreshold(duration= None, # not supported
                                    total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                    downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                    uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                    )
    
    uplink = QosAwareness.QosMonitoringParameter.UPLINK
    # Minimum delay of data package during uplink, in milliseconds
    uplink_threshold = 20

    # reporting_mode = QosAwareness.EventTriggeredReportingConfiguration(1)
    reporting_mode = QosAwareness.PeriodicReportConfiguration(1)

    subscription = qos_awareness.create_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_id,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        gbr_qos_reference=discrete_automation,
        usage_threshold=usage_threshold,
        qos_monitoring_parameter=uplink,
        threshold=uplink_threshold,
        reporting_mode=reporting_mode
    )

    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ---")
    print(subscription)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awareness.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + " ---")
    print(subscription_info)


def read_and_delete_all_existing_subscriptions():
    
    qos_awareness = get_qos_awareness()
    
    print("--- SEARCHING FOR EXISTING SUBSCRIPTIONS TO BE DELETED ---")
    try:
        all_subscriptions = qos_awareness.get_all_subscriptions(netapp_id)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            qos_awareness.delete_subscription(netapp_id, id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active subscriptions found")
        else: #something else happened, re-throw the exception
            raise
