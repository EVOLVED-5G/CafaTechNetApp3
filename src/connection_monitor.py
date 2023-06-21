from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import ConnectionMonitor
import emulator_utils
import datetime
from os import getenv

netapp_id = str(getenv("NETAPP_ID"))


def get_connection_monitor():
    nef_url = emulator_utils.get_url_of_the_nef_emulator()
    capif_path_for_certs_and_api_key=emulator_utils.get_folder_path_for_netapp_certificates_and_capif_api_key()
    capif_host=emulator_utils.get_capif_host()
    capif_https_port=emulator_utils.get_capif_https_port()
    connection_monitor = ConnectionMonitor(nef_url, capif_path_for_certs_and_api_key, capif_host, capif_https_port)
    return connection_monitor


def create_connection_monitor_subscription(external_id):
    
    expire_time = (datetime.datetime.utcnow() + datetime.timedelta(days=1)).isoformat() + "Z"
    
    connection_monitor = get_connection_monitor()
    
    read_and_delete_all_existing_subscriptions()

    notification_destination = str(getenv("CALLBACK_ADDRESS"))

    subscription_when_not_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=notification_destination,
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_NOT_CONNECTED,
        wait_time_before_sending_notification_in_seconds=1,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    subscription_when_connected = connection_monitor.create_subscription(
        netapp_id=netapp_id,
        external_id=external_id,
        notification_destination=notification_destination,
        monitoring_type= ConnectionMonitor.MonitoringType.INFORM_WHEN_CONNECTED,
        wait_time_before_sending_notification_in_seconds=1,
        maximum_number_of_reports=1000,
        monitor_expire_time=expire_time
    )

    get_subscription_info(connection_monitor, subscription_when_not_connected)
    get_subscription_info(connection_monitor, subscription_when_connected)


def get_subscription_info(connection_monitor, subscription):
    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ---")
    print(subscription)
    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = connection_monitor.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + " ---")
    print(subscription_info)


def read_and_delete_all_existing_subscriptions():
    
    connection_monitor = get_connection_monitor()
    
    print("--- SEARCHING FOR EXISTING SUBSCRIPTIONS TO BE DELETED ---")
    try:
        all_subscriptions = connection_monitor.get_all_subscriptions(netapp_id, 0, 100)
        print(all_subscriptions)

        for subscription in all_subscriptions:
            id = subscription.link.split("/")[-1]
            print("Deleting subscription with id: " + id)
            connection_monitor.delete_subscription(netapp_id, id)
    except ApiException as ex:
        if ex.status == 404:
            print("No active transcriptions found")
        else: #something else happened, re-throw the exception
            raise
