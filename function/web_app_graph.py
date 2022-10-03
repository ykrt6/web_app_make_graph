from cProfile import label
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib import font_manager

@st.cache
def readInitFile(init_file) :
    df_init = pd.read_csv(init_file, encoding="shift-jis", header=None)
    return df_init

@st.cache
def readDataFile(data_file) :
    df_data = pd.read_csv(data_file, encoding="shift-jis")
    return df_data

def readData(df_init) :
    font_dirs = ["/fonts"]
    font_files = font_manager.findSystemFonts(fontpaths=font_dirs)
    for font_file in font_files:
        font_manager.fontManager.addfont(font_file)
    
    set_data_list = {}
    data_name_list = ['fontFamilyJa', 'fontFamilyEn', 'fontSize', 'fontLegendSize', 'width', 'height', 'tickFrame', 'tickDirection', 'tickSize']
    data_input_list = []
    dict_font_family_ja = {'HGP教科書体': "/HGRKK.TTC", 'メイリオ': "font/meiryo.ttc", 'MS明朝': "font/msmincho.ttc", 'UDデジタル教科書N-R': "font/UDDigiKyokashoN-R.ttc", '游ゴシックMedium': "font/YuGothiM.ttc"}
    font_family_ja = df_init.loc[0,1]
    data_input_list.append(dict_font_family_ja[font_family_ja])
    font_family_en = df_init.loc[1,1]
    data_input_list.append(font_family_en)
    font_size = float(df_init.loc[2,1])
    data_input_list.append(font_size)
    font_legend_size = float(df_init.loc[3,1])
    data_input_list.append(font_legend_size)
    width = float(df_init.loc[4,1])
    data_input_list.append(width)
    height = float(df_init.loc[5,1])
    data_input_list.append(height)
    tickFrame = float(df_init.loc[6,1])
    data_input_list.append(tickFrame)
    tick_direction = df_init.loc[7,1]
    data_input_list.append(tick_direction)
    tick_size = float(df_init.loc[8,1])
    data_input_list.append(tick_size)
    set_data_list.update(zip(data_name_list, data_input_list))
    st.write(set_data_list['fontFamilyJa'])

    return set_data_list

def inputNumberErr(data) :
    if data == 0.0 :
        st.warning("数値を入力してください")
    else :
        st.write('input: ', data)

def inputTextErr(var, unit) :
    if str(var) ==  "" or str(unit) == "":
        st.warning("文字列を入力してください")
    else :
        st.write(f'var: {var},  unit: {unit}')


def setting(set_data_list) :
    # 一応フォントとフォントサイズの設定(適用されてるかわかんない)
    plt.rcParams["font.family"] = set_data_list["fontFamilyEn"]                    
    plt.rcParams["font.size"] = set_data_list["fontSize"]      

    #第一軸(ax1)と第二軸(ax2)を作ってax1 が左側の第一軸に、ax2 が右側で第二軸
    fig, ax1 = plt.subplots(figsize=(set_data_list["width"], set_data_list["height"]), frameon=False, tight_layout=True)
    
    second_vartical_axis = st.selectbox("第二縦軸の有無", ["n", "y"])
    if second_vartical_axis == "y" :
        second_axis = True
        ax2 = ax1.twinx()
        ax2.tick_params(axis="y",which='major', direction=set_data_list["tickDirection"],length=set_data_list["tickSize"], width=1.5, labelsize=set_data_list["fontSize"])
        ax2.tick_params(axis="y",which='minor', direction=set_data_list["tickDirection"],length=(set_data_list["tickSize"]/2.0), width=1.0, labelsize=set_data_list["fontSize"])
    else :
        second_axis = False
        ax2 = 0

    #軸の太さの調整
    ax1.spines["top"].set_linewidth(set_data_list["tickFrame"])
    ax1.spines["left"].set_linewidth(set_data_list["tickFrame"])
    ax1.spines["bottom"].set_linewidth(set_data_list["tickFrame"])
    ax1.spines["right"].set_linewidth(set_data_list["tickFrame"])

    # 軸の各パラメータの設定
    ax1.tick_params(axis="x",which='major', direction=set_data_list["tickDirection"],length=set_data_list["tickSize"], width=1.5, labelsize=set_data_list["fontSize"])
    ax1.tick_params(axis="x",which='minor', direction=set_data_list["tickDirection"],length=(set_data_list["tickSize"]/2.0), width=1.0, labelsize=set_data_list["fontSize"])
    ax1.tick_params(axis="y",which='major', direction=set_data_list["tickDirection"],length=set_data_list["tickSize"], width=1.5, labelsize=set_data_list["fontSize"])
    ax1.tick_params(axis="y",which='minor', direction=set_data_list["tickDirection"],length=(set_data_list["tickSize"]/2.0), width=1.0, labelsize=set_data_list["fontSize"])

    return ax1, ax2, second_axis, fig

