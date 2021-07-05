import numpy as np
from tensorflow.keras.preprocessing.sequence import pad_sequences

# 모델 검증용 문장을 생성하는 함수
def sentence_generation(model, t, max_len, current_word, n): # 모델, 토크나이저, 현재 단어, 반복할 횟수
    init_word = current_word # 처음 들어온 단어도 마지막에 같이 출력하기위해 저장
    sentence = ''
    for _ in range(n): # n번 반복
        encoded = t.texts_to_sequences([current_word])[0] # 현재 단어에 대한 정수 인코딩
        encoded = pad_sequences([encoded], maxlen=max_len-1, padding='pre') # 데이터에 대한 패딩
        #result = model.predict_classes(encoded, verbose=0)
        result = np.argmax(model.predict(encoded), axis=-1)
    # 입력한 X(현재 단어)에 대해서 Y를 예측하고 Y(예측한 단어)를 result에 저장.
        for word, index in t.word_index.items(): 
            if index == result: # 만약 예측한 단어와 인덱스와 동일한 단어가 있다면
                break # 해당 단어가 예측 단어이므로 break
        current_word = current_word + ' ' + word # 현재 단어 + ' ' + 예측 단어를 현재 단어로 변경
        sentence = sentence + ' ' + word # 예측 단어를 문장에 저장
        
    # for문이므로 이 행동을 다시 반복
    sentence = init_word + sentence
    return sentence