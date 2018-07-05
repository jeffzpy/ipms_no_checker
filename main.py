__author__ = "Jeff Zhang: Jeff Zhang@Chorus.co.nz"
__copyright__ = "​​Owned and Maintained by Chorus Network Ltd NZ"

import requests as rs
import os
from bs4 import BeautifulSoup as bs
import pyodbc
from datetime import date, timedelta
import re
from ChorusProxiesAuth import generate_proxy_str as gps
import config as cfg
from AccdbProcess import db_connect as dp

vdi_user = cfg.lan_user_name
vdi_pass = cfg.lan_user_pass
wireline_user = cfg.oot_user_name
wireline_pass = cfg.oot_user_pass
oot_init_url = cfg.oot_init_url
oot_login_url = cfg.oot_login_url
oot_search_url = cfg.oot_search_url
http_header_host = cfg.http_header_host
proxies_str = gps(vdi_user, vdi_pass)
oot_lst = []
oot_s = rs.session()


def get_oot_list():
    oot_lst = []
    db_loc = cfg.ucll_db_location
    query = 'SELECT OOT_ID FROM tblProcessedOrders WHERE NOTES = ?;'
    par = 'POTS ORDER WAITER'
    conn = dp(db_loc, '')
    cursor = conn.cursor()
    cursor.execute(query, par)
    try:
        oot_lst = cursor.fetchall()
    except:
        oot_lst.append('NA')
    conn.close()

    return oot_lst


def update_db_record(oot_id, notes):
    db_loc = cfg.ucll_db_location
    query = 'UPDATE tblProcessedOrders SET SCRIPT_NOTES = ? WHERE OOT_ID = ?'
    query2 = 'UPDATE tblProcessedOrders SET NOTES = ? WHERE OOT_ID = ?'
    par = ''
    conn = dp(db_loc, '')
    cursor = conn.cursor()
    cursor.execute(query, notes, oot_id)
    cursor.execute(query2, par, oot_id)
    conn.commit()
    conn.close()


def wireline_login():
    login_pg_r = oot_s.get(cfg.oot_init_url, proxies=proxies_str)
    login_pg_bs = bs(login_pg_r.text, 'lxml')
    viewstate = str(login_pg_bs.find('input', {'id': '__VIEWSTATE'})['value'])
    viewstategenerator = str(login_pg_bs.find('input', {'id': '__VIEWSTATEGENERATOR'})['value'])
    eventvalidation = str(login_pg_bs.find('input', {'id': '__EVENTVALIDATION'})['value'])
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Content-Length': '424',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Host': http_header_host,
               'Origin': oot_init_url,
               'Referer': oot_login_url,
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
    payload = {'__EVENTTARGET': '',
               '__EVENTARGUMENT': '',
               '__VIEWSTATE': viewstate,
               '__VIEWSTATEGENERATOR': viewstategenerator,
               '__EVENTVALIDATION': eventvalidation,
               'LoginNameTextBox': wireline_user,
               'LoginPasswordTextBox': wireline_pass,
               'LoginButton': 'Login'}
    oot_land_pg_r = oot_s.post(oot_login_url, headers=headers, data=payload,
                               verify=False, proxies=proxies_str)
    return oot_land_pg_r


