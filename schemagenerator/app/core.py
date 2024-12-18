import pandas as pd
import logging
from typing import Dict, List, Optional
# from os import path, walk

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

def read_excel(file_path: str) -> pd.DataFrame:
    return pd.read_excel(file_path)

def describe_data(df: pd.DataFrame):
    # Display details
    # analysis = schema

    #  Perform analysis on the schema (Might need to make this a data frame)
    # description = {
    #     'num_fields': len(schema),
    #     'data_types': list(set(type(value).__name__ for value in schema.values())),
    #     # Add more analysis as needed
    # }
    description = {}
    return description

def generate_schema(df: pd.DataFrame, column_mapping: Optional[Dict[str, str]] = None) -> List[Dict[str, str]]:
    records = []
    desc = df.describe(include='all')
    info = desc.to_dict()
    columns = df.columns
    # column_list = columns.to_dict()
    logger.warning('Running generate_schema for schema of %s \n', df)
    column_list = df.columns.to_list()
    # Check the data types for each column
    data_types = [str(df[col].dtype) for col in df.columns]
    logger.warning('Columns are %s \n', column_list)
    shcema_info = {
        'columns': column_list,
        'data_types': data_types
    }

    for _, row in df.iterrows():
        record = {}
        for col in columns:
            field_name = column_mapping.get(col, col) if column_mapping else col
            record[field_name] = str(row[col]) if pd.notna(row[col]) else ""
        records.append(record)

    data = {
        'schema':shcema_info,
        'records':records,
        'info':info
    }
    
    return data

def process_excel_to_schema(file: str, column_mapping: Optional[Dict[str, str]] = None) -> str:
    # Check the file extension from the filename attribute
    if hasattr(file, 'filename'):
        filename = file.filename
    else:
        logger.error('File object does not have a filename attribute.')
        raise ValueError("Invalid file object.")
    
    logger.warning('Running process_excel_to_schema for  %s', filename)
    if filename.endswith('.csv'):
        df = pd.read_csv(file)
    elif filename.endswith(('.xlsx','.xls')):
        df = read_excel(file)
    else:
        logger.error('Unsupported file type: %s', filename)
        raise ValueError("Unsupported file type. Please upload a .csv or .xlsx/.xls file.")
    data = generate_schema(df, column_mapping)
    logger.warning('\n Schema generation returned')
    return data

def sample_tables():
    tables = ["accounttype", "ach_distribution", "acknowledgement", "address_type", "affiliation", "affpro", "altaddress", "apcheck", "apheader", "apheaderhis", "aplines", "aplineshis", "appay", "appayheader", "apphistlineitem", "apphistory", "application", "applineitem", "apppref", "aptran", "aptranhis", "apwork", "asset_strategy", "asset_target", "association", "atscode", "broker", "bulletinproducts", "bulletinreadstatus", "bulletinstatus", "bulletintext", "catalog", "checkrecon", "classaccounts", "classificationcode", "cntctype", "codemap", "codexrf", "committee", "condition", "contact", "controlfile", "country", "county", "currency", "customrptlayout", "dailyvalues", "dashboardcontrol", "dashboarddata", "dc_team", "dc_teamfundxrf", "dc_teamprofreptypexrf", "dc_teamprofxrf", "deductibilitycode", "division", "donor", "donor_fund", "donorclass", "donorhistory", "donorsoftcred", "dyna_menu", "effect", "encrypteddata", "encryptionkey", "ethnic", "event", "eventtype", "expenseclass", "externalmap", "f_account_balance", "f_pool_balance", "feature", "fee", "fii", "fii_map", "fii_process_cycle", "fii_values", "file_map", "fm_application", "fm_fund", "fm_gift", "fm_pledge", "fm_profile", "follow_up", "forecast", "foundation", "foundationcode", "freq_used_descr", "fund", "fund_distributions", "fund_fees", "fund_note", "fund_rep", "fund_schol", "fund_stmnt", "fund1099rtaxpct", "fundclass", "funddetailhistory", "fundgl", "fundsummaryhistory", "fundtype", "gift", "gift_note", "giftdist", "giftdistbi", "giftdisthis", "gifthistory", "giftsoftcredits", "gifttype", "gl_value", "glchart", "glcolumn", "glcontrol", "gljournal", "glmaps", "glrecur", "glrow", "glsegment", "glwork", "grant_letter", "grant_note", "grantee", "granteestatus", "granteesummaryhistory", "granteetype", "grantlineitem", "grants", "helpfile", "helpfims", "historicstrategy", "igamcondition", "igammyaccount", "igampref", "integrationrun", "integrationstats", "interest", "interfund", "investacct", "journalkey", "keydescriptions", "keynum", "keyuser", "keyvalues", "labels", "mapconnection", "maptemplate", "match", "menu", "nameprefix", "notepad", "npascii", "occupation", "onlinegifts", "osdoclinks", "osdocs", "p2smismatch", "pastpass", "permission", "pledge", "pledge_installhis", "pledge_installment", "pledgehistory", "pltran", "pltrangift", "policy", "pool", "pop_age", "pop_disability", "pop_economic", "pop_gender", "population", "position", "position_fund", "position_price", "position_transaction", "printer", "Pro2SQL", "proalias", "profile", "profilegroup", "program", "project", "promise", "protitle", "purpose", "qrymstr", "rankcode", "recontran", "region", "relationship", "rep_type", "reportselect", "reportsortsel", "req_type", "risk", "roomcode", "rptitem", "rptlayout", "rptlayoutdata", "rptselect", "rptsetup", "scentral_coding_values", "scentral_suggestions", "scentral_tables", "schformfund", "schformula", "schol_pref", "schqualifications", "schusercode", "schyear", "securities", "securitytype", "sf_sync", "softcredtypecode", "solicitor", "source", "special_handling", "staffer", "state", "statuscode", "stmnt_style", "strategy", "student", "stuqual", "subtype", "success_rank", "syncredo", "syncredofield", "syscontrol", "sysdiagrams", "system_user_", "terms", "test", "transaction_type", "translation", "uds_assoc", "uds_field", "uds_file", "uds_layout", "uds_screen", "upgrade_rec_count", "usercode", "userini", "usrfrml", "usrgrp", "usrgrp_actxrf", "usrgrp_divisionxrf", "usrgrp_usrxrf", "usrqdet", "usrqry", "vendorclass", "voidreason", "watchlist", "workrow", "zipmaster"]
    return tables
