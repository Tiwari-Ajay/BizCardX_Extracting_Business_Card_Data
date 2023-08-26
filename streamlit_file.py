import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
from PIL import Image
from data_extraction import *
import mysql.connector
####################################################
# Youtube Data Extraction
################################################
def project_decription():
    title_templ = """
        <h3 style="color:blue"><b>Project Description:</b></h3>
        """
    st.markdown(title_templ, unsafe_allow_html=True)
    data = f"""
                    **Project Name**: BizCardX: Extracting Business Card Data with OCR

                    **Domain Name**: Business

                    **Used Technologies** : Python, MYSQL, easyOCR and Streamlit
                    
                    It is a Streamlit application that allows users to extract the information on the Business Card.

                    Focus of the project is to make a Streamlit application that allows users to upload
                    an image of a business card and extract relevant information from it using easyOCR.
                    The extracted information would include the company name, card holder name,
                    designation, mobile number, email address, website URL, area, city, state, and pin
                    code. The extracted information would then be displayed in the application's
                    graphical user interface (GUI).
                    """
    st.write(data)

def main():
    title_templ = """
    <div style="background-color:#000080;padding:8px;">
    <h3 style="color:white;padding:15px;text-align:center">BizCardX: Extracting Business Card Data with OCR</h3></div>
    """
    st.markdown(title_templ, unsafe_allow_html=True)
    with st.sidebar:
        selected = option_menu(
            menu_title="Project Menu",
            options=["About the Project", "Choose Card Image","Extract Information","Save Information","All Recorded Data"],
            default_index=0
        )
    if selected == "About the Project":
        project_decription()
    elif selected == "Choose Card Image":
        # Create a file uploader
        image_file = st.file_uploader("**Choose an image:**", type=["jpg", "png", "jpeg"])

        if image_file is not None:
            st.write("**Your Uploaded Image:**")
            st.write("")
            img = Image.open(image_file)
            path = './image/' + image_file.name
            img.save(path)
            with open('path.txt','w') as f:
                f.write(path)
            st.image(image_file, caption='Uploaded Image.', use_column_width=True)
    elif selected == "Extract Information":
        st.write("")
        st.write("**Extracted Information**")
        st.write("")
        with open('path.txt', 'r') as f:
            path = f.read()
            all_info=main_method(path)
            #save data in file
            temp_info=list(all_info).copy()
            temp_info[3] = list(set(temp_info[3]))[0] if len(list(set(temp_info[3]))) == 1 else list(set(temp_info[3]))
            temp_info[4] = list(set(temp_info[4]))[0] if len(list(set(temp_info[4]))) == 1 else list(set(temp_info[4]))
            temp_info[5] = '.'.join(list(set(temp_info[5]))[0].split(' ')) if len(list(set(temp_info[5]))) == 1 else list(set(temp_info[5]))
            i=0
            for x in temp_info:
                if(isinstance(x,list)):
                    try:
                        str1=','.join(x)
                        temp_info.insert(i,str1)
                        del temp_info[i+1]
                    except:
                        pass
                i += 1
            #st.write(temp_info)
            for i in range(len(temp_info)):
                temp_info[i]=temp_info[i]+'\n'

            with open('path.txt','w') as f:
                f.writelines(temp_info)
            col1,col2=st.columns(2)
            with col1:
                st.write("**Company Name**: ")
                st.write("**Card holder name**: ")
                st.write("**Designation**: ")
                st.write("**Mobile Number**: ")
                st.write("**Email Address**: ")
                st.write("**Website URL**: ")
                st.write("**Area**: ")
                st.write("**City**: ")
                st.write("**State**: ")
                st.write("**Pin Code**: ")
            with col2:
                st.text(all_info[0])
                st.text(all_info[1])
                st.text(all_info[2])
                st.text(list(set(all_info[3]))[0] if len(list(set(all_info[3])))==1 else list(set(all_info[3])))
                st.text(list(set(all_info[4]))[0] if len(list(set(all_info[4])))==1 else list(set(all_info[4])))
                st.text('.'.join(list(set(all_info[5]))[0].split(' ')) if len(list(set(all_info[5])))==1 else list(set(all_info[5])))
                st.text(all_info[6])
                st.text(all_info[7])
                st.text(all_info[8])
                st.text(all_info[9])

    elif selected =="Save Information":
        mydb=mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port='3306',
            database='bizcardx')
        cursor = mydb.cursor()
        with open('path.txt','r') as f:
            info_list=f.readlines()
            for i in range(len(info_list)):
                info_list[i]=info_list[i].rstrip('\n')
            print(info_list)
            query="""insert into candidate_details (company_name,card_holder_name,designation,mobile_number,email_address,website_url,area,city,state,pincode)
             select %s, %s, %s, %s,%s, %s, %s, %s,%s,%s where not exists (select * from candidate_details where email_address = %s)"""
            value=(info_list[0],info_list[1],info_list[2],info_list[3],info_list[4],info_list[5],info_list[6],info_list[7],info_list[8],info_list[9],info_list[4])
            cursor.execute(query,value)
        mydb.commit()
        st.write("**Data Saving Status:**")
        st.write("")
        st.success("Succcessfully, Data Saved in MYSQL")
    else:
        mydb = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            port='3306',
            database='bizcardx')
        cursor = mydb.cursor()
        cursor.execute("select * from candidate_details")
        result=cursor.fetchall()
        company_name=[]
        card_holder_name=[]
        designation=[]
        mobile_number=[]
        email_address=[]
        website_url=[]
        area=[]
        city=[]
        state=[]
        pin_code=[]
        #df=pd.DataFrame()
        for x in result:
            company_name.append(x[0])
            card_holder_name.append(x[1])
            designation.append(x[2])
            mobile_number.append(x[3])
            email_address.append(x[4])
            website_url.append(x[5])
            area.append(x[6])
            city.append(x[7])
            state.append(x[8])
            pin_code.append(x[9])

            df=pd.concat([pd.Series(company_name, name='Company Name'),pd.Series(card_holder_name, name='Card holder name'),
                          pd.Series(designation, name='Designation'),pd.Series(mobile_number, name='Mobile Number'),
                          pd.Series(email_address, name='Email Address'),pd.Series(website_url, name='Website URL'),
                          pd.Series(area, name='Area'),pd.Series(city, name='City'),pd.Series(state, name='State'),
                          pd.Series(pin_code, name='Pin Code')], axis=1)
        st.dataframe(df) #show in streamlit

main()
