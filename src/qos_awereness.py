from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import QosAwareness
import emulator_utils
from evolved5g.swagger_client import UsageThreshold


netapp_id = "CafaTechNetApp2"
equipment_network_identifier = "10.0.0.1"
host = emulator_utils.get_host_of_the_nef_emulator()
token = emulator_utils.get_token()
qos_awareness = QosAwareness(host, token.access_token)
network_identifier = QosAwareness.NetworkIdentifier.IP_V4_ADDRESS

gigabyte = 1024 * 1024 * 1024
usage_threshold = UsageThreshold(duration= None, # not supported
                                total_volume=10 * gigabyte,  # 10 Gigabytes of total volume
                                downlink_volume=5 * gigabyte,  # 5 Gigabytes for downlink
                                uplink_volume=5 * gigabyte  # 5 Gigabytes for uplink
                                )

notification_destination="http://172.17.0.2:5555/monitoring/callback"

def create_quaranteed_bit_rate_subscription_for_discrete_automation():
    discrete_automation = QosAwareness.GBRQosReference.DISCRETE_AUTOMATION
    uplink = QosAwareness.QosMonitoringParameter.UPLINK
    # Minimum delay of data package during uplink, in milliseconds
    uplink_threshold = 20

    subscription = qos_awareness.create_guaranteed_bit_rate_subscription(
        netapp_id=netapp_id,
        equipment_network_identifier=equipment_network_identifier,
        network_identifier=network_identifier,
        notification_destination=notification_destination,
        gbr_qos_reference=discrete_automation,
        usage_threshold=usage_threshold,
        qos_monitoring_parameter=uplink,
        threshold=uplink_threshold,
        wait_time_between_reports=10
    )

    print("--- PRINTING THE SUBSCRIPTION WE JUST CREATED ---")
    print(subscription)

    # Request information about a subscription
    id = subscription.link.split("/")[-1]
    subscription_info = qos_awareness.get_subscription(netapp_id, id)
    print("--- RETRIEVING INFORMATION ABOUT SUBSCRIPTION " + id + " ---")
    print(subscription_info)


def read_and_delete_all_existing_subscriptions():
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


if __name__ == "__main__":
    read_and_delete_all_existing_subscriptions()
    create_quaranteed_bit_rate_subscription_for_discrete_automation()