def drawPlot(df, ax1, ax2, second_axis) :
    fig_marker_style = "ドット"
    fig_number = int(st.number_input(label="系列の個数", value=1))
    fig_line_width = st.number_input(label="線の太さ", value=1.0, min_value=0.0, max_value=10.0)
    fig_list_xlabel = []
    fig_list_ylabel = []
    fig_list_line_style = []
    fig_list_color = []
    fig_list_marker = []
    fig_list_marker_size = []
    fig_list_marker_style = []
    fig_dict_line_style = {'直線': "-", '破線': "--", '一点鎖線': "-.", '点線': ":"}
    fig_dict_marker_style = {'ドット': ".", '丸': "o", '三角形': "^", '四角形': "s", '十字': "+", 'バツ': "x", 'ひし形': "d", '五角形': "p"}
    fig_dict_color = {'青': "Blue", '緑': "Green", '赤': "Red", 'オレンジ': "orange", 'シアン': "Cyan", 'マゼンタ': "Magenta", '黄': "Yellow", '黒': "Black", '白': "White"}

    st.subheader("詳細設定")
    for i in range(fig_number) :
        with st.expander(str(i+1) + '個目のグラフ設定'):
            fig_list_xlabel.append(st.selectbox(str(i+1) + " : x軸のラベル", df.columns.values))
            st.write("input: ", fig_list_xlabel[i])
            fig_list_ylabel.append(st.selectbox(str(i+1) + " : y軸のラベル", df.columns.values))
            st.write("input: ", fig_list_ylabel[i])
            fig_list_line_style.append(st.selectbox(str(i+1) + " : 線種", fig_dict_line_style))
            st.write("input: ", fig_list_line_style[i])
            fig_list_color.append(st.selectbox(str(i+1) + " : 色", fig_dict_color))
            st.write("input: ", fig_list_color[i])
            fig_list_marker.append(st.selectbox(str(i+1) + " : マーカーの有無(更新後に追加設定あり)", ["n", "y"]))
            st.write("input: ", fig_list_marker[i])
            if fig_list_marker[i] == "y" :
                fig_list_marker_size.append(st.number_input(str(i+1) + " : マーカサイズ", value=8.0, min_value=0.0, max_value=50.0))
                st.write("input: ", fig_list_marker_size[i])
                fig_list_marker_style.append(st.selectbox(str(i+1) + " : マーカー", fig_dict_marker_style))
                st.write("input: ", fig_list_marker_style[i])
            else :
                fig_list_marker_size.append(0)
                fig_list_marker_style.append(fig_marker_style)
            if second_axis:
                axis2 = st.selectbox(str(i+1) + " : 第二横軸で描画", ["n", "y"])
                st.write('input: ', axis2)
                if axis2 == "y" :
                    ax2.plot(df[fig_list_xlabel[i]].values, df[fig_list_ylabel[i]].values, ls=fig_dict_line_style[fig_list_line_style[i]], lw=fig_line_width, color=fig_dict_color[fig_list_color[i]], marker=fig_dict_marker_style[fig_list_marker_style[i]], markersize=fig_list_marker_size[i], label=fig_list_ylabel[i])
                else :
                    ax1.plot(df[fig_list_xlabel[i]].values, df[fig_list_ylabel[i]].values, ls=fig_dict_line_style[fig_list_line_style[i]], lw=fig_line_width, color=fig_dict_color[fig_list_color[i]], marker=fig_dict_marker_style[fig_list_marker_style[i]], markersize=fig_list_marker_size[i], label=fig_list_ylabel[i])
            else :
                ax1.plot(df[fig_list_xlabel[i]].values, df[fig_list_ylabel[i]].values, ls=fig_dict_line_style[fig_list_line_style[i]], lw=fig_line_width, color=fig_dict_color[fig_list_color[i]], marker=fig_dict_marker_style[fig_list_marker_style[i]], markersize=fig_list_marker_size[i], label=fig_list_ylabel[i])
    return fig_list_ylabel, fig_number

def selectFigType(ax1) :
    fig_type = st.selectbox("対数", ["n", "y"])
    st.write('input: ', fig_type)
    if fig_type == "y":
        ax1.set_xscale('log')
        ax1.minorticks_off()            # 補助目盛消す
        return 1
    return 0

