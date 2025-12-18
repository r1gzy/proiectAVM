import streamlit as st
import pandas as pd
import numpy as np

st.title("Cerinta 1")

if 'df' not in st.session_state:
    st.session_state['df'] = None

st.header('1. Incarcare fisier')
uploaded_file = st.file_uploader('Incarca un fisier csv sau excel', type=['csv', 'xlsx', 'xls'])

#incarcare fisier
if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        
        #validare citire corecta a fisierului
        if df.empty:
            st.error('Fisierul este gol')
        elif df.shape[0] == 0:
            st.error('Fisierul nu contine date')
        else:
            st.session_state['df'] = df
            #mesaj de confirmare
            st.success('Fisierul a fost incarcat cu succes')

    except Exception as e:
        st.error(f'Eroare la incarcarea fisierului: {str(e)}')
        st.session_state['df'] = None
    
if 'df' in st.session_state and st.session_state['df'] is not None:
    df = st.session_state['df']
    
    #afisare primele 10 randuri
    st.header('2. Primele 10 randuri')
    st.dataframe(df.head(10), use_container_width=True)

    #filtrare date
    st.header('3. Filtrare date')
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(exclude=[np.number]).columns.tolist()

    #numar randuri inainte de filtrare
    rows_before = len(df)

    filtered_df = df.copy()

    #filtrare coloane numerice cu slidere
    if numeric_cols:
        st.subheader('Filtrare coloane numerice')
        for col in numeric_cols:
            min_val = float(df[col].min())
            max_val = float(df[col].max())

            selected_range = st.slider(
                f'Interval pentru {col}',
                min_value=min_val,
                max_value=max_val,
                value=(min_val, max_val)
            )

            filtered_df = filtered_df[(filtered_df[col] >= selected_range[0]) & (filtered_df[col] <= selected_range[1])]
    
    #filtrare coloane categorice
    if cat_cols:
        st.subheader('Filtrare coloane categorice')
        for col in cat_cols:
            unique_values = df[col].dropna().unique().tolist()

            selected_values = st.multiselect(
                f'Selecteaza valori pentru {col}',
                options=unique_values,
                default=unique_values
            )

            if selected_values:
                filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
            else:
                filtered_df = filtered_df[filtered_df[col].isin([])]

    #afisare rezultate
    st.header('4. Rezultate filtrare')
    rows_after = len(filtered_df)
    
    #numar randuri inainte si dupa filtrare
    col1, col2 = st.columns(2)
    with col1:
        st.metric('Numar randuri inainte de filtrare: ', rows_before)
    with col2:
        st.metric('Numar randuri dupa filtrare: ', rows_after, delta=rows_after - rows_before)

    #afisare dataframe filtrat
    st.write('5. Dataframe filtrat:')
    st.dataframe(filtered_df, use_container_width=True)

else:
    st.info('Incarca un fisier csv sau excel pentru a continua')    