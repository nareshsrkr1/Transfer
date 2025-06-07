# Create mapping from businessdate to businessdaycount
bdc_map = dict(zip(businessdays['businessdate'], businessdays['businessdaycount']))

# Create two new columns to hold the mapped businessdaycount values
calculatedataframe['exit_bdc'] = calculatedataframe['tradeexitcalanderdate'].map(bdc_map)
calculatedataframe['unwindend_bdc'] = calculatedataframe['unwindendday'].map(bdc_map)

# Apply condition and update 'tradeexitperiod_inmths'
mask = (
    calculatedataframe['unwindstartday'].notna() &
    calculatedataframe['unwindendday'].notna() &
    calculatedataframe['Exit_Strategy'].str.lower().isin(['novation', 'compression']) &
    calculatedataframe['exit_bdc'].notna() &
    calculatedataframe['unwindend_bdc'].notna()
)

# Replace values only where condition is True
calculatedataframe.loc[mask, 'tradeexitperiod_inmths'] = (
    calculatedataframe.loc[mask, 'exit_bdc'].astype(int) -
    calculatedataframe.loc[mask, 'unwindend_bdc'].astype(int)
).astype(str)
