import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Cerinta 2")

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.warning('Fisierul nu a fost incarcat inca')
else:
    df = st.session_state['df']

    #nr randuri si coloane
    st.header('1. Dimensiuni Dataset')
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Numar randuri:', df.shape[0])
    with col2:
        st.metric('Numar coloane:', df.shape[1])
    
    #tipuri date pt fiecare coloana
    st.header('2. Tipuri de Date')
    dtype_df = pd.DataFrame({
        'Coloana': df.columns,
        'Tip de Date': [str(dtype) for dtype in df.dtypes],
        'Numar valori non-null': df.count().values
    })
    st.dataframe(dtype_df, use_container_width=True)
    
    #coloane cu valori lipsa
    st.header('3. Analizare valori lipsa')

    missing_values = df.isnull().sum()
    missing_percentage = (missing_values / len(df)) * 100
    missing_df = pd.DataFrame({
        'Coloana': df.columns,
        'Valori Lipsa': missing_values.values,
        'Procent': missing_percentage.values.round(2)
    })

    missing_df_filtered = missing_df[missing_df['Valori Lipsa'] > 0].sort_values('Valori Lipsa', ascending=False)
    if len(missing_df_filtered) > 0:
        st.write('Coloane cu valori lipsa:')
        st.dataframe(missing_df_filtered, use_container_width=True)

        #grafic valori lipsa
        st.subheader('Grafic valori lipsa')
        fig, ax = plt.subplots(figsize=(10, 6))
        missing_df_filtered_sorted = missing_df_filtered.sort_values('Procent', ascending=True)

        # Folosim index numeric pentru y și setăm etichetele manual
        y_pos = np.arange(len(missing_df_filtered_sorted))
        y_labels = missing_df_filtered_sorted['Coloana'].tolist()
        x_values = missing_df_filtered_sorted['Procent'].values

        ax.barh(y_pos, x_values)
        ax.set_yticks(y_pos)
        ax.set_yticklabels(y_labels)
        ax.set_xlabel('Procent Valori Lipsa (%)')
        ax.set_ylabel('Coloana')
        ax.set_title('Procentul Valorilor Lipsa pe Coloana')
        ax.grid(axis='x', alpha=0.3)

        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.success('Nu exista valori lipsa in dataset')

    #statistici descriptive pt coloanele numerice
    st.header('4. Analiza statistica coloane numerice')
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) > 0:
        stats_df = pd.DataFrame({
            'Coloana': numeric_cols,
            'Mean': [df[col].mean() for col in numeric_cols],
            'Median': [df[col].median() for col in numeric_cols],
            'Std': [df[col].std() for col in numeric_cols],
            'Min': [df[col].min() for col in numeric_cols],
            'Max': [df[col].max() for col in numeric_cols],
            'Q1': [df[col].quantile(0.25) for col in numeric_cols],
            'Q3': [df[col].quantile(0.75) for col in numeric_cols]
        })
        for col in ['Mean', 'Median', 'Std', 'Min', 'Max', 'Q1', 'Q3']:
            stats_df[col] = stats_df[col].round(2)
        st.dataframe(stats_df, use_container_width=True)
    else:
        st.success('Nu exista coloane numerice in setul de date incarcat')
    