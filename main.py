import streamlit as st
from dotenv import load_dotenv
import os
from web3 import Web3
from streamlit_autorefresh import st_autorefresh
from compassapisdk import CompassAPISDK, models
import pandas as pd
#from decimal import Decimal


load_dotenv()

st.title("Live Monitoring of Aave Position")

rpc_url = os.environ["ARBITRUM_MAINNET_RPC_URL"]
api_key = os.environ["COMPASS_API_KEY"]
w3 = Web3(Web3.HTTPProvider(rpc_url))

# count = st_autorefresh(interval=2000, limit=None, key="refresh")
block_placeholder = st.empty()
key_placeholder = st.empty()

with CompassAPISDK(
    api_key_auth=api_key,
) as compass_api_sdk:
    interest_rates = compass_api_sdk.aave_v3.rate(
        chain=models.AaveRateChain.ARBITRUM_MAINNET, token=models.AaveRateToken.USDC
    )
    position_per_token = compass_api_sdk.aave_v3.user_position_per_token(
        chain=models.AaveUserPositionPerTokenChain.ARBITRUM_MAINNET,
        user="0xb8340945eBc917D2Aa0368a5e4E79C849c461511",
        token=models.AaveUserPositionPerTokenToken.USDC,
    )


# Trigger a re-run every 2 seconds
st_autorefresh(interval=2000, limit=None, key="refresh")

# while True:
# now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
latest_block = w3.eth.get_block("latest").number

# placeholder.write(f"Current date/time: {now}")
# block_placeholder.write(f"Current block: {latest_block}")
# key_placeholder.write(f" {res}")
rates_dict = interest_rates.model_dump(mode="json")
position_dict = position_per_token.model_dump(mode="json")

rates_dict["block"] = latest_block

merged = position_dict | rates_dict
for key in [
    "stable_debt",
    "variable_debt",
    "principal_stable_debt",
    "principal_variable_debt",
    "stable_borrow_rate",
    "borrow_apr_fixed_rate",
    "borrow_apy_fixed_rate",
    "stable_borrow_rate_for_new_loans",
    "variable_borrow_rate",
    "liquidity_rate"
]:
    merged.pop(key, None)

merged['original_token_balance_on_2025-05-18-20:00'] = 1
merged["profit"] =  float(merged["token_balance"])-1

df = pd.DataFrame([merged])
df = df.transpose()
st.dataframe(df, use_container_width=True)
