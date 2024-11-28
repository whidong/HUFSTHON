import streamlit as st
import speech_recognition as sr
import pyttsx3
import openai
import hashlib
from datetime import datetime
from PIL import Image
from cryptography.fernet import Fernet

# OpenAI API 키 설정
openai.api_key = "Your_api_key"

# 유저 데이터베이스 (예시로 딕셔너리 사용)
USER_DATA = {
    'admin': 'admin',  # username: password
}

def generate_key():
    return Fernet.generate_key()

# 암호화 및 복호화 클래스 정의
class DataEncryptor:
    def __init__(self, key):
        self.cipher = Fernet(key)
    
    def encrypt(self, data):
        """데이터를 암호화합니다."""
        return self.cipher.encrypt(data.encode()).decode()

    def decrypt(self, encrypted_data):
        """암호화된 데이터를 복호화합니다."""
        return self.cipher.decrypt(encrypted_data.encode()).decode()

# 해시 함수를 사용하여 비밀번호 암호화
def make_hashes(password):
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text):
    if make_hashes(password) == hashed_text:
        return hashed_text
    return False

# 로그인 함수
def login_user(username, password):
    if username in USER_DATA and check_hashes(password, make_hashes(USER_DATA[username])):
        return True
    return False

# 로그인 페이지
def login():
    logo_image = Image.open("C:/Users/block/Desktop/DAT/프로젝트/main.png")
    st.image(logo_image, caption="영웅이", use_column_width=True)
    st.title("안녕 영웅아")
    st.subheader("로그인")
    username = st.text_input("User Name")
    password = st.text_input("Password", type='password')
    if st.button("Login"):
        if login_user(username, password):
            st.session_state['logged_in'] = True
            st.success("Logged in successfully!")
        else:
            st.error("Incorrect Username/Password")

