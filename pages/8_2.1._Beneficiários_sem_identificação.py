import streamlit as st
from st_files_connection import FilesConnection

import pandas as pd

from functions.bene_sem_id import bene_sem_id_func

from PIL import Image
import xlsxwriter
from io import BytesIO

st.set_page_config(
     page_title="Auditoria Beta",
     page_icon="🏗️",
 )

# st.cache_resource.clear()

conn = st.experimental_connection('s3', type=FilesConnection)

@st.cache_data(ttl=3600, show_spinner="1/4 - Carregando base completa...") #Ler base com a classificação TUSS da ANS
def get_data_1():
    return conn.read("df-for-mvps/6/290/mai-2024/df_append_all.csv", input_format="csv")
#     return pd.read_csv("../dados/df_append_all.csv")

df_append_all = get_data_1()

# @st.cache_data(ttl=3600, show_spinner="2/4 - Carregando histórico...") #Ler base com a classificação TUSS da ANS
# def get_data_2():
#     return conn.read("df-for-mvps/6/290/mai-2024/df_append.csv", input_format="csv")
# #     return pd.read_csv('../dados/df_append.csv')
    
# df_append = get_data_2()

# df_append = df_append_all.dropna()

# df_append.loc[:, "valor_pago"] = df_append["valor_pago"].map('{:.2f}'.format)
df_append_all.loc[:, "valor_pago"] = df_append_all["valor_pago"].map('{:.2f}'.format)

df_append_all['operadora'] = df_append_all['operadora'].astype(str)

# st.write(df_append_all["valor_pago"].sum())


st.markdown("# Beneficiários sem identificação")
st.sidebar.markdown("# Beneficiários sem identificação")
st.markdown('Beneficiários sem identificação representam sinistros que não estão atrelados a um beneficiário, ou seja uma conta ou gasto sem o registro de qualquer usuário.')

filter_date = st.sidebar.selectbox(label='Selecione o período', options=['2024', '2023'])

if filter_date == 'Mar/2023':
    min_date = '2023-03-01'
    max_date = '2023-03-31'
elif filter_date == 'Fev/2023':
    min_date = '2023-02-01'
    max_date = '2023-02-31'
elif filter_date == 'Jan/2023':
    min_date = '2023-01-01'
    max_date = '2023-01-31'
elif filter_date == 'Dez/2022':
    min_date = '2022-12-01'
    max_date = '2022-12-31'
elif filter_date == 'Nov/2022':
    min_date = '2022-1-01'
    max_date = '2022-11-31'
elif filter_date == 'Out/2022':
    min_date = '2022-10-01'
    max_date = '2022-10-31'
elif filter_date == 'Set/2022':
    min_date = '2022-09-01'
    max_date = '2022-09-31'
elif filter_date == 'Ago/2022':
    min_date = '2022-08-01'
    max_date = '2022-08-31'
elif filter_date == 'Jul/2022':
    min_date = '2022-07-01'
    max_date = '2022-07-31'
elif filter_date == 'Jun/2022':
    min_date = '2022-06-01'
    max_date = '2022-06-31'
elif filter_date == 'Mai/2022':
    min_date = '2022-05-01'
    max_date = '2022-05-31'
elif filter_date == 'Abr/2022':
    min_date = '2022-04-01'
    max_date = '2022-04-31'
elif filter_date == 'Mar/2022':
    min_date = '2022-03-01'
    max_date = '2022-03-31'
elif filter_date == 'Fev/2022':
    min_date = '2022-02-01'
    max_date = '2022-02-31'
elif filter_date == 'Jan/2022':
    min_date = '2022-01-01'
    max_date = '2022-01-31'
elif filter_date == '2022':
    min_date = '2022-01-01'
    max_date = '2022-12-31'
elif filter_date == '2023':
    min_date = '2023-01-01'
    max_date = '2023-12-31'
else:
    min_date = '2018-12-01'
    max_date = '2022-11-30'

insurance_option = df_append_all['operadora'].unique().tolist()

if len(insurance_option) > 1:
    filter_insurance = st.sidebar.selectbox(label='Selecione a Operadora', options=['Todas', insurance_option[0], insurance_option[1]])
else:
    filter_insurance = st.sidebar.selectbox(label='Selecione a Operadora', options=[insurance_option[0]])

image = conn.open("df-for-mvps/6/img/logo.png", input_format="png")
image = Image.open(image)
st.sidebar.image(image, width=110)

image = conn.open("df-for-mvps/6/290/img/logo.png", input_format="png")
image = Image.open(image)
st.sidebar.image(image, width=50)

st.sidebar.write('\n\n')
st.sidebar.write('\n\n')
st.sidebar.write('\n\n')
st.sidebar.write('\n\n')
st.sidebar.write('\n\n')
st.sidebar.write('\n\n')


