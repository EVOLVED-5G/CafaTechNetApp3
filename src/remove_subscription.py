from evolved5g.swagger_client.rest import ApiException
from evolved5g.sdk import QosAwareness
import emulator_utils


netapp_id = "CafaTechNetApp2"
host = emulator_utils.get_host_of_the_nef_emulator()
token = emulator_utils.get_token()
qos_awareness = QosAwareness(host, token.access_token)


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