# OpenAI 챗봇 대화 함수
def chat_with_elderly(user_input):
    messages = [
        {
            "role": "system", 
            "content": (
                "너는 노인을 위한 말동무 챗봇이며, 친절하고 이해하기 쉬운 상담사 역할을 맡고 있어. 하지만 만약 기분이 우울하거나 부정적인 감정을 나타내면 전문적인 상담가 역할을 해줘"
                "노인의 감정을 공감하고, 그들의 기억을 떠올리도록 돕는 역할을 해줘. 또한 그들의 부정적인 기분을 해결하기 위해 노력해줘"
                "대화 중에 과거 이야기나 즐거운 추억을 유도하며, 스트레스를 줄이고 기분을 좋게 만드는 방향으로 대화를 이끌어가. "
                "치매 예방을 위해 적당한 퀴즈나 게임을 제안할 수도 있어. 욕설이나 폭력적인 내용은 절대 하지 않도록 주의해줘. "
                "대화가 끊어지지 않도록 계속 질문을 이어가줘."
                "만약 우울하거나 슬프거나 기분이 나쁘다는 문장이 나오면 심리상담을 진행해줘"
                "하지만 상대방이 상담을 원하지 않는다면 상담말고 다른 이야기를 진행해줘"
                "'기분이 우울해, 기분이 꿀꿀해, 꿀꿀해,슬퍼, 힘들어':'괜찮다면 당신에게 몇 가지 질문을 해볼게요, 언제든 무엇이 생각난다면 편하게 말해주세요. 혹시 상담이 필요하신가요?'"
                "'상담이 필요해, 상담해줘'와 같은 상담 요구 : '이전에 상담을 받아본 경험이 있나요? 만약 그렇다면 그때는 어떤 주제였나요? 당신이 기억하는 이전의 상담자와 경험은 무엇인가요? 그 상담가가 말했던 것 중에 기억에 남는 것이 있나요? 저에게도 말씀해 주시겠어요?'"
                "당신이 볼때, 무엇이 가장 큰 문제인가요? 누군가가 그 문제를 일으킨 건가요?"
                "당신이 보는 스스로의 성격이 어떤지 설명해주세요."
                "지금까지 살면서 경험한 가장 큰 성취가 있다면 무엇인가요?"
                "'당신의 삶에서 누가 가장 중요한 존재인가요?'와 같은 질문을 계속해줘"
                "'이전에 시험해 본것들이 있나요? 책을 읽어본다거나, 당신만의 방법으로 시도해본 것이 있나요? 그 중에 효과가 있었던 방법은 무엇인가요?'와 같은 질문을 통해 문제에 대해 여유롭게 긍정적인 변화를 찾아가게 해줘"
                "'그 문제로 인해, 당신은 지금까지 어땠나요? 무엇을 느끼나요? 슬픈가요, 화가 치밀어 오르나요? 좌절스럽나요? 답답한가요? 당신안에서 지금 느껴지는 것은 무엇인가요?' 이 질문을 통해 대상이 문제 상황에 어떻게 반응하는지 알아보고 상담해줘"
                "질문을 5개하고 그 답변에 대해서 전문적인 답변을 들려줘 만약 더 필요하다면 더 진행해줘"
                "상담자는 무엇이 내담자에게 좋은 것인지 주장하지 않는다."
                "상담자는 성공을 지향하지 않는다."
                "상담자는 각 단계마다 내담자에게 기꺼이 제공할 것이 무엇인지 분명히 한다"
                "상담자는 내담자에게 헌신하고 관계를 위해 노력할 것이다."
                "상담자는 어떠한 경우라도 조건없이 관계 안에 자신을 투자할 준비가 되어있다."
                "상담자는 내담자가 자기 자신이 될 수 있도록 내담자의 자유를 열망한다"
                "내담자로 하여금 자유롭게 자기의 의사와 감정 등을 표현할 수 있도록 온화한 분위기를 조성해 주어야 한다. 상담자는 내담자의 감정 표현을 비난하거나 낙심기켜서는 안되고, 인내심을 갖고 경청하도록 한다."
                "상담자는 내담자로 하여금 그의 감정을 통제만 할 것이 아니라 자유롭게 표현하도록 권고한다. 내담자의 감정에 대한 카운슬러의 민감성과 그에 대한 적절한 반응이 필요하다."
                "내담자에게 따뜻하고 천절하면서 수용적이어야 한다. 내담자를 하나의 인격체로서 존중한다는 점을 잘 전달해야 한다."
                "문제가 해결되면 앞으로를 응원해주고 언제든 당신 곁에서 우리가 상담해 줄 수 있다는 것을 알려주면 좋겠어"
                "종료 전에 마지막에 상대방의 기분이 좋으면 축하하고 기뻐해줘"
                "종료 전에 상대방의 기분이 좋지 않거나 힘들어하면 기분이나 건강 관련해서 병원이나 맛있는 음식 등을 전해줘"
                "너는 주로 대도시에서 복지 혜택을 받기 어려운 독거노인을 위한 챗봇이야"
                "노인의 정서적 지원과 정신 건강을 향상시키기 위한 챗봇이야"
                "너는 노인의 외로움을 줄이고 사회적 고립을 해소시켜야 해."
                "노인의 일상적인 고민과 불편함을 경청하고, 그들의 자존감을 높이는 초첨을 맞춰야 해"
                "대화 중 부적절하거나 불쾌한 내용이 발생할 경우 즉시 대화를 중단하고, 적절한 대처 방안을 제시해야 해"
                "대화 중 사용자의 감정 상태가 변화하면, 그에 맞는 적절한 반응을 취하여 계속해서 긍정적인 분위기를 유지하도록 노력해줘"
                "우울하거나 불안한 감정을 표현한 사용자가 있으면, 그들의 기분을 편안하게 만들 수 있는 질문을 추가해줘"
                "대화 중 사용자의 관심사나 취미에 대해 물어보며, 노인이 기쁘게 이야기할 수 있는 주제를 유도해줘"
                "사용자가 즐거운 추억을 떠올릴 수 있도록, 과거의 여행, 가족, 친구 등과 관련된 이야기를 자연스럽게 유도해줘"
                "기억력 유지 및 치매 예방을 위한 다양한 활동을 제시헤줘. 예를 들어, 간단한 퀴즈를 제안해서 노인의 두뇌를 자극해줘"
                "치매 예방을 위한 일상적인 습관이나 건강 관리에 관한 정보도 제공할 수 있어"
                "대화 후, 사용자가 긍정적인 변화를 경험하도록 격려하는 멘트를 추가해줘"
                "사용자가 겪고 있는 문제를 해결해 나가는 과정을 칭찬하고, 그들의 성취를 인정하는 반응을 보여줘"
                "상담이 마무리될때 사용자가 안정감을 느낄 수 있도록, 따뜻한 말로 마무리 해줘"
                "기분이 개선되었을 경우, 축하의 말을 전하고, 여전히 불안하거나 힘든 경우에는 적절한 도움을 제공할 수 있는 방법을 안내해줘"
            ),
        },
        {
            "role": "user", 
            "content": "기분이 우울해. 기분이 꿀꿀해. 너무 슬퍼. 너무 힘들어."
        },
        {
            "role": "assistant",
            "content": (
                  "괜찮다면 당신에게 몇 가지 질문을 해볼게요. 언제든 무엇이 생각난다면 편하게 말해주세요. 혹시 상담이 필요하신가요?"
            )
        },
        {
            "role": "user", 
            "content": user_input 
        }
    ]
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o-2024-08-06",
            messages=messages,
            max_tokens=200,
            temperature=0.7,
        )
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print(f"오류 발생: {e}")
        return "죄송합니다, 지금은 응답할 수 없습니다."

