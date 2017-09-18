'''
'''

from collections import namedtuple


class Schemas(object):
    '''
    '''

    # XXX need a versioned schema with source tables
    #     partitioned from transaction namespace.
    
    _catalog = { 'AccountPermission': ['AP_CA_ID','AP_ACL', 'AP_TAX_ID',
                                       'AP_F_NAME','AP_L_NAME'],
                 'Address': ['AD_ID','AD_LINE1','AD_LINE2','AD_ZIP',
                             'AD_CTRY'], 
                 'Broker': ['B_ID','B_ST_ID','B_NAME',
                            'B_NUM_TRADES','B_COMM_TOTAL'],
                 'CashTransaction': ['CT_T_ID','CT_DTS','CT_AMT','CT_NAME'],
                 'Charge': ['CH_TT_ID','CH_C_TIER','CH_CHRG'],
                 'CommissionRate': ['CR_C_TIER','CR_TT_ID','CR_EX_ID',
                                    'CR_FROM_QTY','CR_TO_QTY','CR_RATE'],
                 'Company': ['CO_ID','CO_ST_ID','CO_NAME','CO_IN_ID',
                             'CO_SP_RATE','CO_CEO','CO_AD_ID','CO_DESC',
                             'CO_OPEN_DATE'],
                 'CompanyCompetitor':['CP_CO_ID','CP_COMP_CO_ID','CP_IN_ID'],
                 'Customer': ['C_ID','C_TAX_ID','C_ST_ID','C_L_NAME',
                              'C_F_NAME','C_M_NAME','C_GENDER','C_TIER',
                              'C_DOB','C_AD_ID','C_COUNTRY_1','C_AREA_1',
                              'C_LOCAL_1','C_EXT_1','C_COUNTRY_2','C_AREA_2',
                              'C_LOCAL_2','C_EXT_2','C_COUNTRY_3','C_AREA_3',
                              'C_LOCAL_3','C_EXT_3','C_EMAIL_1','C_EMAIL_2'],
                 'CustomerAccount': ['CA_ID','CA_B_ID','CA_C_ID','CA_NAME',
                                     'CA_TAX_ST','CA_BAL'],
                 'CustomerAccount2': ['CA_C_ID','CA_ID','CA_TAX_ID',
                                      'CA_B_ID','CA_NAME','CA_BAL',
                                      'CA_L_NAME','CA_F_NAME','CA_M_NAME'],
                 'CustomerTaxrate': ['CX_TX_ID','CX_C_ID'],
                 'DailyMarket': ['DM_DATE','DM_S_SYMBOL','DM_CLOSE',
                              'DM_HIGH','DM_LOW','DM_VOL'],
                 'Exchange': ['EX_ID','EX_NAME','EX_NUM_SYMBOL','EX_OPEN',
                              'EX_CLOSE','EX_DESC','EX_AD_ID'],
                 'Financial': ['FI_CO_ID','FI_YEAR','FI_QTR',
                               'FI_QTR_START_DATE','FI_REVENUE',
                               'FI_NET_EARN','FI_BASIC_EPS',
                               'FI_DILUT_EPS','FI_MARGIN','FI_INVENTORY',
                               'FI_ASSETS','FI_LIABILITY','FI_OUT_BASIC',
                               'FI_OUT_DILUT'],
                 'Holding': ['H_T_ID','H_CA_ID','H_S_SYMBOL','H_DTS',
                             'H_PRICE','H_QTY'],
                 'HoldingHistory': ['HH_H_T_ID','HH_T_ID',
                                    'HH_BEFORE_QTY','HH_AFTER_QTY'],
                 'HoldingSummary': ['HS_CA_ID','HS_S_SYMBOL','HS_QTY'],
                 'Industry': ['IN_ID','IN_NAME','IN_SC_ID'],
                 'LastTrade': ['LT_S_SYMBOL','LT_DTS','LT_PRICE','LT_OPEN_PRICE',
                               'LT_VOL'],
                 'NewsItem': ['NI_ID','NI_HEADLINE','NI_SUMMARY','NI_ITEM',
                              'NI_DTS','NI_SOURCE','NI_AUTHOR'],
                 'NewsXref': ['NX_NI_ID','NX_CO_ID'],
                 'Security': ['S_SYMBOL','S_ISSUE','S_ST_ID','S_NAME',
                              'S_EX_ID','S_CO_ID','S_NUM_OUT',
                              'S_START_DATE','S_EXCH_DATE','S_PE',
                              'S_52WK_HIGH','S_52WK_HIGH_DATE',
                              'S_52WK_LOW','S_52WK_LOW_DATE',
                              'S_DIVIDEND','S_YIELD'],
                 'Settlement': ['SE_T_ID','SE_CASH_TYPE',
                                'SE_CASH_DUE_DATE','SE_AMT'],
                 'StatusType': ['ST_ID','ST_NAME'],
                 'TaxRate': ['TX_ID','TX_NAME','TX_RATE'],
                 'Trade': ['T_ID','T_DTS','T_ST_ID','T_TT_ID','T_IS_CASH',
                           'T_S_SYMBOL','T_QTY','T_BID_PRICE','T_CA_ID',
                           'T_EXEC_NAME','T_TRADE_PRICE','T_CHRG','T_COMM',
                           'T_TAX','T_LIFO'],
                 'TradeHistory': ['TH_T_ID','TH_DTS','TH_ST_ID'],
                 'TradeRequest': ['TR_T_ID','TR_TT_ID','TR_S_SYMBOL',
                                  'TR_QTY','TR_BID_PRICE','TR_B_ID'],
                 'TradeType': ['TT_ID','TT_NAME','TT_IS_SELL','TT_IS_MRKT'],
                 'WatchList': ['WI_WL_ID','WI_S_SYMBOL'],
                 'Zipcode': ['ZC_CODE','ZC_TOWN','ZC_DIV'],

                 # Transaction Payloads
                 'CustomerValuationRequest': ['C_ID','C_TAX_ID'],
                 'MarketStream': ['PRICE_QUOTE', 'TRADE_QTY', 'SYMBOL'],
    }

    @classmethod
    def catalogKeys(cls):
        '''
        '''
        return list(cls._catalog.keys())

    
    @classmethod
    def createRowFactory(cls, name):
        '''
        '''

        try:
            schema = cls._catalog[name]
            return namedtuple(name, schema)
        except KeyError:
            pass
        
        if name in ['CustomerValuationResponse']:
            return namedtuple(name, cls._customerValuationResponse_schema())

        raise KeyError(name)

    
    @classmethod
    def _customerValuationResponse_schema(cls, maxAcctN=10, maxSecurityN=18):
        '''
        '''
        schema = []
        for n in ['C_ASSET_TOTAL_{}', 'C_CASH_BAL_{}', 'C_ACCT_ID_{}']:
            schema.extend([n.format(i) for i in range(1,maxAcctN+1)])
            
        for n in ['C_SYMBOL_{}_{}',
                  'C_HOLDING_QTY_{}_{}',
                  'C_HOLDING_VAL_{}_{}',
                  'C_LAST_TRADE_{}_{}',
                  'C_HOLDING_PCT_CHG_{}_{}']:
            for acct in range(1, maxAcctN+1):
                for securities in range(1, maxSecurities+1):
                    schema.append(n.format(acct, securities))

        schema.extend(['C_AD_ID', 'C_ACCT_CNT', 'C_DOB'])
        schema.extend(f'C_AREA_{i}' for i in range(1,4))
        schema.extend(f'C_CTRY_{i}' for i in range(1,4))
        schema.extend(f'C_EMAIL_{i}' for i in range(1,3))
        schema.extend(f'C_EXT_{i}' for i in range(1,4))
        schema.extend(['C_F_NAME', 'C_GENDER', 'C_L_NAME'])
        schema.extend(f'C_LOCAL_{i}' for i in range(1,4))
        schema.extend(['C_M_NAME', 'C_TIER'])
        return schema
