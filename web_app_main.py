import streamlit as st
import sqlite3
import hashlib
from function import web_app_graph

conn = sqlite3.connect('database.db')
c = conn.cursor()

def make_hashes(password) :
    return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password, hashed_text) :
    if make_hashes(password) == hashed_text :
        return hashed_text
    return False

def create_user() :
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')

def add_user(username, password) :
    c.execute('INSERT INTO userstable(username, password) VALUES (?,?)',(username, password))
    conn.commit()

def login_user(username, password) :
    c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username, password))
    data = c.fetchall()
    return data

def fileUpload() :
    st.subheader("ファイル読み込み")
    uploaded_init_file = st.file_uploader("初期設定ファイルアップロード", type='csv')
    if uploaded_init_file is not None:
        # アップロードファイルをメインにデータ表示
        df_init = web_app_graph.readInitFile(uploaded_init_file)
        if st.checkbox("初期設定ファイルの内容を表示") :
            st.table(df_init)
    else :
        st.warning("初期設定ファイルをアップロードしてください")
        st.stop()
    uploaded_data_file = st.file_uploader("データファイルアップロード", type='csv')
    if uploaded_data_file is not None:
        # アップロードファイルをメインにデータ表示
        df_data = web_app_graph.readDataFile(uploaded_data_file)
        if st.checkbox("データファイルの内容を表示") :    
            st.table(df_data)
    else :
        st.warning("データファイルをアップロードしてください")
        st.stop()
    return df_init, df_data

def main() :
    st.title("グラフ作成サイト")

    start_menu = ["ホーム", "サインアップ", "ログイン"]
    choice1 = st.sidebar.radio("スタートメニュー", start_menu)

    if choice1 == "ホーム" :
        st.subheader("ホーム")
    elif choice1 == "ログイン" :
        st.subheader("ログイン")

        username = st.sidebar.text_input("ユーザー名を入力してください")
        password = st.sidebar.text_input("パスワードを入力してください", type='password')

        if st.sidebar.checkbox("ログイン") :
            create_user()
            hashed_pswd = make_hashes(password)

            result = login_user(username, check_hashes(password, hashed_pswd))

            if result :
                st.success("{}さんでログインしました".format(username))
                df_init, df_data = fileUpload()
                set_data_list = web_app_graph.readData(df_init)
                with st.form(key='show_graph_form') :
                    # 基本設定（2軸、系列、線の太さ）
                    st.subheader("基本設定")
                    ax1, ax2, second_axis, fig = web_app_graph.setting(set_data_list)
                    # 詳細設定
                    fig_list_ylabel, fig_number = web_app_graph.drawPlot(df_data, ax1, ax2, second_axis)
                    #軸設定（対数、最小大、目盛り、ラベル）
                    fig_type = web_app_graph.selectFigType(ax1)
                    web_app_graph.graidShow(ax1)
                    web_app_graph.axisSetting(fig_type, ax1, ax2, second_axis)
                    web_app_graph.setLabel(set_data_list, ax1, ax2, second_axis)
                    #凡例設定
                    web_app_graph.selectLegend(set_data_list, fig_number, fig_list_ylabel, ax1, ax2, second_axis)
                    st.subheader("グラフ表示")
                    submit_btn = st.form_submit_button("更新")
                    if submit_btn :
                        st.pyplot(fig)
            else :
                st.warning("ユーザー名かパスワードが間違っています")
        
    elif choice1 == "サインアップ" :
        st.subheader("新しいいアカウントを作成します")
        new_user = st.text_input("ユーザー名を入力してください")
        new_password = st.text_input("パスワードを入力してください", type='password')

        if st.button("サインアップ") :
            create_user()
            add_user(new_user, make_hashes(new_password))
            st.success("アカウントの作成に成功しました")
            st.info("ログインをしてください")

if __name__ == '__main__' :
    main()