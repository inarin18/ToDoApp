#############################################
# ToDo App
# author : Hinata Inaoka
##############################################

import streamlit as st
import pandas as pd

from config import initialize_session_state_vals
from update_json import *

import os, json


TASK_JSON_PATH : os.path = '../data/tasklist.json'


def main():
    
    # 初期起動時にセッション変数を初期化
    initialize_session_state_vals()
    
    # タイトル
    st.title(":green[ToDoApp]")
    
    # タスクリストの一覧表示
    st.subheader("タスクの一覧と編集", divider="rainbow")
    
    if st.session_state.tasklist == [] :
        st.error("ToDoリストにタスクが追加されていません.")
    else :
        df = pd.DataFrame(st.session_state.tasklist)
        edited_df = st.data_editor(
            df,
            column_order=("name", "discription", "deadline", "is_checked"),
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
                "is_checked" : st.column_config.CheckboxColumn(
                    "選択",
                    width="small",
                    disabled=False,
                    default=False,
                )
            },
            hide_index=True
        )
        
        # 見栄えのためにボタンを配置する列を作成
        col_delete, col_reload, col_edit = st.columns(3)
        
        with col_delete : 
            # 選択したタスクを削除した場合は JSON ファイルを更新
            if st.button("選択したタスクを削除") :
                delete_task_in_json_from_edited_df(edited_df)
                st.warning("削除完了しました.")
                
        with col_reload:
            # 更新されないときはボタンを押してリロード
            if st.button("ページ更新"):
                pass
                st.info("更新しました")
            
        with col_edit: 
            # 編集された場合は JSON ファイルを更新
            if st.button("編集確定"):
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
        is_checked  = False # チェックボックス記入のために保持
        
        # 追加ボタンが押された時の処理
        if st.form_submit_button("追加"):

            task_body = {
                "name"        : f"{task_name}",
                "discription" : f"{discription}",
                "deadline"    : f"{pd.to_datetime(deadline)}",
                "is_checked"  : is_checked
            }
            
            # セッション変数中のタスクリストの最後尾にタスクを追加
            st.session_state.tasklist.append(task_body)
            
            update_task_json()
            
            st.info("タスクがToDoリストに追加されました.")


if __name__ == "__main__" :
    main()