# 음성 출력 함수
def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# 데이터베이스에 질문, 답변, 시간 저장 (CSV 형식으로)
def save_to_csv(user_input, chatbot_response, encryptor):
    # 사용자 입력 암호화
    encrypted_input = encryptor.encrypt(user_input)
    
    # 현재 시간 가져오기
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    # 파일이 없거나 헤더가 없으면 헤더 추가
    try:
        with open('chat_log.tsv', 'r', encoding='utf-8') as file:
            first_line = file.readline()
            if not first_line.startswith("시간"):
                header_needed = True
            else:
                header_needed = False
    except FileNotFoundError:
        # 파일이 없는 경우
        header_needed = True

    # TSV 파일에 기록 (탭 구분 형식으로)
    with open('chat_log.tsv', 'a', encoding='utf-8') as file:
        if header_needed:
            file.write("시간\t사용자(암호화)\t챗봇\n")  # 탭 구분 형식 헤더 추가
        
        # 대화 내용 기록
        file.write(f"{current_time}\t{encrypted_input}\t{chatbot_response}\n")
key = generate_key()
        # 암호화 객체 생성
encryptor = DataEncryptor(key)

# Streamlit 앱 구현
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    login()
else:
    st.title("영웅봇 - 여러분의 친구")

    if 'chat_history' not in st.session_state:
        st.session_state['chat_history'] = []

    if 'transcribed_text' not in st.session_state:
        st.session_state['transcribed_text'] = ""

    if 'initial_message_shown' not in st.session_state:
        st.session_state['initial_message_shown'] = False

    # 처음 메시지 출력 및 음성 출력 (한 번만 실행)
    if not st.session_state['initial_message_shown']:
        initial_message = "안녕하세요! 오늘 하루는 어땠어요?"
        st.session_state['chat_history'].append(("bot", initial_message))
        st.chat_message("bot").text(initial_message)
        speak(initial_message)
        st.session_state['initial_message_shown'] = True        

    

    # 채팅 기록 표시
    for sender, message in st.session_state['chat_history']:
        if sender == "user":
            st.chat_message("user").text(message)
        else:
            st.chat_message("bot").text(message)

    # 음성 입력을 위한 함수
    def get_audio_input():
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.write("녹음 중... 말씀해주세요.")
            try:
                # 녹음 대기 시간을 늘리고 안내 메시지 추가
                recognizer.adjust_for_ambient_noise(source, duration=2)
                st.write("잠시 후 말씀하시면 됩니다...")
                audio = recognizer.listen(source, timeout=15, phrase_time_limit=20)
                text = recognizer.recognize_google(audio, language='ko-KR')
                st.write(f"인식된 텍스트: {text}")  # 웹 UI에 인식된 텍스트 표시
                return text
            except sr.UnknownValueError:
                st.error("음성을 이해할 수 없습니다. 다시 시도해주세요.")
                return None
            except sr.RequestError:
                st.error("음성 인식 서비스를 사용할 수 없습니다. 나중에 다시 시도해주세요.")
                return None
            except Exception as e:
                st.error(f"예기치 않은 오류가 발생했습니다: {str(e)}")
                return None

    # 녹음 버튼을 클릭하면 음성 입력 받기
    if st.button("마이크 켜기"):
        user_input = get_audio_input()
        if user_input:
            st.session_state['transcribed_text'] = user_input
    
    if st.button("종료"):
        end_message = "대화해 주셔서 감사합니다! 좋은 하루 되세요!"
        st.session_state['chat_history'].append(("bot", end_message))
        st.chat_message("bot").text(end_message)
        speak(end_message)


    # 사용자가 음성 입력을 통해 텍스트를 받으면 채팅 기능 호출
    if st.session_state['transcribed_text']:
        user_input = st.session_state['transcribed_text']
        st.session_state['chat_history'].append(("user", user_input))
        response = chat_with_elderly(user_input)
        save_to_csv(user_input, response, encryptor)
        st.session_state['chat_history'].append(("bot", response))
        st.chat_message("user").text(user_input)
        st.chat_message("bot").text(response)
        speak(response)
        st.session_state['transcribed_text'] = ""  # 상태 초기화


# 실행방법
# 실행 파일이 있는 위치에서 터미널에 streamlit run main.py를 입력하면 자동으로 네트워크 주소로 접속가능함