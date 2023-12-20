# 필요한 패키지 설치는 서버 환경 설정에서 수행
# !pip install konlpy
# !pip install mysql-connector-python
# !pip install mecab-python3

# 필요한 라이브러리 임포트
import mysql.connector
import pandas as pd
from konlpy.tag import Mecab
from collections import defaultdict
import math
import numpy as np
import csv
from eunjeon import Mecab # konlpy.tag 설치 오류로 eunjeon 사용함.



# 데이터베이스 접속 정보 설정
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Dlatkfkd0525',
    'database': 'teamf4'
}

def classify_new_recipe():
    # Mecab 형태소 분석기 초기화
    mecab = Mecab()

    process_verbs = defaultdict(lambda: defaultdict(int))
    total_verbs = defaultdict(int)

    # MySQL 데이터베이스에서 기존 데이터 로드 및 처리
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM recipe"
        cursor.execute(query)
        recipes_data = pd.DataFrame(cursor.fetchall(), columns=['id', 'title', 'img_url', 'timecost', 'difficulty', 'cookstep', 'author_id', 'created_at', 'img_file', 'updated_at', 'main_ingredients', 'sub_ingredients', 'classification', 'n_main_ingredients', 'n_sub_ingredients'])
        cursor.close()
        conn.close()

        # 기존 데이터에서 동사 추출 및 빈도수 계산
        for index, row in recipes_data.iterrows():
            process = row['classification']
            cookstep = row['cookstep'] # recipe -> cookstep (이유 : 테이블 변경)
            verbs = [word for word, tag in mecab.pos(cookstep) if tag.startswith('VV')]
            for verb in verbs:
                process_verbs[process][verb] += 1
                total_verbs[verb] += 1
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 중 에러 발생: {err}")

    # 전체 레시피 수 및 조건부 확률 및 TF-IDF 계산
    total_recipes = len(recipes_data)
    conditional_probabilities = {}
    tf_idf_scores = defaultdict(lambda: defaultdict(float))
    for process, verbs in process_verbs.items():
        conditional_probabilities[process] = {verb: count / total_verbs[verb] for verb, count in verbs.items()}
        for verb, count in verbs.items():
            tf = count / total_verbs[verb]
            idf = math.log(total_recipes / total_verbs[verb])
            tf_idf_scores[process][verb] = tf * idf

    # 가중평균값 계산 및 상위 100개 동사 리스트 생성 및 저장
    top_verbs_list = []
    id_counter = 1
    for process, verbs in tf_idf_scores.items():
        weighted_averages = {}
        for verb, tf_idf in verbs.items():
            conditional_probability = conditional_probabilities[process].get(verb, 0)
            weighted_avg = (conditional_probability / np.std(list(conditional_probabilities[process].values())) +
                            tf_idf / np.std(list(tf_idf_scores[process].values()))) / (
                            1 / np.std(list(conditional_probabilities[process].values())) + 1 / np.std(list(tf_idf_scores[process].values())))
            weighted_averages[verb] = weighted_avg

        top_100_verbs = sorted(weighted_averages.items(), key=lambda x: x[1], reverse=True)[:100]
        for verb, weighted in top_100_verbs:
            top_verbs_list.append([id_counter, verb, weighted, process])
            id_counter += 1

    # MySQL 데이터베이스에서 최신 레시피 데이터 로드
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        query = "SELECT * FROM recipe ORDER BY id DESC LIMIT 1"
        cursor.execute(query)
        latest_recipe = pd.DataFrame(cursor.fetchall(), columns=['id', 'title', 'img_url', 'timecost', 'difficulty', 'cookstep', 'author_id', 'created_at', 'img_file', 'updated_at', 'main_ingredients', 'sub_ingredients', 'classification', 'n_main_ingredients', 'n_sub_ingredients']).iloc[0]
        cursor.close()
    except mysql.connector.Error as err:
        print(f"데이터베이스 연결 중 에러 발생: {err}")

    # "동사리스트" 불러오기
    verb_list_path = 'C:/Users/LOVE/cook_alone2/static/verblist.csv'
    #verb_list_df = pd.read_csv(verb_list_path, encoding='utf-8')
    verb_list_df = pd.read_csv(verb_list_path, encoding='cp949')


    # 최신 레시피에서 동사 추출 및 조리 분류 포인트 계산
    input_recipe = latest_recipe['cookstep']
    input_verbs = [word for word, tag in mecab.pos(input_recipe) if tag.startswith('VV')]
    input_points = defaultdict(float)
    for verb in input_verbs:
        matched_verbs = verb_list_df[verb_list_df['verb'] == verb]
        for _, verb_row in matched_verbs.iterrows():
            input_points[verb_row['classification']] += verb_row['weighted']

    # 조리 분류 포인트 정렬 및 상위 3개 분류 결정
    top_classifications = sorted(input_points.items(), key=lambda x: x[1], reverse=True)[:3]

    # 최종 분류 결과 (가장 높은 포인트의 분류)를 데이터베이스에 저장
    try:
        if top_classifications:  # 리스트가 비어 있지 않은 경우
            top_classification = top_classifications[0][0]
        else:
            top_classification = None  # 혹은 기본값 또는 적절한 처리

        if top_classification:  # 유효한 분류가 있는 경우에만 데이터베이스 업데이트
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()
            update_query = f"UPDATE recipe SET classification = '{top_classification}' WHERE id = {latest_recipe['id']}"
            cursor.execute(update_query)
            conn.commit()
            cursor.close()
            conn.close()
            print(f"'{top_classification}'")
        else:
            print("유효한 분류 결과가 없습니다.")
    except mysql.connector.Error as err:
        print(f"데이터베이스 업데이트 중 에러 발생: {err}")

    return top_classification
