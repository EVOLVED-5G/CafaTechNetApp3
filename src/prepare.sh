timestamp="`date +%y%m%d%H%M%S`"

curl  --connect-timeout 5 \
    --max-time 10 \
    --retry-delay 0 \
    --retry-max-time 40 \
    --request GET "$CAPIF_HOSTNAME:$CAPIF_PORT_HTTP/ca-root" 2>/dev/null | jq -r '.certificate' -j > ca.crt

jq -r .folder_to_store_certificates=\"/netapp/$PATH_TO_CERTS\" /netapp/capif_registration.json >> tmp.json && mv tmp.json /netapp/capif_registration.json
jq -r .capif_host=\"$CAPIF_HOSTNAME\" /netapp/capif_registration.json >> tmp.json && mv tmp.json /netapp/capif_registration.json
jq -r .capif_http_port=\"$CAPIF_PORT_HTTP\" /netapp/capif_registration.json >> tmp.json && mv tmp.json /netapp/capif_registration.json
jq -r .capif_https_port=\"$CAPIF_PORT_HTTPS\" /netapp/capif_registration.json >> tmp.json && mv tmp.json /netapp/capif_registration.json
jq -r .capif_callback_url=\"$CAPIF_CALLBACK_URL\" /netapp/capif_registration.json >> tmp.json && mv tmp.json /netapp/capif_registration.json
jq -r .capif_netapp_username=\"$NETAPP_NAME"_"$timestamp\" /netapp/capif_registration.json >> tmp.json && mv tmp.json /netapp/capif_registration.json

evolved5g register-and-onboard-to-capif --config_file_full_path="/netapp/capif_registration.json" --environment="production"

tail -f /dev/null
