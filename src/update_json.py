#
# json の操作に関する関数を集めたファイル
# 
# usage : from update_json import *
# 


import streamlit as st

import os, json


__ALL__ = [
    "update_task_json", 
    "delete_task_in_json_from_edited_df",
    "update_taskjson_from_edited_df"
]


TASK_JSON_PATH : os.path = '../data/tasklist.json'


# jsonファイルをセッション変数内に保持している情報をもとに更新
def update_task_json():
    
    # JSONファイルを更新するためにセッション変数をまず辞書に格納
    task_dict = {
        "metadata" : st.session_state.metadata,
        "tasklist" : st.session_state.tasklist
    }
    
    # task_dict を保存することにより JSON ファイルを更新
    with open(TASK_JSON_PATH, "w", encoding="utf-8") as file:
        json.dump(task_dict, file, indent=2)


# 編集された df をもとに json ファイルに含まれるタスクを削除
def delete_task_in_json_from_edited_df(edited_df):
    edited_taskdict = edited_df.transpose().to_dict()
    edited_tasklist = [task for task in edited_taskdict.values()]
    
    # チェックボックスの値を加味してタスクを新しいリストへ移す
    new_tasklist = []
    for idx, edited_task in enumerate(edited_tasklist):
        if not edited_task["is_checked"] :
            new_tasklist.append(edited_tasklist[idx])
    
    # 削除が完了したら明示的にチェックボックスの値を False に
    for task in new_tasklist :
        task["is_checked"] = False
    
    # セッション変数を更新
    st.session_state.tasklist = new_tasklist
    
    update_task_json()


# 編集された df をもとにセッション変数内のタスクリストを更新
def update_taskjson_from_edited_df(edited_df):
    
    # df を辞書に変換したのちリストへ変換
    edited_taskdict = edited_df.transpose().to_dict()
    edited_tasklist = [task for task in edited_taskdict.values()]
    
    # セッション変数を更新
    st.session_state.tasklist = edited_tasklist
    
    update_task_json()
    