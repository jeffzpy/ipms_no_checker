#! python3
#!/usr/bin/env python

from configparser import ConfigParser as scp

#Load the Config ini file from your local Company VDI secured personal data persistence Drive
#These Configuration files are stored at "config_files" directory
#Once your OOT Password`s expired, please run "update_your_config_file.bat" in Company shared G: Drive
config = scp()
cfg_file_location = '..\\config_files\\config.ini'
config.read(cfg_file_location)

proxy_ip = config['PROXY_SETTINGS']['PROXY_IP']
proxy_port = config['PROXY_SETTINGS']['PROXY_PORT']
proxy_domain_str = config['PROXY_SETTINGS']['PROXY_DOMAIN_STRING']

lan_user_name = config['LAN_USER']['LAN_USER_NAME']
lan_user_pass= config['LAN_USER']['LAN_USER_PASSWORD']
oot_user_name = config['OOT_USER']['OOT_USER_NAME']
oot_user_pass= config['OOT_USER']['OOT_USER_PASSWORD']
ucll_db_location= config['UCLL_MIGRS_DB']['DB_LOCATION']
order_stage_db_location= config['UCLL_MIGRS_DB']['ORDER_STAGE']
oot_init_url= config['URL_ADDR']['OOT_INIT_URL']
oot_login_url = config['URL_ADDR']['OOT_LOGIN_URL']
oot_search_url = config['URL_ADDR']['OOT_SEARCH_URL']
http_header_host = config['HTTP_REQUEST']['HEADER_HOST']