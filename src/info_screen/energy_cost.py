# -*- coding: utf-8 -*-

# Western Norway is in region NO5
#


your_key = "231621a1-d821-4e17-b8f6-d4be4b295b51"
from entsoe import EntsoePandasClient
import pandas as pd
import pdb
import datetime as dt
import numpy as np
from forex_python.converter import CurrencyRates

class EnergyCost:
    def __init__(self, ExchangeRateEURNOK) -> None:
        self.client = EntsoePandasClient(api_key=your_key)
        self.ExchangeRateEURNOK = ExchangeRateEURNOK

    def GetCurrentCost(self) -> int:
        start = pd.Timestamp('20220912', tz='Europe/Brussels')
        end = pd.Timestamp('20220913', tz='Europe/Brussels')
    
        self.countrycode = '10Y1001A1001A48H'
        ts = self.client.query_day_ahead_prices(self.countrycode, start=start, end=end)
        price_eur_mwh = ts.to_frame().mean()

        print("Prisen: ", price_eur_mwh)

        price_nok_kwh = (price_eur_mwh[0] * self.ExchangeRateEURNOK) / 1000
        return price_nok_kwh

    #contrycodelist=['10Y1001A1001A63L','10Y1001A1001A63L','10YNO-1--------2','10YNO-2--------T','10YNO-3--------J','10YNO-4--------9','10Y1001A1001A48H','10Y1001A1001A44P','10Y1001A1001A45N'
      #              ,'10Y1001A1001A47J','10YDK-1--------W','10YDK-2--------M','FI','EE','LV','LT','AT','BE','FR','NL']
    # API Parameter liste
    #https://transparency.entsoe.eu/content/static_content/Static%20content/web%20api/Guide.html#_complete_parameter_list
    #10Y1001A1001A48H er NO5
    #contrycodelist=['10Y1001A1001A48H']

    #for n in range(0,len(contrycodelist)):
    #    countrycode=contrycodelist[n]
    #    np.disp(countrycode)

    #    ts = client.query_day_ahead_prices(countrycode, start=start, end=end)
    #    #ts=client.query_imbalance_prices(countrycode, start=start, end=end, psr_type=None)
    #    #ts=client.query_imbalance_prices(countrycode, start=start,end=end, psr_type=None)
    #    if n>0:
    #        del(df_temp)
    #    df_temp=ts.to_frame()
    #    #df_temp.columns = [countrycode]
    #    #pdb.set_trace()
    #    if n==0:
    #        df=df_temp
    #    else:
    #        #pdb.set_trace()
    #        df=pd.merge(df,df_temp,how='outer', left_index=True, right_index=True)

    #    print(df)
    #    print("Snitt: ", df.mean())

    #df.columns = contrycodelist

    ##df.plot(color='red', title = 'Straumpris NO5 (EURO/MWh)')
    ##.save('test')