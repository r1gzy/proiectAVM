import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Cerinta 4')

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.warning('Fisierul nu a fost incarcat')
else:
    df = st.session_state['df']

    categorical_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()
    if len(categorical_cols) == 0:
        st.info('Nu exista coloane categorice in setul de date incarcat')
    else:
        st.header('1. Selectare Coloana Categorica')
        selected_col = st.selectbox('Alege o coloana categorica', options=categorical_cols)

        if selected_col:
            value_counts = df[selected_col].value_counts()
            value_counts_percent = (df[selected_col].value_counts(normalize=True) * 100).round(2)

            #tabel frecvente
            st.header('2. Tabel Frecvente')
            freq_df = pd.DataFrame({
                'Valoare': value_counts.index,
                'Frecventa Absoluta': value_counts.values,
                'Procent din total valori de pe coloana': value_counts_percent.values
            })
            freq_df = freq_df.sort_values('Frecventa Absoluta', ascending=False)
            st.dataframe(freq_df, use_container_width=True)

            #count plot
            st.header('3. Count Plot')
            fig, ax = plt.subplots(figsize=(10, 6))
            value_counts_sorted = value_counts.sort_values(ascending=False)
            bars = ax.bar(range(len(value_counts_sorted)), value_counts_sorted.values, edgecolor='black', alpha=0.7)
            ax.set_xticks(range(len(value_counts_sorted)))
            ax.set_xticklabels(value_counts_sorted.index, rotation=45, ha='right')
            ax.set_xlabel(selected_col)
            ax.set_ylabel('Frecventa')
            ax.set_title(f'Count Plot pentru {selected_col}')
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)