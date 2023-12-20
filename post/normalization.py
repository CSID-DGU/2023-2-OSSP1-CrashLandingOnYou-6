# import mysql.connector
# import chardet
# import difflib
# import pandas as pd

# # 레시피 정보를 읽는 함수
# def read_recipe_info(recipe_id):
#     # MySQL 연결 설정
#     conn = mysql.connector.connect(
#         host='localhost',
#         user='root',
#         password='Dlatkfkd0525',
#         database='teamf4'
#     )
#     # 커서 생성
#     cursor = conn.cursor()

#     try:
#         # 레시피 정보를 조회하는 SQL 쿼리 실행
#         query = f"SELECT main_ingredients, sub_ingredients FROM recipe WHERE id = {recipe_id}"
#         cursor.execute(query)
#         # 결과 가져오기
#         result = cursor.fetchone()
#         if result:
#             main_data = result[0]
#             sub_data = result[1]
#             # 컴마로 분리하여 리스트로 저장
#             main_list = main_data.split(',')
#             sub_list = sub_data.split(',')

            
#             # 추가: recipe_id 불러온거 확인
#             print(f"레시피 ID {recipe_id}의 데이터를 성공적으로 불러왔습니다.")

#             # 추가: main_list_sub_list 확인
#             print("Main ingredients list:", main_list)  # 추가된 부분
#             print("Sub ingredients list:", sub_list)  # 추가된 부분
#             return main_list, sub_list
#         else:
#             print(f"레시피 ID {recipe_id}에 해당하는 레코드가 없습니다.")
#             return None, None
#     except mysql.connector.Error as e:
#         print(f"MySQL 오류: {e}")
#     finally:
#         # 연결 종료
#         conn.close()

# # 두 단어의 관계를 분석하는 함수
# def analyze_relationship(word, cell_content):
#     # Convert both inputs to strings
#     a_str = str(word)
#     d_str = str(cell_content)
#     # Condition 1: word's entire set is contained within cell_content
#     is_subset = a_str in d_str
#     return is_subset

# # 메인 함수: 정규화를 수행하고 데이터베이스를 업데이트하는 함수
# def normalize_and_update_data(recipe_id):
#     #i_recipe_id = int(recipe_id)
#     main_data, sub_data = read_recipe_info(recipe_id) 

#     if main_data and sub_data:
#         # difflib을 이용한 유사도 판단 및 결과 저장
#         best_match_main = []  # Main 데이터에 대한 최적 매치를 저장할 리스트
#         best_match_sub = []   # Sub 데이터에 대한 최적 매치를 저장할 리스트

#         # 사전 데이터 로드
#         dictionary_filepath = 'C:/Users/LOVE/cook_alone2/static/최후_식재료 사전_식재료 넘버링.xlsx'  # 파일 경로 변경 필요
#         excel_data = pd.read_excel(dictionary_filepath)
#         specified_columns = ['식품명', '식품명 동의어', '종류', '종류동의어', '품종', '식품명+가공형태',
#                              '식품명 동의어+가공형태', '부위', '부위 동의어', '식품명+부위',
#                              '식품명 동의어+부위', '식품명+부위 동의어', '식품명 동의어+부위 동의어']

#          # Main 데이터에 대한 유사도 비교
#         for word_main in main_data:
#             max_similarity_main_word = 0.0
#             best_match_main_word = None
#             for column in specified_columns:
#                 for j, cell_content in enumerate(excel_data[column]):
#                     similarity_ratio_main = difflib.SequenceMatcher(None, word_main, str(cell_content)).ratio()
#                     if similarity_ratio_main > max_similarity_main_word:
#                         max_similarity_main_word = similarity_ratio_main
#                         best_match_main_word = (
#                             excel_data.at[j, '식품명 번호'],
#                             cell_content,
#                         )
#             if best_match_main_word is not None:
#                 if analyze_relationship(word_main, cell_content) == True:
#                     best_match_main.append(best_match_main_word)

#         # 확인을 위한 로그 출력 (추가)
#         print("Main matches:", best_match_main)


#         # Sub 데이터에 대한 유사도 비교
#         for word_sub in sub_data:
#             max_similarity_sub_word = 0.0
#             best_match_sub_word = None
#             for column in specified_columns:
#                 for j, cell_content_dict in enumerate(excel_data[column]):
#                     similarity_ratio_sub = difflib.SequenceMatcher(None, word_sub, str(cell_content_dict)).ratio()
#                     if similarity_ratio_sub > max_similarity_sub_word:
#                         max_similarity_sub_word = similarity_ratio_sub
#                         best_match_sub_word = (
#                             excel_data.at[j, '식품명 번호'],
#                             cell_content_dict,
#                         )
#             if best_match_sub_word is not None:
#                 if analyze_relationship(word_sub, cell_content_dict) == True:   ##########여기 수정
#                     best_match_main.append(best_match_sub_word)

#         # 확인을 위한 로그 출력
#         print("Sub matches:", best_match_sub)

#         # 데이터베이스에 저장
#         conn = mysql.connector.connect(
#             host='localhost',
#             user='root',
#             password='Dlatkfkd0525',
#             database='teamf4'
#         )
#         cursor = conn.cursor()

#         # 데이터베이스에 저장할 SQL 쿼리 작성
#         update_query = "UPDATE recipe SET n_main_ingredients = %s, n_sub_ingredients = %s WHERE id = %s"
#         n_main_data = str(best_match_main)
#         n_sub_data = str(best_match_sub)
#         data_to_update = (n_main_data, n_sub_data, recipe_id)

#         # 원본 
#         # # 쿼리 실행
#         # cursor.execute(update_query, data_to_update)
#         # # 변경사항 커밋
#         # conn.commit()
#         # # 연결 종료
#         # conn.close()

#         # 예외처리 로깅 남기기
#         try:
#             cursor.execute(update_query, data_to_update)
#             conn.commit()
#             print("Data updated successfully")
#         except Exception as e:
#             print("Error updating data:", e)
#         finally:
#             conn.close()
