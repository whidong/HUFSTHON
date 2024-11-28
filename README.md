# 🌟 AI 말동무 서비스  
HUFSTHON 4조 B1A4  


## 🧩 프로젝트 소개  
**AI 말동무 서비스**는 독거 노인의 **사회적 고립을 방지**하고, **정서적 지지**와 **사회적 상호작용**을 제공하기 위한 대화형 챗봇 서비스입니다.  

### 🎯 프로젝트 목표  
1. 🤝 독거노인의 외로움과 사회적 고립 문제를 해결하여 정서적 지지와 사회적 상호작용 제공  
2. 🗣️ IT 기술에 익숙하지 않은 노인도 쉽게 사용할 수 있도록 AI 모델을 스피커에 탑재  

### 💡 주요 기능  
- **대화형 챗봇 서비스**  
  - 🗨️ 사용자가 챗봇과 대화를 시도하면, 챗봇은 사용자의 말을 듣고 적절한 답변을 생성  
  - 💬 추가 질문을 유도하여 지속적이고 자연스러운 대화 제공  
- **데이터 암호화 및 상태 모니터링**  
  - 🔒 사용자와 AI 서비스 간의 대화 기록은 암호화되어 저장  
  - 📈 저장된 데이터는 필요 시 복지 기관에 제공하여 사용자 상태를 모니터링  

---

## 🌟 주요 특징  
- **🔐 개인정보 보호**  
  - 서비스 이용 전 **개인정보수집 동의서** 및 **개인정보 제3자 동의서** 작성  
- **💻 접근성 향상**  
  - 사용이 간편한 인터페이스로 IT 기술에 익숙하지 않은 노인도 쉽게 사용 가능  

---

## 프로젝트 구조  
```
├── app/main.py # AI 말동무 서비스 애플리케이션 코드
├── app/main.png # 메인화면 이미
├── README.md # 프로젝트 설명 문서
```


---

## 기술 스택  
- **🛠️ 프로그래밍 언어**: Python  
- **📦 프레임워크**: Streamlit
- **🤖 AI 모델**: GPT 기반 언어 모델 (예: OpenAI API)  
- **💾 데이터베이스**: local tsv파일(chat_log.tsv) (암호화된 대화 기록 저장) 

---

## 설치 및 실행 방법  
1. **환경 설정**  
   - 🐍 Python 3.8 이상 설치  
2. **앱 실행**  
   - Streamlit 서버 실행:  
     ```bash
     streamlit run app/main.py
     ```
3. **웹 브라우저에서 접속**  
   - 🌐 로컬 환경: `http://localhost:8501`  

---

## 📜 라이선스  
MIT License를 기반으로 합니다.