def search_oot_id(oot_id):
    oot_search_pg_r = oot_s.get(oot_search_url, verify=False,
                                proxies=proxies_str)
    oot_search_pg_bs = bs(oot_search_pg_r.text, 'lxml')
    viewstate = str(oot_search_pg_bs.find('input', {'id': '__VIEWSTATE'})['value'])
    viewstategenerator = str(oot_search_pg_bs.find('input', {'id': '__VIEWSTATEGENERATOR'})['value'])
    eventvalidation = str(oot_search_pg_bs.find('input', {'id': '__EVENTVALIDATION'})['value'])
    headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'en-US,en;q=0.8',
               'Cache-Control': 'max-age=0',
               'Connection': 'keep-alive',
               'Content-Length': '20220',
               'Content-Type': 'application/x-www-form-urlencoded',
               'Host': http_header_host,
               'Origin': oot_init_url,
               'Referer': oot_search_url,
               'Upgrade-Insecure-Requests': '1',
               'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; rv:55.0) Gecko/20100101 Firefox/55.0'}
    start_date = ''

    tday_date = date.today()
    substracted_date = tday_date - timedelta(days=30)
    formated_tday_date = tday_date.strftime('%d-%b-%Y')
    formated_substracted_date = substracted_date.strftime('%d-%b-%Y')
    payload = {'__EVENTTARGET': '',
               '__EVENTARGUMENT': '',
               '__LASTFOCUS': '',
               '__VIEWSTATE': viewstate,
               '__VIEWSTATEGENERATOR': viewstategenerator,
               '__EVENTVALIDATION': eventvalidation,
               'Template:RequestTypes': 'All',
               'Template:FormsDropDown': '-1',
               'Template:ProductDropdownlist': '-1',
               'Template:PortingOptionsDropDown': '-1',
               'Template:BulkOrdersDropdownlist': '-1',
               'Template:TruckRollRequiredDropDown': '-1',
               'Template:EscalationDropDown': '0',
               'Template:StatusDropDown': 'ALL ACTIVE Statuses',
               'Template:StartDate': formated_substracted_date,  # start_date,
               'Template:EndDate': formated_tday_date,  # end_date,
               'Template:RequestIDTextBox': oot_id,
               'Template:SearchRequestIDButton': 'Go',
               'Template:AltRefTextBox': '',
               'Template:PhoneNumberTextBox': '',
               'Template:QuickSearchCustomerNameTextBox': '',
               'Template:QuickSearchServiceOrderNumberTextBox': '',
               'Template:QuickSearchSidNumberTextBox': '',
               'Template:QuickSearchAccountNumberTextBox': '',
               'Template:QuickSearchBulkOrderIdTextbox': ''}

    oot_searched_result_r = oot_s.post(oot_search_url,
                                       headers=headers, data=payload, verify=False, proxies=proxies_str)
    oot_searched_result_bs = bs(oot_searched_result_r.text, 'lxml')
    tbl_searched_result_r = oot_searched_result_bs.find('table', {'id': 'Template_DgrQueue'})
    for a in tbl_searched_result_r.find_all('a', href=True):
        if 'index.aspx?pageid=VReq&Ret=Enh&InstanceID=' in a['href']:
            oot_id_link = (a['href'])
            break

    oot_id_details_r = oot_s.get(''.join([oot_init_url, oot_id_link]), verify=False,
                                 proxies=proxies_str)
    return oot_id_details_r


def check_pots_order_past_n9(oot_id_details_read):
    oot_id_details_bs = bs(oot_id_details_read.text, 'lxml')
    tbl_oot_details_comments = oot_id_details_bs.find('table',
                                                      {'id': '_ctl2_DealerSupportCommentAdd1_CommentsLog1_dgrComments'})
    ipms_som = 'na'
    for each_tr in tbl_oot_details_comments.findAll('tr'):
        linktext = each_tr.text
        linktext = linktext.lower()
        if 'vodafone.com' in linktext and 'som' in linktext:
            ipms_som = linktext.split('som', 1)[1]
            ipms_som = re.findall(r'\d+', ipms_som)[0]
            break
    return ipms_som


if __name__ == '__main__':
    oot_lst = []
    result_list = []
    oot_lst = get_oot_list()
    r = wireline_login()
    if not 'New passwords must conform to the following policy:' in r.text:
        for each_oot in oot_lst:
            an_oot = each_oot[0]
            print('oot id:' + str(an_oot))
            oot_details_read = search_oot_id(an_oot)
            ipms_found = check_pots_order_past_n9(oot_details_read)
            # print('test')
            # print('oot#' + str(an_oot) + '; IPMS SOM# ' + str(ipms_found))
            if ipms_found != 'na':
                print('IPMS SOM Infomration Detected in OOT#' + str(an_oot) + '. IPMS SOM No.#' + str(ipms_found))
                update_db_record(an_oot, 'UPDATE IPMS NEEDED_' + str(ipms_found))
    else:
        print('Your Wireline Password has been expired; ' +
                'Please set your new Password in Wireline ' +
              ' Also, please run "update_your_config_file.bat" in the Company shared G: Drive for updating the ' +
              'global configuration file in your secured personal data persistence Drive')