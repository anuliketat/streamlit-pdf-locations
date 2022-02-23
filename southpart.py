import streamlit as st
import pandas as pd
import os
import re
import PyPDF2
from collections import Counter
import base64
import warnings
from stqdm import stqdm
warnings.filterwarnings("ignore")


pdf_file = st.file_uploader("Choose a .pdf file", type=["pdf"])
def st_display_pdf(file):

    with open(pdfReader, 'rb') as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')
    pdf_display = f'<embed src="data:application/pdf;base64,{base64_pdf}" width="700" height="1000" type="application/pdf">'
    st.markdown(pdf_display, unsafe_allow_html=True)

def get_page_info(file):
    pdfReader = PyPDF2.PdfFileReader(file)
    num_pages = pdfReader.numPages
    st.markdown(f'Total Pages:{num_pages}')
    #my_bar = st.progress(0)
    with st.spinner('Getting the list of locations...'):
        pin_profiles = ['50', '51', '52', '53']
        tel, ap = [], []
        n_locs = 0
        for page in range(num_pages):
            st.markdown(page)
            pageObject = pdfReader.getPage(page) # read page
            page_text = pageObject.extractText() # extract text in page
            page_pins = re.findall(r'-\d{6}', page_text) # match pincode pattern
            n_locs += len(page_pins)
            for code in page_pins:
                pin = code.strip('-')
                # check first two numbers in pin and append to telangana and ap
                if pin[:2] in pin_profiles[0]:
                    tel.append(pin)
                elif pin[:2] in pin_profiles[1:]:
                    ap.append(pin)
        #my_bar.progress(page)
    return tel, ap, n_locs

tel_dic = {'[4]':'adilabad', '[0]':'hyderabad/rangareddy', '[1]':'hyderabad/rangareddy',
            '[5]':'karimnagar', '[7]':'khammam', '[9]':'mahbubnagar',
          '[2]':'medak', '[3]':'nizamabad', '[8]':'nalgonda', '[6]':'warangal'}
ap_dic = {'[515]':'anantapur', '[517]':'chittoor', '[533]':'east godavari', '[522]':'guntur', '[516]':'kadapa',
            '[520]':'krishna', '[521]':'krishna', '[518]':'kurnool', '[523]':'prakasam', '[524]':'nellore', '[532]':'srikakulam',
            '[530]':'visakhapatnam', '[531]':'visakhapatnam', '[534]':'west godavari', '[535]':'vizianagaram'}
for key, val in tel_dic.items():
    tel_dic[key] = val.title()
for key, val in ap_dic.items():
    ap_dic[key] = val.title()

if pdf_file is not None:
    tel, ap, n_locs = get_page_info(pdf_file)
    ap_list, tel_list = [], []
    for pin in ap:
        inp = str([int(''.join(list(pin[:3])))])
        ap_list.append(ap_dic.get(inp))
    for pin in tel:
        inp = str([int(x) for x in list(pin[2])])
        tel_list.append(tel_dic.get(inp))

    tel_count = Counter(tel_list)
    tel_final = dict(tel_count.most_common())
    ap_count = Counter(ap_list)
    ap_final = dict(ap_count.most_common())

    col1, col2 = st.beta_columns(2)
    col1.header('Andhra Pradesh')
    col1.write(len(ap_list))
    col2.header('Telangana')
    col2.write(len(tel_list))
    col1.write(ap_final)
    col2.write(tel_final)



