# st.sidebar.caption('Construído com 🧠 por Blue AI')

# 1 Beneficiário sem identificação
bene_sem_id = bene_sem_id_func(df_append_all, filter_insurance, min_date, max_date)

total = len(bene_sem_id[(bene_sem_id['id_pessoa'].isnull()) | (bene_sem_id['id_pessoa'] == '') | (bene_sem_id['id_pessoa'] == ' ') | (bene_sem_id['id_pessoa'] == '0') | (bene_sem_id['id_pessoa'] == 0) & (bene_sem_id['dt_utilizacao'] <= max_date) & (bene_sem_id['dt_utilizacao'] >= min_date)])

if total == 1:
    # st.error('**Atenção.** \n\n A Blue encontrou alguma(s) suspeita(s) de fraude com os gastos do plano de saúde, para o período selecionado. Confira abaixo quais são as suspeitas.', icon="🚨")
    st.write('###### Foi encontrado', total, 'beneficiário apenas sem identificação.')
    # st.write('###### 1. Beneficiários sem identificação:', total)
    bene_sem_id = bene_sem_id.rename(columns={"id_pessoa": "ID do usuário", "sexo": "Sexo", "provedor": "Provedor", "cod_tuss": "TUSS", "proc_operadora": "Descrição", "dt_utilizacao": "Data", "valor_pago": "Valor pago"})
    bene_sem_id = bene_sem_id[(bene_sem_id['ID do usuário'].isnull()) | (bene_sem_id['ID do usuário'] == '') | (bene_sem_id['ID do usuário'] == ' ') | (bene_sem_id['ID do usuário'] == '0') | (bene_sem_id['ID do usuário'] == 0) & (bene_sem_id['Data'] <= max_date) & (bene_sem_id['Data'] >= min_date)]
    bene_sem_id
    
#     @st.experimental_memo
#     def convert_df(bene_sem_id):
#         return bene_sem_id.to_csv(index=False).encode('utf-8')


#     csv = convert_df(bene_sem_id)

#     st.download_button(
#         "Baixar planilha",
#         csv,
#         "codigos_sem_identificacao.csv",
#         "text/csv",
#         key='download-csv'
#     )

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        bene_sem_id.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.close()
        processed_data = output.getvalue()
        return processed_data
    df_xlsx = to_excel(bene_sem_id)
    st.download_button(label='📥 Baixar Planilha',
                                    data=df_xlsx ,
                                    file_name= 'codigos_sem_identificacao.xlsx')
    
elif total > 1:
    # st.error('**Atenção.** \n\n A Blue encontrou alguma(s) suspeita(s) de fraude com os gastos do plano de saúde, para o período selecionado. Confira abaixo quais são as suspeitas.', icon="🚨")
    st.write('###### Foram encontrados', total, 'registros de beneficiários sem identificação.')
    # st.write('###### 1. Beneficiários sem identificação:', total)
    bene_sem_id = bene_sem_id.rename(columns={"id_pessoa": "ID do usuário", "sexo": "Sexo", "provedor": "Provedor", "cod_tuss": "TUSS", "proc_operadora": "Descrição", "dt_utilizacao": "Data", "valor_pago": "Valor pago"})
    bene_sem_id = bene_sem_id[(bene_sem_id['ID do usuário'].isnull()) | (bene_sem_id['ID do usuário'] == '') | (bene_sem_id['ID do usuário'] == ' ') | (bene_sem_id['ID do usuário'] == '0') | (bene_sem_id['ID do usuário'] == 0) & (bene_sem_id['Data'] <= max_date) & (bene_sem_id['Data'] >= min_date)]
    bene_sem_id
    
#     @st.experimental_memo
#     def convert_df(bene_sem_id):
#         return bene_sem_id.to_csv(index=False).encode('utf-8')


#     csv = convert_df(bene_sem_id)

#     st.download_button(
#         "Baixar planilha",
#         csv,
#         "codigos_sem_identificacao.csv",
#         "text/csv",
#         key='download-csv'
#     )

    def to_excel(df):
        output = BytesIO()
        writer = pd.ExcelWriter(output, engine='xlsxwriter')
        bene_sem_id.to_excel(writer, index=False, sheet_name='Sheet1')
        workbook = writer.book
        worksheet = writer.sheets['Sheet1']
        format1 = workbook.add_format({'num_format': '0.00'}) 
        worksheet.set_column('A:A', None, format1)  
        writer.close()
        processed_data = output.getvalue()
        return processed_data
    df_xlsx = to_excel(bene_sem_id)
    st.download_button(label='📥 Baixar Planilha',
                                    data=df_xlsx ,
                                    file_name= 'codigos_sem_identificacao.xlsx')
    
else:
    st.info('Nenhum alerta de possível inconsistência foi encontrado para esse período. \n\n**Uma notificação te avisará se algo diferente acontecer.**', icon="🌟")