def axisSetting(fig_type, ax1, ax2, second_axis) :
    # カラムを追加する
    if second_axis :
        col1, col2, col3 = st.columns(3)
    else :
        col1, col2 = st.columns(2)
    with col1 :
        st.write("x軸")
        x_max = float(st.number_input("x軸の最大値"))
        st.write('input: ', x_max)
        x_min = float(st.number_input("x軸の最小値"))
        st.write('input: ', x_min)
        if fig_type == 0:
            x_step = float(st.number_input("x軸の刻み幅"))
            # plt.xticks(np.arange(start, stop, step))
            try :
                ax1.set_xticks(np.arange(stop=x_max*10, step=x_step))
            except :
                inputNumberErr(x_step)
    ax1.set_xlim(x_min, x_max)     # 原点ゼロ合わせ
    ax1.get_xaxis().set_tick_params(pad=8)    # 目盛と軸の間隔
    if second_axis:
        with col2 :
            st.write("第1y軸")
            y1_max = float(st.number_input("y1軸の最大値"))
            st.write('input: ', y1_max)
            y1_min = float(st.number_input("y1軸の最小値"))
            st.write('input: ', y1_min)
            y1_step = float(st.number_input("y1軸の刻み幅"))
            try :
                ax1.set_yticks(np.arange(stop=y1_max*10, step=y1_step))
            except :
                inputNumberErr(y1_step)
            ax1.set_ylim(y1_min, y1_max)     # 原点ゼロ合わせ
        with col3 :
            st.write("第2y軸")
            y2_max = float(st.number_input("y2軸の最大値"))
            st.write('input: ', y2_max)
            y2_min = float(st.number_input("y2軸の最小値"))
            st.write('input: ', y2_min)
            y2_step = float(st.number_input("y2軸の刻み幅"))
            try :
                ax2.set_yticks(np.arange(stop=y2_max*10, step=y2_step))
            except :
                inputNumberErr(y2_step)
            ax2.set_ylim(y2_min, y2_max)     # 原点ゼロ合わせ
        ax1.get_yaxis().set_tick_params(pad=8)    # 目盛と軸の間隔
        ax2.get_yaxis().set_tick_params(pad=8)    # 目盛と軸の間隔
    else :
        with col2 :
            st.write("y軸")
            y_max = float(st.number_input("y軸の最大値"))
            st.write('input: ', y_max)
            y_min = float(st.number_input("y軸の最小値"))
            st.write('input: ', y_min)
            y_step = float(st.number_input("y軸の刻み幅"))
            try :
                ax1.set_yticks(np.arange(stop=y_max*10, step=y_step))
            except :
                inputNumberErr(y_step)
            ax1.set_ylim(y_min, y_max)     # 原点ゼロ合わせ
            ax1.get_yaxis().set_tick_params(pad=8)    # 目盛と軸の間隔

# excel
def graidShow(ax1) :
    if st.selectbox("グリッドを表示(更新後に追加設定あり)", ["n", "y"])  == "y":
            if st.selectbox("補助目盛線を追加", ["n", "y"]) == "y":
                ax1.minorticks_on()         # 補助目盛をつける
                ax1.grid(which = "both")    # 主目盛線線and補助目盛線の表示
            else :
                ax1.grid()    # 主目盛線


def setLabel(set_data_list, ax1, ax2, second_axis) :
    # $で囲む
    # 太文字: \mathbf
    # 斜体じゃない: \mathrm
    # 下付き: _
    # 上付き: ^

    # カラムを追加する
    if second_axis :
        col1, col2, col3 = st.columns(3)
    else :
        col1, col2 = st.columns(2)
    with col1 :
        x_label_var = st.text_input("x軸の変数")
        x_label_unit = st.text_input("x軸の単位")
        if x_label_unit == "":
            x_label_unit = "-"
        x_label = x_label_var + "$\ " + "[\mathrm{" + x_label_unit + "}]$"
        inputTextErr(x_label_var, x_label_unit)
        ax1.set_xlabel(x_label, fontsize = set_data_list["fontSize"], fontname=set_data_list["fontFamilyJa"])
    if second_axis:
        with col2 :
            y1_label_var = st.text_input("y1軸の変数")
            y1_label_unit = st.text_input("y1軸の単位")
            if y1_label_unit == "":
                y1_label_unit = "-"
            y1_label = y1_label_var + "$\ " + "[\mathrm{" + y1_label_unit + "}]$"
            inputTextErr(y1_label_var, y1_label_unit)
            ax1.set_ylabel(y1_label, fontsize = set_data_list["fontSize"], fontname=set_data_list["fontFamilyJa"])
        with col3 :
            y2_label_var = st.text_input("y2軸の変数")
            y2_label_unit = st.text_input("y2軸の単位")
            if y2_label_unit == "":
                y2_label_unit = "-"
            y2_label = y2_label_var + "$\ " + "[\mathrm{" + y2_label_unit + "}]$"
            inputTextErr(y2_label_var, y2_label_unit)
            ax2.set_ylabel(y2_label, fontsize = set_data_list["fontSize"], fontname=set_data_list["fontFamilyJa"])
    else :
        with col2 :
            y_label_var = st.text_input("y軸の変数")
            y_label_unit = st.text_input("y軸の単位")
            if y_label_unit == "":
                y_label_unit = "-"
            y_label = y_label_var + "$\ " + "[\mathrm{" + y_label_unit + "}]$"
            inputTextErr(y_label_var, y_label_unit)
            ax1.set_ylabel(y_label, fontsize = set_data_list["fontSize"], fontname=set_data_list["fontFamilyJa"])

