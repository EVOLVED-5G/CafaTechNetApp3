The CAPIF and NEF Emulator must be started prior to the current NetApp.
The ./start_flask starts a Flask server at port 5555.
It has four endpoints:
	1) "/" Flask web page shows current NEF and CAPIF credentials from the capif_and_nef_credentials.json:
		a) netapp_ip_and_port
		b) nef_user
		c) nef_pwd
		d) nef_host
		e) capif_cert_path (relative to the NetApp's src folder)
		f) capif_host ("capifcore")
		g) capifhost_ip (the real ip-address behind the capifcore)
		e) capif_port
	The page allows to change these parameters with a press on the button on the page. It adds capifcore to /etc/hosts.
	Also, the lower button on the page allows to register the NetApp to the CAPIF, using username and password.
	
	2) "/subscribe_ue" is used by the vApp for qos awareness and connection monitor subscription.
	It takes 3 parameters as a JSON:
		a) ue_id (UE eqipment network identifier, e.g. 10.0.0.1)
		b) ext_id (UE external identifier, e.g. 10001@domain.com)
		c) vapp_notif_dest (vApp notification destination)
	The function behind this endpoint subscribes the UE to the NEF Emulator (quaranteed bit rate subscription for discrete automation, periodic notification every second + connection monitor subscription with notification when connected and when not connected) and writes the notification destination address to the file vapp_notif_dest.txt where the /nefcallbacks endpoint takes its url for forwarding to the vApp.
	
	3) "/unsubscribe" deletes the subscriptions.
	
	4) "/nefcallbacks" receives the NEF Emulator's QoS notifications and forwards them to the given vApp IP endpoint.