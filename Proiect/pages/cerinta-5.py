import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title('Cerinta 5')

if 'df' not in st.session_state or st.session_state['df'] is None:
    st.warning('Fisierul nu a fost incarcat inca')
else:
    df = st.session_state['df']

    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    if len(numeric_cols) < 2:
        st.info('Pentru analiza corelatiilor si outlierilor, sunt necesare cel putin 2 coloane numerice')
    else:
        #matrice de corelatii
        st.header('1. Matrice de Corelatii')
        correlation_matrix = df[numeric_cols].corr()

        #heatmap corelatii
        st.subheader('Heatmap Corelatii')
        fig1, ax1 = plt.subplots(figsize=(12, 10))
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8}, ax=ax1)
        ax1.set_title('Heatmap')
        plt.tight_layout()
        st.pyplot(fig1)

        #selectare doua variabile numerice
        st.header('2. Scatter Plot și Corelație Pearson')
        col1, col2 = st.columns(2)
        with col1:
            var1 = st.selectbox('Selecteaza prima variabila numerica:', options=numeric_cols, key='var1')
        with col2:
            var2 = st.selectbox('Selecteaza a doua variabila numerica:', options=numeric_cols, key='var2')
        
        if var1 and var2 and var1 != var2:
            #calcul coeficient de corelatie Pearson
            pearson_corr = df[var1].corr(df[var2])

            #afisare coeficient de corelatie Pearson
            st.subheader('Coeficient de Corelatie Pearson')
            st.write(f'Coeficient de corelatie Pearson intre {var1} si {var2}: {pearson_corr}')

            #scatter plot
            st.subheader('Scatter Plot')
            fig2, ax2 = plt.subplots(figsize=(10, 6))
            sns.scatterplot(x=df[var1], y=df[var2], ax=ax2)
            ax2.set_xlabel(var1)
            ax2.set_ylabel(var2)
            ax2.set_title(f'Scatter Plot intre {var1} si {var2}')
            ax2.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig2)

        #detecție outlieri - metoda IQR
        st.header('3. Detecție Outlieri (Metoda IQR)')
        outliers_data = []
        for col in numeric_cols:
            q1 = df[col].quantile(0.25)
            q3 = df[col].quantile(0.75)
            iqr = q3 - q1

            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            num_outliers = len(outliers)
            percent_outliers = (num_outliers / len(df)) * 100

            outliers_data.append({
                'Coloana': col,
                'Numar Outlieri': num_outliers,
                'Procent Outlieri': round(percent_outliers, 2),
                'Limita inferioara': round(lower_bound, 2),
                'Limita superioara': round(upper_bound, 2)
            })

        outliers_df = pd.DataFrame(outliers_data)
        outliers_df = outliers_df.sort_values('Numar Outlieri', ascending=False)
        st.dataframe(outliers_df, use_container_width=True)

        #afisare numar si procent outlieri pentru fiecare coloana numerica
        st.header('4. Numar si Procent Outlieri')
        st.dataframe(outliers_df, use_container_width=True)

        #vizualizare outlieri pe grafic
        st.header('5. Vizualizare Outlieri')
        selected_col_outlier = st.selectbox('Selecteaza coloana pentru vizualizare outlieri:', options=numeric_cols, key='outlier_col')

        if selected_col_outlier:
            q1 = df[selected_col_outlier].quantile(0.25)
            q3 = df[selected_col_outlier].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr

            outliers_mask = (df[selected_col_outlier] < lower_bound) | (df[selected_col_outlier] > upper_bound)
            normal_data = df[~outliers_mask][selected_col_outlier]
            outlier_data = df[outliers_mask][selected_col_outlier]

            fig3, ax3 = plt.subplots(figsize=(10, 6))
            ax3.boxplot(df[selected_col_outlier].dropna(), vert=True)
            ax3.axhline(lower_bound, color='red', linestyle='--', linewidth=2, label=f'Limita inferioara: {lower_bound:.2f}')
            ax3.axhline(upper_bound, color='red', linestyle='--', linewidth=2, label=f'Limita superioara: {upper_bound:.2f}')
            ax3.set_ylabel(selected_col_outlier)
            ax3.set_title(f'Box Plot cu Outlieri - {selected_col_outlier}')
            ax3.legend()
            ax3.grid(alpha=0.3)
            plt.tight_layout()
            st.pyplot(fig3)