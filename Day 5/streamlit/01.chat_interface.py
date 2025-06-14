import streamlit as st
import openai

# Azure OpenAI 설정
AZURE_OPENAI_ENDPOINT = "<YOUR_AZURE_OPENAI_ENDPOINT>"  # 예: "https://your-resource-name.openai.azure.com/"
AZURE_OPENAI_API_KEY = "<YOUR_AZURE_OPENAI_API_KEY>"  # Azure OpenAI API 키
DEPLOYMENT_NAME = "<YOUR_DEPLOYMENT_NAME>"  # Azure OpenAI에서 배포한 모델 이름

# OpenAI 라이브러리 초기화
openai.api_type = "azure"
openai.azure_endpoint = AZURE_OPENAI_ENDPOINT
openai.api_version = "2024-12-01-preview"
openai.api_key = AZURE_OPENAI_API_KEY

def get_openai_response(messages):
    """
    Azure OpenAI API를 호출하여 응답을 가져오는 함수
    """
    try:
        response = openai.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=messages,
            max_tokens=100,
            temperature=0.7
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# Streamlit 앱
st.title("Azure OpenAI Chat Interface")
st.write("Azure OpenAI 모델과 대화하세요!")

# 채팅 기록 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []

# 채팅 기록 표시
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])

# 사용자 입력 처리
if user_input := st.chat_input("메시지를 입력하세요"):
    # 사용자 메시지 저장 및 표시
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    # 모델 응답 생성 및 저장
    with st.spinner("응답을 기다리는 중..."):
        assistant_response = get_openai_response(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": assistant_response})
    st.chat_message("assistant").write(assistant_response)