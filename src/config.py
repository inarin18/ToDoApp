import streamlit as st

import json, os


__ALL__ = ["initialize_session_state_vals"]


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