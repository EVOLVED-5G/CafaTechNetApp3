The NetApp creates quaranteed bit rate subscription for discrete automation.
The eqipment network identifier for NEF Emulator is 10.0.0.1.
The notification_destination="http://172.17.0.2:5555/monitoring/callback" is docker container address running NetApp's Flask server.
The Flask server notifies vApp's Flask server (running on its docker container 172.17.0.3 port 5000) about QoS changes
