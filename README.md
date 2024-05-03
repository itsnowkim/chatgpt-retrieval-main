# chatgpt-retrieval

## Installation

Install [Langchain](https://github.com/hwchase17/langchain) and other required packages.

```
# 환경 세팅
conda create -n gpt python=3.11
conda activate gpt

# 패키지 설치
pip install openai chromadb tiktoken unstructured
pip install "unstructured[pdf]" 

# 맥 os 일 때 brew 로 설치, window 는 알아서 찾아보셈
brew install poppler

# gpu 없어서 cpu 로 설치함
pip install faiss-cpu
```

```
# 이거 말고도 패키지 없다고 뜰 때마다 에러 보고 설치했는데 기억 안남. 추가로 생기면 pr 해주셈
pip install --upgrade --quiet  langchain langchain-community langchainhub langchain-openai langchain-chroma bs4
```

## Example usage

기본적으로 `rag_local.py` 를 사용.
나머지는 튜토리얼 공부용이었음.

코드상에서 `./data/` 디렉토리 안에 `.txt` 파일들을 RAG 벡터 db 로 만들어서 retriever 하고 있음.
(해당 디렉토리 안에 채팅 형식으로 `.txt` 파일 추가하면 해당 메시지를 retriever 한다는 뜻. 반대로, 디렉토리에서 제외시키면 모델이 해당 정보를 포함시키지 않음.)

"Me" 의 페르소나는 `./data/my_persona.txt` 에 정의되어 있음.
페르소나를 바꾸려면 헤당 파일 정보를 갈아끼우면 됨.

예시 실행 방법
```
> python rag_local.py "B [16:05] - Hey, are you free later tonight at 6pm? There's this new movie out I really want to see!""

```

Test reading `data/cat.pdf` file.
```
> python chatgpt.py "what is my cat's name"
Me [16:15] - Sorry, I already have plans for dinner tonight. Maybe we can catch that movie another time though!
```
