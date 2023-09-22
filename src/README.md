CafaTechNetApp4
Uses Evolved 5G SDK 1.0.13

The CAPIF and NEF Emulator must be started prior to the current Network App.
Starting the container starts automatically Flask server (using api.py) at port 5555:

Endpoints:
- “/” web page shows that "CAFA Tech Network App is working"
- “/subscribe_ue” 
	Takes subscription request with parameters from the vApp and creates
	QoS and Connection monitor subscription to NEF using environmental 
	variables (through emulator_utils.py).
- “/unsubscribe”
	Deletes subscriptions with the ID of this NetApp
- “/nefcallbacks”
	- receives notifications from the NEF
	- separates them into QoS and Connection monitor messages
		and extracts the corresponding states from the JSON
	- forwards the extracted states to the vApp endpoints “/qos_state”
		and “/conn_state” respectively
