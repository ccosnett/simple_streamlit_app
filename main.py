import streamlit as st
from datetime import datetime
from dotenv import load_dotenv
import os
from web3 import Web3
from streamlit_autorefresh import st_autorefresh
from datetime import datetime
from compassapisdk import CompassAPISDK, models
import pandas as pd


load_dotenv()

st.title("Money Generator")

rpc_url = os.environ["ARBITRUM_MAINNET_RPC_URL"]
api_key = os.environ["COMPASS_API_KEY"]
w3 = Web3(Web3.HTTPProvider(rpc_url))

#count = st_autorefresh(interval=2000, limit=None, key="refresh")
block_placeholder = st.empty()
key_placeholder = st.empty()

with CompassAPISDK(
    api_key_auth=api_key,
) as compass_api_sdk:

    interest_rates = compass_api_sdk.aave_v3.rate(chain=models.AaveRateChain.ARBITRUM_MAINNET, token=models.AaveRateToken.USDC)
    position_per_token = compass_api_sdk.aave_v3.user_position_per_token(chain=models.AaveUserPositionPerTokenChain.ARBITRUM_MAINNET, user="0xb8340945eBc917D2Aa0368a5e4E79C849c461511", token=models.AaveUserPositionPerTokenToken.USDC)


while True:
    #now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    latest_block = w3.eth.get_block("latest").number

    #placeholder.write(f"Current date/time: {now}")
    block_placeholder.write(f"Current block: {latest_block}")
    #key_placeholder.write(f" {res}")
    rates_dict = interest_rates.model_dump(mode="json")
    df = pd.DataFrame([rates_dict])
    st.table(df.round(2))