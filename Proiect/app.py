import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from scipy import stats
from scipy.stats import kurtosis, skew
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler, Normalizer, RobustScaler, \
    QuantileTransformer
import warnings
import pymongo
from datetime import datetime

warnings.filterwarnings('ignore')

st.set_page_config(
    page_title="Proiect - Oprea Vlad",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Welcome page
st.title("Proiect - Oprea Vlad")
st.markdown("---")
st.markdown("""
Accesati pagina cerinta-1 din sidebar pentru a incepe fluxul de analiza a datelor.
""")

