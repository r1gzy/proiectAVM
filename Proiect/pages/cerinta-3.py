import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Cerinta 3')

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.warning('Fisierul nu a fost incarcat')
else:
    df = st.session_state['df']
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()

    if len(numeric_cols) == 0:
        st.info('Nu exista coloane numerice in setul de date incarcat')
    else:
        st.header('1. Selectare Coloană Numerica')
        selected_col = st.selectbox('Alege o coloana numerica', options=numeric_cols)

        if selected_col:
            st.header('2. Configurare Histograma')
            #slider pt. bins
            num_bins = st.slider('Numar bins histograma', min_value=10, max_value=100, value=20)

            #calcul statistici
            col1, col2, col3 = st.columns(3)
            with col1:
                col1 = st.metric('Medie: ', df[selected_col].mean())
            with col2:
                col2 = st.metric('Mediana: ', df[selected_col].median())
            with col3:
                col3 = st.metric('Deviatie standard: ', df[selected_col].std())
            
            #histograma
            st.header('3. Histograma')
            fig, ax = plt.subplots(figsize=(10, 6))
            ax.hist(df[selected_col].dropna(), bins=num_bins, edgecolor='black', alpha=0.7)
            ax.axvline(df[selected_col].mean(), color='red', linestyle='--', linewidth=2, label=f'Medie: {df[selected_col].mean():.2f}')
            ax.axvline(df[selected_col].median(), color='green', linestyle='--', linewidth=2, label=f'Mediana: {df[selected_col].median():.2f}')
            ax.set_xlabel(selected_col)
            ax.set_ylabel('Frecventa')
            ax.set_title(f'Histograma pentru {selected_col}')
            ax.legend()
            ax.grid(axis='y', alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig)

            #boxplot
            st.header('4. Box Plot')
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.boxplot(x=df[selected_col].dropna(), ax=ax2)
            ax2.set_xlabel(selected_col)
            ax2.set_ylabel('Valori')
            ax2.set_title(f'Box Plot pentru {selected_col}')
            
            plt.tight_layout()
            st.pyplot(fig2)
        else:
            st.info('Selecteaza o coloana numerica')