# デフォルト(font_size)
def selectLegend(set_data_list, fig_number, fig_list_label, ax1, ax2, second_axis) :
    select_dict_legend = {'最適': "best", '右上': "upper right", '左上': "upper left", '左下': "lower left", '右下': "lower right", '左': "center left", '右': "center right", '下': "lower center", '上': "upper center", '中央': "center", '矢印': "arow"}
    select_legend = st.selectbox("凡例の表示形式", select_dict_legend)
    if select_legend != '矢印':
        # グラフの本体設定時に、ラベルを手動で設定する必要があるのは、barplotのみ。plotは自動で設定される＞
        col_number = int(st.number_input(label="列数", value=1))
        st.write("input: ", col_number)
        fram = st.selectbox("枠の有無", ["n", "y"])
        st.write("input: ", fram)
        if second_axis:
            handler1, label1 = ax1.get_legend_handles_labels()
            handler2, label2 = ax2.get_legend_handles_labels()
            if fram == "y":
                # 凡例をまとめて出力する
                ax1.legend(handler1 + handler2, label1 + label2, loc = select_dict_legend[select_legend], frameon = True, ncol=col_number, edgecolor=[0.,0.,0.], prop={"family":set_data_list["fontFamilyJa"], "size": set_data_list["fontSize"]})
            elif fram == "n":
                # 凡例をまとめて出力する
                ax1.legend(handler1 + handler2, label1 + label2, loc = select_dict_legend[select_legend], frameon = False, ncol=col_number, edgecolor=[0.,0.,0.], prop={"family":set_data_list["fontFamilyJa"], "size": set_data_list["fontSize"]})
        else :
            if fram == "y":
                # 凡例をまとめて出力する
                ax1.legend(loc = select_dict_legend[select_legend], frameon = True, ncol=col_number, edgecolor=[0.,0.,0.], prop={"family":set_data_list["fontFamilyJa"], "size": set_data_list["fontSize"]})
            elif fram == "n":
                # 凡例をまとめて出力する
                ax1.legend(loc = select_dict_legend[select_legend], frameon = False, ncol=col_number, edgecolor=[0.,0.,0.], prop={"family":set_data_list["fontFamilyJa"], "size": set_data_list["fontSize"]})
    if select_legend == "矢印":
        plt.gca.legend_ =None
        # カラムを追加する
        col1, col2 = st.columns(2)
        for i in range(fig_number) :
            with col1 :
                x = float(st.number_input(fig_list_label[i] + "x軸の矢印の先端位置"))
                inputNumberErr(x)
                y = float(st.number_input(fig_list_label[i] + "y軸の矢印の先端位置"))
                inputNumberErr(y)
            with col2 :
                text_x = float(st.number_input(fig_list_label[i] + "x軸のテキストの表示位置"))
                inputNumberErr(text_x)
                text_y = float(st.number_input(fig_list_label[i] + "y軸のテキストの表示位置"))
                inputNumberErr(text_y)
            # xycoordsがLデフォルトの'data'なので、
            # 座標(4, 1)のデータに対して座標(3, 1.5)にテキストを表示して
            # 矢印で線を引っ張る
            # width:矢印の太さ, headwidth:矢印の先端の三角形の高さ, headlength:矢印の先端の三角形の底辺の長さ, shrink:矢印を縮小する割合
            ax1.annotate(fig_list_label[i], fontfamily=set_data_list["fontFamilyJa"], fontweight="bold", xy=(x, y), fontsize=set_data_list["fontSize"], xytext=(text_x, text_y),
                arrowprops=dict(facecolor='black', shrink=1, width=0.1, headwidth=0, headlength=5),
                )