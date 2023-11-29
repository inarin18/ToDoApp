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
    if ( "metadata", "tasklist") not in st.session_state :
        task_dict : dict = restore_dict_from_json(TASK_JSON_PATH)
        
        st.session_state.metadata = task_dict["metadata"]
        st.session_state.tasklist = task_dict["tasklist"]
    

def delete_task_in_json():
    pass
    
    
def update_task_json():
    
    # JSONファイルを更新するためにセッション変数をまず辞書に格納
    task_dict = {
        "metadata" : st.session_state.metadata,
        "tasklist" : st.session_state.tasklist
    }
    
    # task_dict を保存することにより JSON ファイルを更新
    with open(TASK_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(task_dict, file, indent=2)


# 編集された df をもとにセッション変数内のタスクリストを更新
def update_taskjson_from_edited_df(edited_df):
    
    edited_taskdict = edited_df.transpose().to_dict()
    edited_tasklist = [task for task in edited_taskdict.values()]
    
    st.session_state.tasklist = edited_tasklist
    
    update_task_json()


def main():
    
    initialize_session_state_vals()
    
    # タイトル
    st.title("ToDoApp")
    
    # タスクリストの一覧表示
    st.subheader("タスクの一覧と編集", divider="rainbow")
    df = pd.DataFrame(st.session_state.tasklist)
    edited_df = st.data_editor(
        df,
        column_order=("name", "discription", "deadline", "_index"),
        column_config={
            "name" : st.column_config.Column(
                "タスク名",
                width="medium"
            ),
            "discription" : st.column_config.Column(
                "タスクの説明",
                width="medium"
            ),
            "deadline" : st.column_config.Column(
                "締め切り",
                width="medium"
            ),
            "_index" : st.column_config.CheckboxColumn(
                "選択",
                width="small",
                disabled=False,
                default=False,
            ) 
        },
    )
    
    # 見栄えのためにボタンを配置する列を作成
    col_delete, col_empty, col_edit = st.columns(3)
    
    with col_delete :
        is_deleted = st.button("選択したタスクを削除")
    with col_edit: 
        is_edited = st.button("編集確定")
        
    # 選択したタスクを削除した場合は JSON ファイルを更新
    if is_deleted :
        delete_task_in_json()
        st.warning("削除完了しました.")
        
    # 編集された場合は JSON ファイルを更新
    if is_edited:
        update_taskjson_from_edited_df(edited_df)
        st.info("編集完了しました.")
    
    # ----------------------------------------------------------------------------
    
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
                "deadline"    : f"{pd.to_datetime(deadline)}",
            }
            
            # セッション変数中のタスクリストの最後尾にタスクを追加
            st.session_state.tasklist.append(task_body)
            
            update_task_json()
            
            st.info("タスクがToDoリストに追加されました.")    


if __name__ == "__main__" :
    main()