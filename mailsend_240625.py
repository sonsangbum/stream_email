# streamlit run 240625_mailsend.py

import streamlit as st
import smtplib
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase #첨부된 파일을 바이너리로 변환시켜주는 개체
from email import encoders

def Mail_send() :

    def form_callback():
        from_subject =st.session_state.m_subject
        from_id =st.session_state.m_id   
        from_content =st.session_state.m_content
        from_file=st.session_state.m_file
    
        #메일 제목/받는 사람/보내는 사람 정보
        my_mail= from_id #'sonsangbum@gmail.com'
        pwd='ccqg etmw drgf aorq'
        to_mail='sonsangbum@gmail.com'

        msg=MIMEMultipart()
        msg['Subject']=from_subject #이메일 제목
        msg['Form']= my_mail
        msg['To'] =  to_mail
        text = MIMEText(from_content)
        msg.attach(text)

        #업로드된 파일을 로컬에 저장함
        if from_file is not None :
            with open(from_file.name,"wb") as file:  #"wb" write 바이너리 ## 파일이름으로 자료를 갖고 오기 위해 '.name'을 붙임
                file.write(from_file.getbuffer())  #buffer에 있는 파일을 내 PC에 저장함

        #메일 첨부(PC에 저장된 파일을 메일에 첨부해서 보냄)
            with open(from_file.name,'rb') as f :   #mail에 첨부할때는 읽기로만 가능
                file_data = MIMEBase('application','octect-strem') #바이너리 객체변환
                file_data.set_payload(f.read())                    #f파일을 읽어서, file_data에 불어옴
                encoders.encode_base64(file_data)
                file_data.add_header('Content-Disposition','attachment',filename=from_file.name)  #첨부할 파일이 header에 s넣음
                msg.attach(file_data)

        #이메일 전송 -
        smtp=smtplib.SMTP("smtp.gmail.com",587)
        smtp.starttls() #보안설정
        smtp.login(user=to_mail,password=pwd)
        smtp.sendmail(my_mail,to_mail,msg.as_string())
        smtp.close()
        st.header("이메일이 전송되었습니다.")
   
    ##메일보내기 메인
    with st.form(key='form'):  #다른 사람이 부르면, 내용이 모두 초기화됨, streamlit 안에서는 한몸으로 움직이도록 만듦
        #메일 폼 작성(구글메일)
        from_subject = st.text_input("메일 제목",key='m_subject')  #초기화는 되나, key 안에 기억됨. 이 key를 불러오는게 session
    
        st.write(st.session_state.m_subject)               #.write 는 파이썬의 Print와 같은 기능
        from_id = st.text_input("보내는 사람 eMAIL",key='m_id')
        from_content = st.text_area('본문 내용',height=5,key='m_content')
        from_file = st.file_uploader('첨부파일',type=['csv','txt','xls','xlsx'],key='m_file')
        # # clicked= st.button("메일 보내기")
        submit = st.form_submit_button('메일 보내기',on_click=form_callback)
        # st.write(st.session_state.m_subject)   

        # if submit:    #form_callback을 한거라, 본인(submit)이 아닌, 타인(session)이 부른것이 되서 현재는 submit는 필요없음.
        #     #메일 제목/받는 사람/보내는 사람 정보
        #     my_mail= from_id #'sonsangbum@gmail.com'
        #     pwd='ccqg etmw drgf aorq'
        #     to_mail='sonsangbum@gmail.com'

        #     msg=MIMEMultipart()
        #     msg['Subject']=from_subject #이메일 제목
        #     msg['Form']= my_mail
        #     msg['To'] =  to_mail
        #     text = MIMEText(from_content)
        #     msg.attach(text)

        #     #업로드된 파일을 로컬에 저장함
        #     if from_file is not None :
        #         with open(from_file.name,"wb") as file:  #"wb" write 바이너리 ## 파일이름으로 자료를 갖고 오기 위해 '.name'을 붙임
        #             file.write(from_file.getbuffer())  #buffer에 있는 파일을 내 PC에 저장함

        #     #메일 첨부(PC에 저장된 파일을 메일에 첨부해서 보냄)
        #         with open(from_file.name,'rb') as f :   #mail에 첨부할때는 읽기로만 가능
        #             file_data = MIMEBase('application','octect-strem') #바이너리 객체변환
        #             file_data.set_payload(f.read())                    #f파일을 읽어서, file_data에 불어옴
        #             encoders.encode_base64(file_data)
        #             file_data.add_header('Content-Disposition','attachment',filename=from_file.name)  #첨부할 파일이 header에 s넣음
        #             msg.attach(file_data)

        #     #이메일 전송 -
        #     smtp=smtplib.SMTP("smtp.gmail.com",587)
        #     smtp.starttls() #보안설정
        #     smtp.login(user=to_mail,password=pwd)
        #     smtp.sendmail(my_mail,to_mail,msg.as_string())

        #     st.write("이메일이 전송되었습니다.")

if __name__ == "__main__ ":
    Mail_send()
