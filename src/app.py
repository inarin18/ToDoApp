#############################################
# ToDo App
# author : Hinata Inaoka
##############################################

import streamlit as st
import pandas as pd

import os, json

TASK_JSON_PATH : os.path = '../data/tasklist.json'


# JSONファイルを辞書に復元
def restore_dict_from_json(json_file_path : os.path) -> dict:
    with open(json_file_path, encoding="utf-8") as f:
        return json.load(f)


# セッション変数を初期化
def initialize_session_state_vals():
    
    # JSONからタスクのメタデータとリストを取得してセッション変数に登録
    if ("tasklist", "metadata") not in st.session_state :
        task_dict : dict = restore_dict_from_json(TASK_JSON_PATH)
        
        st.session_state.metadata = task_dict["metadata"]
        st.session_state.tasklist = task_dict["tasklist"]
        

def add_task():
    pass
        


def main():
    
    initialize_session_state_vals()
    
    st.title("ToDoApp")
    
    # タスクリストの一覧表示
    st.subheader("タスクリスト", divider="rainbow")
    
    st.session_state.tasklist
    st.table(st.session_state.tasklist)
    # df = pd.DataFrame(st.session_state.tasklist)
    # st.dataframe(df)
    
    # タスクリストへのタスク追加
    st.subheader("タスクの追加", divider="rainbow")
    with st.form(key="register_form", clear_on_submit=True):
        
        # メタデータをユーザ入力から取得 
        
        # 実内容をユーザ入力から取得
        task_name   = st.text_input("タスク名", placeholder="例）風呂掃除")
        discription = st.text_area("タスクの説明", placeholder="例）お風呂を掃除する")
        deadline    = st.date_input("タスクの期限")
        
        # 追加ボタン
        is_submitted = st.form_submit_button("追加")
        
        # 追加ボタンが押された時の処理
        if is_submitted:

            task_body = {
                "name"        : f"{task_name}",
                "discription" : f"{discription}",
                "deadline"    : f"{deadline}"
            }
            
            # セッション変数中のタスクリストの最後尾にタスクを追加
            st.session_state.tasklist.append(task_body)
            
            # JSONファイルを更新するためにセッション変数をまず辞書に格納
            task_dict = {
                "metadata" : st.session_state.metadata,
                "tasklist" : st.session_state.tasklist
            }
            
            # task_dict を保存することにより JSON ファイルを更新
            with open(TASK_JSON_PATH, "w", encoding="utf-8") as file:
                json.dump(task_dict, file, indent=2)
                
            # st.session_state.is_updated_dict = True
            
            st.info("タスクがToDoリストに追加されました.")
    
    # タスクリストからタスクを削除
    st.subheader("タスクの削除", divider="rainbow")


if __name__ == "__main__" :
    main()