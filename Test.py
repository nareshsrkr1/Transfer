# Constants.py

# Static columns that are always required
STATIC_COLUMNS = [
    "BankingTradingFlag",
    "Exit_Strategy",
    "Exit_Phase"
]

# Aggregations for specific columns
AGGREGATIONS = {
    "Current_Position_Netted_MTM_Value_USD": "SUM(CAST(Current_Position_Netted_MTM_Value_USD AS FLOAT)) AS NPV",
    "Notional_USD": "SUM(ISNULL(CAST(Notional_USD AS FLOAT), 0)) AS Notional",
    "Transaction_ID_FACS": "COUNT(Transaction_ID_FACS) AS Trade_count"
}
