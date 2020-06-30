#! /usr/bin/python3.8
# -*- coding:utf-8 -*-
"""感染simulater（cv19sim.py）
    概要:感染症の拡大〜収束のプロセスをシュミレーションします。
        シミュレーションには単純なSIRモデルを用いています。
        作成者は防疫などの専門家ではないため、結果はあくまでも
        参考となります。この結果をもってリアルな防疫政策の策定
        や批評をすべきではありません。あくまでも、単純化したモ
        デル上において、人口密度や感染確率、人々の移動規制・外
        出規制を変化させることで、感染拡大〜収束の様子がどのよ
        うに変化するのかを「学習」するためのものです。

    使い方
        （必要であれば）パラメータを変更し、「セットアップ」ボ
        タンを押してください。設定が画面に反映され、シミュレー
        ションの準備が整います。
        続いて、「シミュレーション実行」ボタンを押すことで、シ
        ミュレーションが開始されます。シミュレーション中は、
        「一時停止」「再開ボタン」で、一時停止・再開ができます。
        シミュレーションが終了すると、「結果サマリ」のウィンドウ
        が表示されます。
    
    機能:以下の機能があります
        (1)シミュレーションの前提条件（パラメータ）の設定
            デフォルト値を用意していますが、利用者が変更すること
            が可能です。
            ※初期人数を大きくし過ぎないでください。処理が非常に
            重くなる場合があります。
        (2)パラメータの保存・復元
            パラメータはJson形式のファイルに書き出すことができ
            ます。また、以前の書き出しておいたパラメータファイル
            を読み込んで設定することができます。
        (3)シミュレーションのリアルタイム表示
            シミュレーション中は、感染者数や履歴グラフ、感染の様
            子をアニメーションで表示します。ただし、グラフやアニ
            メは処理が非常に重いため、結果のみが必要な場合は、こ
            れらの機能をオフすることができます。
        (4)シミュレーションの一時停止・再開
            シミュレーションを一時停止し、一部のパラメータを変更
            することができます。例えば、感染が拡大してきたので、
            規制を強化するとか、落ち着いてきたので緩和するなどが
            可能です。
        (5)結果サマリの表示
            シミュレーション終了後、別ウインドウで結果サマリが表
            示されます。コピー＆ペーストが可能です。このウィンド
            ウは「結果サマリ表示」ボタンでも表示できます。
            次のシミュレーションを実行しても、このウィンドウは破
            棄されません。なお、ボタン押下により表示した場合は、
            直近の結果サマリが表示されます。
        (6)シミュレーション結果の保存
            シミュレーション結果をcsvファイルに保存できます。複
            数の結果を保存し、後で表計算ソフトなどで分析する際に
            役立ちます
        (7)ヘルプ
            ヘルプを表示します。機能の他、プログラム内で使用して
            いる自作クラスや関数の説明もあります。利用上、これら
            クラスや関数の説明は不要ですが、pythonの学習用という
            意味も踏まえて表示しています。
            
    パラメータの説明:
        「サイクル」
            すべての人々の「移動〜感染判定」が終了する単位をさし
            ます。これを１日とみるか、１時間と見るかは利用者の
            自由です。
        「未感染者」
            まだ感染していない（逆に言えば感染しうる）人々です
        「感染者」
            感染した人です。これらの人々は、「未感染者」に感染さ
            せることができます。「感染者」は、他の「感染者」から
            感染しません。
            また、「感染者」には以下の３つの重篤度があります。
            「症状なし」：自分が感染している自覚はありません。ま
                わりからも感染しているとは分かりません。そのため、
                一般的には外出や移動に制限はありません。
            「軽症」：感染が確認され、自他とも認識している状態で
                す。一般的には、隔離（外出・移動制限）対象です。
            「重症」：入院が必要な状態です、一般的には、外出・移
                動はできません。
            「感染者」は、感染すると、まず「症状なし」の状態にな
            ります。その後、一定の割合で「軽症」→「重症」と悪化
            していきます。症状が進行するかどうかは、乱数を用いて
            １サイクル毎に判定します。
        「免疫保持者」
            感染から回復した人です。感染から一定期間（「免疫獲得
            サイクル」）たち、途中で死亡しなければ、「免疫保持者」
            になります。「免疫保持者」は再度感染はしません。一般
            的には、外出・移動の制限はかかりません。
            なお、感染者がゼロになった時（「免疫獲得者」か「死亡
            者」になった時）、シミュレーションは終了します。
        「死亡者」
            死亡した人です。外出・移動はしません。また、感染させ
            ることもありません。
            「死亡者」は、「感染者」の各重篤度別に、ある割合で発
            生します。死亡するかどうかは、乱数を用いて１サイクル
            毎に判定します。
        「フィールドサイズ（１辺）」
            シミュレーション空間の大きさを指定します。正方形です
            が壁は無く、右からはみ出すと左から、上からはみ出すと
            下からでてきます（つまり壁に衝突することはない）
        「打ち切りサイクル」
            シミュレーションが長期化した場合の打ち切りサイクルで
            す。このサイクルに達すると、シミュレーションは終了し
            ます（感染者が残った状態となります）。
        「平均移動距離」
            人が１回に移動する距離です。「平均」とあるように、こ
            の値を中心とした正規分布で、標準偏差４の範囲でランダ
            ムに移動します。「移動距離制限」がかかっている場合、
            その分割り引かれます。
            移動の方向は、進行方向（前回から移動してきた方向）を
            正面（中心）とした正規分布で、標準偏差８の範囲のラン
            ダムな方向に進みます。
        「感染領域」
            「感染者」が「非感染者」に感染させることができる領域
            （円）です。どちらも中心点座標で判定します。そのため、
            アニメーション画面と一致しない場合があります。
        「感染確率」
            「非感染者」が「感染領域」に入ってしまった場合の感染
            確率です。
        「免疫獲得サイクル」
            「感染者」が「免疫獲得者」になるまでのサイクルです。
            重篤度にかかわらず、「免疫獲得サイクル」を経過すると
            「免疫獲得者」になります。
        「症状変化率」
            重篤度の進行割合です。１サイクルごとの判定のため、あ
            まり大きな値にすると、あっという間に皆が重症化してし
            まいます。
        「感染者死亡率」
            重篤度に応じた死亡割合です。１サイクルごとの判定のた
            め、あまり大きな値にすると、あっという間に死に絶えて
            しまいます。
        「移動距離制限率」
            人々の移動距離を制限する割合です。「遠出を控える」に
            相当します。シミュレーション中でも一時停止することで、
            値を変更することができます。
        「移動対象者制限率」
            人々の移動そのものを制限する割合です。「外出制限」に
            相当します。シミュレーション中でも一時停止することで、
            値を変更することができます。
            
    補足・注意事項:
        ・「実行再生産数」は、厳密な計算ではありません。前サイク
        　ルと現サイクルの感染者数の差異から計算しています。
        　そのため、厳密には、「毎サイクルごとに基本再生産数を計
        　算している」ということになります。
        ・「経済活動(%)」は、「本来人々が移動したであろう距離の
        　合計」(合計人数×平均移動距離)に対して、「実際に移動し
        　た距離の合計」の割合で表現しています。感染者(軽症・重
        　症)が増えたり、外出規制（「移動対象者制限」）や移動規
        　制（移動距離制限）を強化すると、経済活動は減少します。
        
    実装方式:どのように構築されているかの説明です（マニアック）
        外部ライブラリは使用せず、python3.8の標準ライブラリの
        みで構築しています。GUIは、tkinterです。
        このプログラムは、Lynux(BionicPup32-jp - 19.03)
        上で開発されました。Windows10()で簡単な稼働確認をして
        います。
        [注意]Windows10で動かすためには、事前にpython3.8のイ
        ンストールが必要です。
        マルチスレッドには対応していません。
        シミュレーション空間とアニメーション画面は分離しています。
        移動・感染判定はすべてシミュレーション空間で行い、結果の
        みをアニメーション画面に表示しています。そのため、シミュ
        レーション空間（フィールドサイズ）を大きくとりすぎると、
        アニメーション画面上は重なっているのに感染しないように見
        える場合があります。
"""

import os, tkinter, tkinter.filedialog, tkinter.scrolledtext
import time, pathlib, datetime, glob, shutil, sys
import json, random, math, csv

###CONST
###ステータス
S_STATE = 'S'       #未感染者（S）
I_STATE = 'I'       #感染者（I）
R_STATE = 'R'       #免疫保持者（R）
D_STATE = 'D'       #死者（D）
#感染者重篤度(const)
I_RANK_NON = 'N'    #症状なし（移動制限なし）
I_RANK_LOW = 'L'    #軽症（隔離）
I_RANK_HIGH = 'H'   #重症（入院）
#画面関連
#キャンバス
SIM_PERSONS_R = 6
SIM_CANVAS_BASE_H = 500
SIM_CANVAS_BASE_W = SIM_CANVAS_BASE_H
SIM_CANVAS_H = SIM_CANVAS_BASE_H
SIM_CANVAS_W = SIM_CANVAS_BASE_W
STAT_CANVAS_H = 45
STAT_CANVAS_W = SIM_CANVAS_W
GRAPH_CANVAS_H = 150
GRAPH_CANVAS_W = SIM_CANVAS_W
#コマンドエリアの幅
CMD_AREA_W = 80
#パラメータエリアの幅
PRM_AREA_W = 190
#テキスト入力域の幅(文字数)
TXT_ENTRY_W = 6
#windowサイズ
WIN_H = STAT_CANVAS_H + GRAPH_CANVAS_H + SIM_CANVAS_H
WIN_W = PRM_AREA_W + CMD_AREA_W + SIM_CANVAS_W
#色
CANVAS_BACK_CLR = "black"
CANVAS_FONT_CLR = "white"
PERSON_S_CLR = "green"
PERSON_I_N_CLR = "yellow"
PERSON_I_L_CLR = "orange"
PERSON_I_H_CLR = "red"
PERSON_R_CLR = "blue"
PERSON_D_CLR = "white"
PERSON_ECO_CLR = "pink"
#パラメータ域のフォントサイズ
PRM_FONT_SIZE = "8"
#表示用タイトル
DSP_TITLES_DIC =[ ["サイクル", CANVAS_FONT_CLR, CANVAS_BACK_CLR],  \
                    ["未感染", CANVAS_FONT_CLR, PERSON_S_CLR],               \
                    ["感染(無)", CANVAS_BACK_CLR, PERSON_I_N_CLR],    \
                    ["感染(軽)", CANVAS_FONT_CLR, PERSON_I_L_CLR],    \
                    ["感染(重)", CANVAS_FONT_CLR, PERSON_I_H_CLR],   \
                    ["免疫保持", CANVAS_FONT_CLR, PERSON_R_CLR],   \
                    ["死亡", CANVAS_BACK_CLR, PERSON_D_CLR],   \
                    ["実行再生産数", CANVAS_FONT_CLR, CANVAS_BACK_CLR],  \
                    ["経済活動(%)", CANVAS_BACK_CLR, PERSON_ECO_CLR] ]
#wedgitのステータス（活性・非活性）
WG_DISABLE = "disabled"
WG_NORMAL = "normal"
#UserPrmクラス用
#値のタイプ（小数の入力を許可するか）
VAL_INT="INT"
VAL_DOUBLE="DOUBLE"
#Entry()を作るか、Label()を作るか
MAKE_ENTRY = "ENTRY"
MAKE_LABEL = "LABEL"
#StopWatchクラス用status定義
STAT_READY="READY"
STAT_RUN="RUN"
STAT_STOP="STOP"
#結果サマリ画面サイズ
RESULT_GIO="450x340"
#ヘルプ画面サイズ
HELP_GIO="600x430"
#ヘルプ画面(テキストボックス)の横幅(文字数)
HELP_WIDTH=60
#人口密度計算の単位
DENCTY_CELL=100
#サイクル実行フラグ
CYC_PAUSE="pause"
CYC_RUN="run"
#Personクラスの描画モード
MODE_REFRESH="refresh"
MODE_MOVE="move"

class TimeRec():
    """TimeRec【実行時間記録用クラス】

        実行時における、「画面構築」「セットアップ」「移動」
        「感染判定」「画面描写」の各実行時間を保持します。

    Attributes:
        allmovetime(float):
            「移動」処理の合計時間(ms)を保持
        allrenewtime(float):
            「感染判定」処理の合計時間(ms)を保持
        alldrawtime(float):
            「画面描写」処理の合計時間(ms)を保持
        buildtime(StopWatch):
            「画面構築」時間計測用StopWatchクラスの保持
        buildsimtime(StopWatch):
            「セットアップ」時間計測用StopWatchクラスの保持
        allsimtime(StopWatch):
            「シミュレーション」時間計測用StopWatchクラスの保持
        movetime(StopWatch):
            「移動」時間(1サイクル)計測用StopWatchクラスの保持
        renewtime(StopWatch):
            「感染判定」時間(1サイクル)計測用StopWatchクラスの保持
        drawtime(StopWatch):
            「画面描写」時間(1サイクル)計測用StopWatchクラスの保持
    """
    def __init__(self):
        """コンストラクタ

         インスタンスの構築を行う

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.allmovetime=0.0
        self.allrenewtime=0.0
        self.alldrawtime=0.0
        self.buildtime=StopWatch()
        self.buildsimtime=StopWatch()
        self.allsimtime=StopWatch()
        self.movetime=StopWatch()
        self.renewtime=StopWatch()
        self.drawtime=StopWatch()

    def addmovetime(self,addtime):
        """「移動」処理時間加算

         「移動」処理の合計時間(ms)に加算する

        Args:
            addtime(float):加算する時間(ms)
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.allmovetime += addtime

    def addrenewtime(self,addtime):
        """「感染判定」処理時間加算

         「感染判定」処理の合計時間(ms)に加算する

        Args:
            addtime(float):加算する時間(ms)
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.allrenewtime += addtime

    def adddrawtime(self,addtime):
        """「画面描写」処理時間加算

         「画面描写」処理の合計時間(ms)に加算する

        Args:
            addtime(float):加算する時間(ms)
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.alldrawtime += addtime
        
    def clearsimrec(self):
        """処理時間のクリア

         各処理時間をクリアする。
         ただし、「画面構築」(buildtime)はクリアしない
         （「画面構築」はアプリ起動時に１回しか呼ばれないため）

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.allmovetime=0.0
        self.allrenewtime=0.0
        self.alldrawtime=0.0
        self.buildsimtime.reset()
        self.allsimtime.reset()
        self.movetime.reset()
        self.renewtime.reset()
        self.drawtime.reset()
        
class StopWatch():
    """StopWatch【経過時間計測クラス】

        start〜stopまでの時間(ms)を計測します。
        タイマーは使用しておらず、呼び出し時のUNIX時間
        （エポック※）の差分で計測しています。
        ※：1970/1/1 午前0時からの経過秒数
        
         正しくないタイミングで各メソッドが呼ばれた場合は標準出
         力にメッセージを表示する。（わざわざ止めることはないと
         思うので、例外は発生させない）

    Attributes:
        starttime(float):
            startメソッド呼び出し時のUNIX時間
        stoptime(float):
            stopメソッド呼び出し時のUNIX時間
        status(str):
            動作時のステータス:
            STAT_READY:計測準備完了（初期化済み）
            STAT_RUN:計測中
            STAT_STOP:計測完了
        self.elapsedtime(float):
            経過時間(stoptime-starttime)
    """
    def __init__(self):
        """コンストラクタ

         インスタンスの構築を行う

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.starttime=0
        self.stoptime=0
        self.status=STAT_READY
        self.elapsedtime=0
        
    def start(self):
        """ストップウォッチのスタート
        
         ストップウォッチをスタートする。

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.status==STAT_READY:
            self.starttime=time.time()
            self.status=STAT_RUN
        else:
            print("[start]now status is [{}]. please reset()".format(self.status))
        
    def stop(self):
        """ストップウォッチのストップ
        
         ストップウォッチをストップする。
         経過時間(elapsedtime)をセットする

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.status==STAT_RUN:
            self.stoptime=time.time()
            self.elapsedtime=self.stoptime-self.starttime
            self.status=STAT_STOP
        else:
            print("[stop]now status is [{}]. please start()".format(self.status))
        
    def reset(self):
        """ストップウォッチのリセット
        
         ストップウォッチをリセット（初期化）する。

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.status==STAT_STOP or self.status==STAT_READY:
            self.__init__()
        else:
            print("[reset]now status is [{}]. please stop()".format(self.status))
            
    def blocking(self,blocktime):
        """処理のブロック
        
         スタートした時間から、指定された時間(ms)が経過するまで、
         処理をブロックする（このメソッドがリターンしない）
         もしこのメソッドが呼ばれた時点ですでに指定された時間を
         超過していた場合は、直ちにリターンする。
         なお、ループでブロックしているため、同一スレッド上の他
         の処理は実行できない

        Args:
            blocktime(int):ブロックする時間(ms)
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.status==STAT_RUN:
            block=self.starttime+(blocktime/1000) #秒にする
            while True:
                if block < time.time():
                    break

    def getelapsedtime(self):
        """経過時間の取得
        
         経過時間を取得する。

        Args:なし
        Returns:
            経過時間(ms)(float)を返す
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return float(self.elapsedtime*1000) #ミリ秒にする
        
    def getstarttime(self):
        """ スタート時間の取得
        
         スタート時間を取得する。

        Args:なし
        Returns:
            スタート時間のUNIX時間(float)を返す
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.starttime
        
    def getstoptime(self):
        """ ストップ時間の取得
        
         ストップ時間を取得する。

        Args:なし
        Returns:
            ストップ時間のUNIX時間(float)を返す
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.stoptime
        
    def getstatus(self):
        """ ステータスの取得
        
         現在のステータスを取得する。

        Args:なし
        Returns:
            現在のステータス(str)を返す
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.status

class UserPrm():
    """UserPrm【ユーザ指定パラメータクラス】

        ユーザが指定できるパラメータ（１個）のクラスです。
        パラメータデータの保持の他、画面表示のための設定値
        （タイトルやデータのタイプ）や、UIによる入力時のデータ
        チェックの機能を持ちます。
        また、入力時に他パラメータを自動更新するような場合（例え
        ば、今数字を入力したら、入力（キーストローク）のたびに、
        合計値を更新する、みたいな場合）のため、他パラメータ
        （インスタンス）へのリンケージ用メソッドがあります。
        このリンケージメソッドは実装されていない(pass)なので、
        利用する場合は、本クラスを継承して、独自クラスを作成し、
        リンケージメソッドを実装する必要があります。
        ※UIに関する設定値も持っているため、UI層とアプリデータ層
        の境界が若干あやふやな実装になってしまっています。

    Attributes:
        tag(str):パラメータのタグ名称(jsonで使用)
        title(str):入力エリアの日本語タイトル
        vl(int or float):保持する値
        valuetype(str):値のタイプ
            VAL_INT:小数の入力を許可しない
            VAL_DOUBLE:小数の入力を許可する
        uitype(str):UIのタイプ
            MAKE_ENTRY:入力域(Entry)をつくる
            MAKE_LABEL:表示のみ(Entryを作らない)
        sv(tkinter.StringVar):
            画面表示用の変数インスタンスの保持
            ※vlとsvは常に同期している
    """
    def __init__(self,tag,title,value,valuetype,uitype=MAKE_ENTRY):
        """コンストラクタ
        
         インスタンスの構築を行う

        Args:
            tag(str):パラメータのタグ名称(jsonで使用)
            title(str):入力エリアの日本語タイトル
            value(int or float):初期設定する値
            valuetype(str):値のタイプ。以下のいずれか
                VAL_INT:小数の入力を許可しない
                VAL_DOUBLE:小数の入力を許可する
            uitype(str,optional)):UIのタイプ。以下のいずれか
                MAKE_ENTRY:入力域(Entry)をつくる(デフォルト)
                MAKE_LABEL:表示のみ(Entryを作らない)
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.tag=tag
        self.title=title
        self.vl=value
        self.valuetype=valuetype        #"INT"or"DOUBLE"
        self.uitype=uitype
        self.sv=tkinter.StringVar()
        self.sv.set(self.vl)
   
    def set(self,value):
        """値の設定
        
         値を設定する

        Args:
            value(int or float):設定する値
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.vl=value
        self.sv.set(self.vl)
        
    def getsv(self):
        """値の取得
        
         値を取得する

        Args:なし
        Returns:値(int or float)
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.sv.get()
        
    def getvl(self):
        """画面表示用の変数インスタンスの取得
        
         画面表示用の変数インスタンスを取得する

        Args:なし
        Returns:変数インスタンス(tkinter.StringVar)
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.vl
        
    def gettag(self):
        """タグ名の取得
        
         タグ名(json用)を取得する

        Args:なし
        Returns:タグ名(str)
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.tag

    def gettitle(self):
        """入力エリアの日本語タイトルの取得
        
         入力エリアの日本語タイトルを取得する

        Args:なし
        Returns:入力エリアの日本語タイトル(str)
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.title

    def getuitype(self):
        """UIのタイプの取得
        
         UIのタイプを取得する

        Args:なし
        Returns:UIのタイプ(str)
            MAKE_ENTRY:入力域(Entry)あり
            MAKE_LABEL:表示のみ(Entryなし)
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return self.uitype

    def vcmd(self, rt):
        """入力値チェック用コールバック関数の登録
        
         入力値チェック用コールバック関数を登録する

        Args:
            rt(tkinter.Tk):widgitを配置する親
        Returns:コールバック関数に渡すコマンド列
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        return (rt.register(self.validate),
            '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W',self.tag  )

    def validate(self,action, index, value_if_allowed,  \
            prior_value, text, validation_type, trigger_type, widget_name, opt):
        """入力値チェック用コールバック関数
        
         入力値チェック（コールバック関数）
         数字（整数・小数）以外の入力は許可しない。
         （マイナスや指数表現(e)も不可）

        Args:
            action(int):アクションコード
                    1: 挿入
                    0: 削除
                    -1: フォーカスイン/アウト、textvariableの変化
            index(int):インデックス
                    0以上: 挿入/削除しようとしたカーソルの位置
                    -1: カーソル位置の関係ないアクション            
            value_if_allowed(str):変更を許可した場合の文字列
            prior_value(str):変更前の文字列
            text(str):挿入または削除した文字列
            validation_type(str):Entryに設定された発火条件。
                'focus', 'focusin', 'focusout',
                'key', 'all', 'none'
            trigger_type(str):コールバックした理由。
                'focusin', 'focusout', 'key', 'forced'
            widget_name(str):ウィジェット名の文字列
            opt(str):パラメータのタグ名称
        Returns:
                False:変更を許可しない
                True:変更を許可する
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.valuetype == VAL_INT:
            if text in '0123456789':
                #先頭のゼロはだめ（単独はOK）
                if len(value_if_allowed)>1 and value_if_allowed[0]=="0":
                    return False
                try:
                    self.vl=int(value_if_allowed)
                except ValueError:
                    return False
            else:
                return False
        elif self.valuetype == VAL_DOUBLE:
            if text in '.0123456789':
                #先頭のゼロはだめ（単独はOK+0.*はOK）
                if len(value_if_allowed)>1 and value_if_allowed[0]=="0":
                    if not value_if_allowed[0:2] == "0.":
                        return False
                try:
                    self.vl=float(value_if_allowed)
                except ValueError:
                    return False
            else:
                return False
        else:
            print("UserPrm class valuetype error input=<{}>".format(self.valuetype))
            return False

        self.linkage()
        
        return True

    def linkage(self):
        """パラメータ間の自動連携（ダミー）
        
         パラメータ間の自動連携機能を、サブクラスにて実装する。
         本クラスでは、呼び出されても何もしない。

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        pass
        
    def debug_print(self,action, index, value_if_allowed,   \
            prior_value, text, validation_type, trigger_type, widget_name, opt):
        """入力チェック関数のデバック用標準出力
        
         入力チェック関数（コールバック関数）をデバッグする時
         に使用する。コールバック関数が呼ばれた時のパラメータを
         標準出力に出力する。

        Args:※validate()を参照
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        print("="*20)
        print("TAG=<{}>".format(self.tag))
        print("アクションコード={}".format(action))
        print("インデックス={}".format(index))
        print("変更を許可した場合の文字列={}".format(value_if_allowed))
        print("変更前の文字列={}".format(prior_value))
        print("挿入または削除した文字列={}".format(text))
        print("発火条件={}".format(validation_type))
        print("コールバックした理由={}".format(trigger_type))
        print("ウィジット名の文字列={}".format(widget_name))
        print("opt={}".format(opt))

class FieldSize(UserPrm):
    """FieldSize【「フィールドサイズ(1辺)」用クラス（UserPrmを継承）】

        「初期人数:合計」と「フィールドサイズ(1辺)」から、
        「人口密度」を自動計算するクラスです。
        UserPrmクラスを継承しています。

    Attributes:
        tg1(UserPrm):
                参照するインスタンス（「初期人数:合計」）
        rslt(UserPrm):
                計算結果を格納するインスタンス（「人口密度」）
            ※他のAttributesはUserPrmクラスを参照
    """
    def addlink2(self,tg1,rslt):
        """参照および結果格納インスタンスの登録
        
         自動計算をするために、参照するインスタンスを結果格納す
         るインスタンスを登録します。

        Args:
            tg1(UserPrm):
                    参照するインスタンス（「初期人数:合計」）
           rslt(UserPrm):
                    計算結果を格納するインスタンス（「人口密度」）
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.tg1=tg1        #UserPrmクラスへのリンク(人数)
        self.rslt=rslt     #UserPrmクラスへのリンク

    def linkage(self):
        """自動計算（「人口密度」の計算）の実行
        
         登録されたインスタンス（「初期人数:合計」）を利用して
         計算結果を結果格納インスタンスに設定します。
         UserPrmクラスのlinkageメソッドをオーバーライド
         しています。

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.vl == 0:
            a=0
        else:
            a = self.tg1.getvl()/(self.vl**2)*DENCTY_CELL**2
        self.rslt.set(a)

class Total4dncty(UserPrm):
    """Total4dncty【「初期人数」用クラス（UserPrmを継承）】

        「初期人数:未感染者(S)」「初期人数:感染者(I)」
        「初期人数:免疫保持者(R)」「初期人数:死亡者(D)」から
        「初期人数:合計」を計算し、さらに「フィールドサイズ(1辺)」
        から、人口密度」を自動計算するクラスです。
        UserPrmクラスを継承しています。

    Attributes:
        tg1(UserPrm):
                参照するインスタンス（自身以外の初期人数）
        tg2(UserPrm):
                参照するインスタンス（自身以外の初期人数）
        tg3(UserPrm):
                参照するインスタンス（自身以外の初期人数）
        tg4(UserPrm):
                参照するインスタンス（「フィールドサイズ(1辺)」）
        rslt1(UserPrm):
                計算結果を格納するインスタンス（「初期人数:合計」）
        rslt2(UserPrm):
                計算結果を格納するインスタンス（「人口密度」）
            ※他のAttributesはUserPrmクラスを参照
    """
    
    def addlink(self,tg1,tg2,tg3,tg4,rslt1,rslt2):
        """参照および結果格納インスタンスの登録
        
         自動計算をするために、参照するインスタンスを結果格納す
         るインスタンスを登録します。

        Args:
            tg1(UserPrm):
                    参照するインスタンス（自身以外の初期人数）
            tg2(UserPrm):
                    参照するインスタンス（自身以外の初期人数）
            tg3(UserPrm):
                    参照するインスタンス（自身以外の初期人数）
            tg4(UserPrm):
                    参照するインスタンス（「フィールドサイズ(1辺)」）
            rslt1(UserPrm):
                    計算結果を格納するインスタンス（「初期人数:合計」）
            rslt2(UserPrm):
                    計算結果を格納するインスタンス（「人口密度」）
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.tg1=tg1        #UserPrmクラスへのリンク(人数内訳)
        self.tg2=tg2        #UserPrmクラスへのリンク(人数内訳)
        self.tg3=tg3        #UserPrmクラスへのリンク(人数内訳)
        self.tg4=tg4        #UserPrmクラスへのリンク(フィールドサイズ)
        self.rslt1=rslt1     #UserPrmクラスへのリンク(人数合計)
        self.rslt2=rslt2     #UserPrmクラスへのリンク(人口密度)

    def linkage(self):
        """自動計算（「初期人数:合計」「人口密度」の計算）の実行
        
         登録されたインスタンス（「初期人数」）を利用して
         計算結果（「初期人数:合計」および「人口密度」）を結果
         格納インスタンスに設定します。
         UserPrmクラスのlinkageメソッドをオーバーライド
         しています。

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        a = self.vl+self.tg1.getvl()+self.tg2.getvl()+self.tg3.getvl()
        self.rslt1.set(a)
        if self.vl == 0:
            b=0
        else:
            b = a/(self.tg4.getvl()**2)*DENCTY_CELL**2
        self.rslt2.set(b)
 
class UsrPrms():
    """UsrPrms【パラメータ保持クラス】

        各種パラメータ(UserPrm)のインスタンスを保持する、
        コレクション的なクラスです。

    Attributes:
        ups_dic(dic):
                インスタンスを辞書で保持します。
                key(str):インスタンスのタグ名
                value(UserPrm):インスタンス
    """
    def __init__(self):
        """コンストラクタ
        
         インスタンスの構築を行う

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.ups_dic={}

        #構築
        self.ups_dic["s_persons_count"]=Total4dncty(tag="s_persons_count",value=0,title="初期人数:未感染者(S)",valuetype=VAL_INT)
        self.ups_dic["i_persons_count"]=Total4dncty(tag="i_persons_count",value=0,title="初期人数:感染者(I)",valuetype=VAL_INT)
        self.ups_dic["r_persons_count"]=Total4dncty(tag="r_persons_count",value=0,title="初期人数:免疫保持者(R)",valuetype=VAL_INT)
        self.ups_dic["d_persons_count"]=Total4dncty(tag="d_persons_count",value=0,title="初期人数:死亡者(D)",valuetype=VAL_INT)
        self.ups_dic["total_persons_count"]= UserPrm(tag="total_persons_count",value=0,title="初期人数:合計",valuetype=VAL_INT,uitype=MAKE_LABEL)
        self.ups_dic["field_size"]=FieldSize(tag="field_size",value=0,title="フィールドサイズ(1辺)",valuetype=VAL_INT)
        self.ups_dic["density"]= UserPrm(tag="density",value=0,title="人口密度("+str(DENCTY_CELL)+"平方あたり)",valuetype=VAL_DOUBLE,uitype=MAKE_LABEL)

        #自動計算表示のためのリンケージ        
        self.ups_dic["s_persons_count"].addlink(tg1=self.ups_dic["i_persons_count"],tg2=self.ups_dic["r_persons_count"],tg3=self.ups_dic["d_persons_count"],    \
            tg4=self.ups_dic["field_size"],rslt1=self.ups_dic["total_persons_count"],rslt2=self.ups_dic["density"])
        self.ups_dic["i_persons_count"].addlink(tg1=self.ups_dic["s_persons_count"],tg2=self.ups_dic["r_persons_count"],tg3=self.ups_dic["d_persons_count"],    \
            tg4=self.ups_dic["field_size"],rslt1=self.ups_dic["total_persons_count"],rslt2=self.ups_dic["density"])
        self.ups_dic["r_persons_count"].addlink(tg1=self.ups_dic["s_persons_count"],tg2=self.ups_dic["i_persons_count"],tg3=self.ups_dic["d_persons_count"],    \
            tg4=self.ups_dic["field_size"],rslt1=self.ups_dic["total_persons_count"],rslt2=self.ups_dic["density"])
        self.ups_dic["d_persons_count"].addlink(tg1=self.ups_dic["s_persons_count"],tg2=self.ups_dic["i_persons_count"],tg3=self.ups_dic["r_persons_count"],    \
            tg4=self.ups_dic["field_size"],rslt1=self.ups_dic["total_persons_count"],rslt2=self.ups_dic["density"])
        #密度表示のためのリンケージ        
        self.ups_dic["field_size"].addlink2(tg1=self.ups_dic["total_persons_count"],rslt=self.ups_dic["density"])

        #構築
        self.ups_dic["cycle_max"]= UserPrm(tag="cycle_max",value=0,title="打ち切りサイクル",valuetype=VAL_INT)
        self.ups_dic["cycle_speed"]= UserPrm(tag="cycle_speed",value=0,title="サイクル速度(ms)",valuetype=VAL_INT)
        self.ups_dic["move_r"]= UserPrm(tag="move_r",value=0,title="平均移動距離",valuetype=VAL_INT)
        self.ups_dic["infection_r"]= UserPrm(tag="infection_r",value=0,title="感染領域",valuetype=VAL_INT)
        self.ups_dic["infection_rate"]= UserPrm(tag="infection_rate",value=0,title="感染確率",valuetype=VAL_DOUBLE)
        self.ups_dic["get_immunity_cycle"]= UserPrm(tag="get_immunity_cycle",value=0,title="免疫獲得サイクル",valuetype=VAL_INT)
        self.ups_dic["i_n2l_tran_rate"]= UserPrm(tag="i_n2l_tran_rate",value=0,title="症状変化率:症状なし→軽症",valuetype=VAL_DOUBLE)
        self.ups_dic["i_l2h_tran_rate"]= UserPrm(tag="i_l2h_tran_rate",value=0,title="症状変化率:軽症→重症)",valuetype=VAL_DOUBLE)
        self.ups_dic["n_dead_rate"]= UserPrm(tag="n_dead_rate",value=0,title="感染者死亡率:症状なし",valuetype=VAL_DOUBLE)
        self.ups_dic["l_dead_rate"]= UserPrm(tag="l_dead_rate",value=0,title="感染者死亡率:軽症(隔離)",valuetype=VAL_DOUBLE)
        self.ups_dic["h_dead_rate"]= UserPrm(tag="h_dead_rate",value=0,title="感染者死亡率:重症(入院)",valuetype=VAL_DOUBLE)
        self.ups_dic["s_move_limit_rate"]= UserPrm(tag="s_move_limit_rate",value=0,title="移動距離制限率:未感染者",valuetype=VAL_DOUBLE)
        self.ups_dic["i_n_move_limit_rate"]= UserPrm(tag="i_n_move_limit_rate",value=0,title="移動距離制限率:感染者(症状なし)",valuetype=VAL_DOUBLE)
        self.ups_dic["i_l_move_limit_rate"]= UserPrm(tag="i_l_move_limit_rate",value=0,title="移動距離制限率:感染者(軽症/隔離)",valuetype=VAL_DOUBLE)
        self.ups_dic["i_h_move_limit_rate"]= UserPrm(tag="i_h_move_limit_rate",value=0,title="移動距離制限率:感染者(重症/入院)",valuetype=VAL_DOUBLE)
        self.ups_dic["r_move_limit_rate"]= UserPrm(tag="r_move_limit_rate",value=0,title="移動距離移動制限率:免疫保持者",valuetype=VAL_DOUBLE)
        self.ups_dic["s_move_disable_rate"]= UserPrm(tag="s_move_disable_rate",value=0,title="移動対象者制限率:未感染者",valuetype=VAL_DOUBLE)
        self.ups_dic["i_n_move_disable_rate"]= UserPrm(tag="i_n_move_disable_rate",value=0,title="移動対象者制限率:感染者(症状なし)",valuetype=VAL_DOUBLE)
        self.ups_dic["i_l_move_disable_rate"]= UserPrm(tag="i_l_move_disable_rate",value=0,title="移動対象者制限率:感染者(軽症/隔離)",valuetype=VAL_DOUBLE)
        self.ups_dic["i_h_move_disable_rate"]= UserPrm(tag="i_h_move_disable_rate",value=0,title="移動対象者制限率:感染者(重症/入院)",valuetype=VAL_DOUBLE)
        self.ups_dic["r_move_disable_rate"]= UserPrm(tag="r_move_disable_rate",value=0,title="移動対象者制限率:免疫保持者",valuetype=VAL_DOUBLE)
        
    def loaddefault(self):
        """デフォルト値の設定
        
         各パラメータにデフォルト値を設定する
         (「初期値ボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #対象者人数
        self.ups_dic["s_persons_count"].set(199)    #未感染者（S）
        self.ups_dic["i_persons_count"].set(1)        #感染者（I）
        self.ups_dic["r_persons_count"].set(0)      #免疫保持者（R）
        self.ups_dic["d_persons_count"].set(0)           #死者（D）

        #対象者人数合計
        self.ups_dic["total_persons_count"].set( \
            self.ups_dic["s_persons_count"].getvl() +  self.ups_dic["i_persons_count"].getvl() +   \
            self.ups_dic["r_persons_count"].getvl() +  self.ups_dic["d_persons_count"].getvl() )

        #フィールドサイズ　※壁にあたったら、反対側から出てくる
        self.ups_dic["field_size"].set(500)

        #人口密度　※総人数÷フィールド面積
        self.ups_dic["density"].set(self.ups_dic["total_persons_count"].getvl() / self.ups_dic["field_size"].getvl()**2*(DENCTY_CELL**2))

        #サイクルMAX　※ここまで達したらシミュレーション終了。または、感染者がゼロになったら終了。
        self.ups_dic["cycle_max"].set(500)

        #サイクルスピード　※サイクルの実行間隔時間(msec)。画像表示が速すぎる場合の調整用
        self.ups_dic["cycle_speed"].set(100)

        #平均移動距離（r） ※ランダムな距離（正規分布）で、ランダムな方向(Θ)（進行方向に対して正規分布）で移動。
        self.ups_dic["move_r"].set(15)
        
        #感染領域（接近範囲）　※人がどれだけ近づいたら感染するかの距離
        self.ups_dic["infection_r"].set(10)
        
        #感染率　※感染領域内に入った場合の感染割合
        self.ups_dic["infection_rate"].set(0.6)
        
        #免疫獲得サイクル　※感染後何サイクル目で免疫を獲得するか
        self.ups_dic["get_immunity_cycle"].set(28)
        
        #感染者症状悪化割合　※以下のどの症状になるかの確率
        self.ups_dic["i_n2l_tran_rate"].set(0.03)        #症状なし→軽症
        self.ups_dic["i_l2h_tran_rate"].set(0.02)        #軽症→重症
        
        #死亡率　※感染した場合の１サイクル毎の死亡率
        self.ups_dic["n_dead_rate"].set(0.001)          #感染者用・症状なし
        self.ups_dic["l_dead_rate"].set(0.002)          #感染者用・軽症
        self.ups_dic["h_dead_rate"].set(0.005)           #感染者用・重症

        #距離移動制限率　※算出された移動距離を割り引く
        self.ups_dic["s_move_limit_rate"].set(0.0)          #未感染者用     
        self.ups_dic["i_n_move_limit_rate"].set(0.0)        #感染者用・症状なし
        self.ups_dic["i_l_move_limit_rate"].set(0.7)        #感染者用・軽症
        self.ups_dic["i_h_move_limit_rate"].set(1.0)        #感染者用・重症
        self.ups_dic["r_move_limit_rate"].set(0.0)          #免疫保持者用
        
        #対象者移動制限率　※移動可能な人数を制限する割合
        self.ups_dic["s_move_disable_rate"].set(0.0)        #未感染者用
        self.ups_dic["i_n_move_disable_rate"].set(0.0)      #感染者用・症状なし
        self.ups_dic["i_l_move_disable_rate"].set(0.8)      #感染者用・軽症
        self.ups_dic["i_h_move_disable_rate"].set(1.0)      #感染者用・重症
        self.ups_dic["r_move_disable_rate"].set(0.0)        #免疫保持者用

    def loadprms(self):
        """パラメータファイル(json)の読込み・設定
        
         パラメータファイル(json)を読込み、各パラメータに値を設
         定する。
         読込みファイル選択ダイアログを表示する。
         (「ロードボタン」押下時の処理)

        Args:なし
        Returns:なし
            False:読込みファイル選択ダイアログでキャンセル
                        が押された。
            True:読込み・設定が行われた
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        # ファイル選択ダイアログの表示
        fTyp = [("JSONファイル", "*.json")]
        in_f = tkinter.filedialog.askopenfilename(filetypes = fTyp, title='パラメータファイル（json）を選択してくだい。')
        
        #キャンセルが押された
        if 0 == len(in_f):
            return False
    
        b = open(in_f)
        c = json.load(b)
        b.close()

        for key,value in c.items():
            self.ups_dic[key].set(value)

        #計算値(total_persons_countとdensity)はjsonが間違っているかもしれないので再計算
        #対象者人数合計
        self.ups_dic["total_persons_count"].set( \
            self.ups_dic["s_persons_count"].getvl() +  self.ups_dic["i_persons_count"].getvl() +   \
            self.ups_dic["r_persons_count"].getvl() +  self.ups_dic["d_persons_count"].getvl() )
        #人口密度　※総人数÷フィールド面積
        self.ups_dic["density"].set(self.ups_dic["total_persons_count"].getvl() / self.ups_dic["field_size"].getvl()**2*(DENCTY_CELL**2))

        
        return True
         
    def saveprms(self):
        """パラメータをファイル(json)に保存する
        
         各パラメータをパラメータファイル(json)に保存する。
         保存ファイル選択ダイアログを表示する。
         (「セーブボタン」押下時の処理)

        Args:なし
        Returns:なし
            False:保存ファイル選択ダイアログでキャンセル
                        が押された。
            True:保存が行われた
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        prm_json = {}
        
        for key, value in self.ups_dic.items():
            prm_json[key]=value.getvl()
        
        # ファイル選択ダイアログの表示
        fTyp = [("JSONファイル", "*.json")]
        out_f = tkinter.filedialog.asksaveasfilename(filetypes = fTyp, title='パラメータファイル（json）を選択してくだい。')
        
        #キャンセルが押された
        if 0 == len(out_f):
            return False
        
        a = open(out_f, "w")
        json.dump(prm_json,a,indent=4)
        a.close()
        
        return True

class Person():
    """Person【人クラス】

        感染の対象となる人の状態を保持するクラスです。

    Attributes:
        id(str):識別番号("PS"+番号)
                シミュレーション時の図形識別TAGとしても使用
        stat(str):感染状態
                「未感染→感染→免疫or死」の順に遷移
        serious(str):感染時の重篤度
                「症状なし→軽症→重症」の順にランダムに遷移
        point[x,y](float,float):シミュレーション空間に
                おける現在の座標（画面表示の座標ではない）
        degree(float):進行方向(角度)
                ※厳密には、前回位置から見た今回位置の方向（角度）
        delta_x(float):
                シミュレーション空間における移動先までのx座標(増分)
        delta_y(float):
                シミュレーション空間における移動先までのy座標(増分)
        r(float):
                シミュレーション空間における移動距離
        odometter(float):
                シミュレーション空間における累積移動距離
        i_history[cycle,distance](int,float):
                感染時のサイクル、累積移動距離
        r_history[cycle,distance](int,float):
                免疫保持時or死亡時のサイクル、累積移動距離
        item_id(int):図形表示用のID(図形識別TAGとは違うもの)
    """    
    def __init__(self, id, stat = S_STATE,  serious = ""):
        """コンストラクタ
        
         インスタンスの構築を行う

        Args:
            id(int):識別番号(PSxx)の生成に使用。重複不可
            stat(str):初期構築時のステータス。以下のいずれか
                S_STATE:未感染者(デフォルト)
                I_STATE:感染者
                R_STATE:免疫保持者
                D_STATE:死者
            serious(str):初期構築時の重篤度。以下のいずれか
                        "":なし(初期構築時のステータスが感染者以外の時)（デフォルト）
                I_RANK_NON:症状なし
                I_RANK_LOW:軽症
                I_RANK_HIGH:重症
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.id = "PS"+str(id)    #もしかしたら後で使うかも知れないので作っておく
        self.stat = stat    #ステータス   ※感染状態（未感染→感染→免疫or死）
        self.serious = serious   #重篤度　※（症状なし/軽症/重症）
        self.point = [random.uniform(0,main.up.ups_dic["field_size"].getvl()), random.uniform(0,main.up.ups_dic["field_size"].getvl()) ]    #現在位置（x, y）※論理的な位置
        self.degree = random.randint(0,360)
        self.delta_x = 0
        self.delta_y = 0
        self.r=0.0
        self.odometter = 0  #累計移動距離
        self.i_history = [0,0]     #感染時（サイクル、移動距離）
        self.r_history = [0,0]      #免疫保持時or死亡時（サイクル、移動距離）
        self.item_id = None #図形ID

    def move(self):
        """人の移動
        
         シュミレーション空間上で人をランダムに移動させる
         （画面への反映はここでは行わない）

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.r=0.0
        self.delta_x = 0
        self.delta_y = 0

        #ステータスチェック（死亡の場合はリターン（移動しない））
        #対象者移動制限を判定する（乱数と対象者移動制限率で算出）
        #対象者移動制限ならば、リターン（移動しない）
        if self.stat == D_STATE:
            return
        elif self.stat == S_STATE:
            if [True] == random.choices([True,False],weights=[main.up.ups_dic["s_move_disable_rate"].getvl(), 1-main.up.ups_dic["s_move_disable_rate"].getvl()],k=1):
                return
        elif self.stat == R_STATE:
            if [True] == random.choices([True,False],weights=[main.up.ups_dic["r_move_disable_rate"].getvl(), 1-main.up.ups_dic["r_move_disable_rate"].getvl()],k=1):
                return
        else:       #i_stat
            if self.serious == I_RANK_NON:
                if [True] == random.choices([True,False],weights=[main.up.ups_dic["i_n_move_disable_rate"].getvl(), 1-main.up.ups_dic["i_n_move_disable_rate"].getvl()],k=1):
                    return
            elif self.serious == I_RANK_LOW:       
                if [True] == random.choices([True,False],weights=[main.up.ups_dic["i_l_move_disable_rate"].getvl(), 1-main.up.ups_dic["i_l_move_disable_rate"].getvl()],k=1):
                    return
            else:       #I_RANK_HIGH
                if [True] == random.choices([True,False],weights=[main.up.ups_dic["i_h_move_disable_rate"].getvl(), 1-main.up.ups_dic["i_h_move_disable_rate"].getvl()],k=1):
                    return

        #移動予定距離（r）・移動予定方向（Θ）をランダムに決める
        r = random.normalvariate(main.up.ups_dic["move_r"].getvl(),4)       #標準偏差はとりあえず4
        dlt_degree = random.normalvariate(0,50)    #標準偏差はとりあえず8
        self.degree += dlt_degree
        radian = math.radians(self.degree)

        #距離移動制限率で移動予定距離を補正する
        if self.stat == S_STATE:
            r = r *(1-main.up.ups_dic["s_move_limit_rate"].getvl())
        elif self.stat == R_STATE:
            r = r *(1-main.up.ups_dic["r_move_limit_rate"].getvl())
        else:       #i_stat
            if self.serious == I_RANK_NON:
                r = r *(1-main.up.ups_dic["i_n_move_limit_rate"].getvl())
            elif self.serious == I_RANK_LOW:       
                r = r *(1-main.up.ups_dic["i_l_move_limit_rate"].getvl())
            else:       #I_RANK_HIGH
                r = r *(1-main.up.ups_dic["i_h_move_limit_rate"].getvl())

        #移動分の座標を求める
        cos_x = math.cos(radian)
        sin_y = math.sin(radian)

        #壁にあたったら、反対側から出てくる
        if 0 > ((r*cos_x) + self.point[0]):
            self.delta_x = ((r*cos_x)+main.up.ups_dic["field_size"].getvl())
        elif main.up.ups_dic["field_size"].getvl() < ((r*cos_x) + self.point[0]):
            self.delta_x = ((r*cos_x)-main.up.ups_dic["field_size"].getvl()) 
        else:
            self.delta_x = (r*cos_x) 
        self.point[0]  += self.delta_x

        if 0 > ((r*sin_y) + self.point[1]):
            self.delta_y = ((r*sin_y)+main.up.ups_dic["field_size"].getvl())
        elif main.up.ups_dic["field_size"].getvl() < ((r*sin_y) + self.point[1]):
            self.delta_y = ((r*sin_y)-main.up.ups_dic["field_size"].getvl())
        else:
            self.delta_y = (r*sin_y)
        self.point[1] += self.delta_y

        #累計移動距離の更新
        self.r=r
        self.odometter += r

    def stat_renew(self):
        """感染判定
        
         自分が感染するか判定する。近くに感染者がいれば、
         ある確率で感染する。

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #未感染者の場合
        if self.stat == S_STATE:
            #感染者を探す
            for p in [pp for pp in main.persons if pp.stat == I_STATE]:
                if self.id != p.id:     #自分は省く
                    #ステータスチェック
                    delta_x = self.point[0] - p.point[0]
                    delta_y = self.point[1] - p.point[1]
                    #感染領域（接近範囲）内に他の感染者がいれば、ステータスを感染者に。
                    if main.up.ups_dic["infection_r"].getvl()**2 > (delta_x**2 + delta_y**2):
                        if [True] == random.choices([True,False],weights=[main.up.ups_dic["infection_rate"].getvl(), 1-main.up.ups_dic["infection_rate"].getvl()],k=1):
                            #重篤度を感染者重篤割合を使ってランダムに設定。
                            self.stat = I_STATE
                            self.serious = I_RANK_NON
                            #履歴に、感染時（サイクル、移動距離）を記録
                            self.i_history = [main.now_cycle,self.odometter]
 
                            break
        #感染者の場合。
        elif self.stat == I_STATE:
            #感染期間が、免疫獲得サイクルを越えていれば（現在サイクルー履歴.感染時サイクル＞感染期間）、
            if main.up.ups_dic["get_immunity_cycle"].getvl() < (main.now_cycle - self.i_history[0] ):
                #ステータスを免疫保持者に更新
                self.stat = R_STATE
                #履歴に、免疫保持時（サイクル、移動距離）を記録
                self.r_history = [main.now_cycle,self.odometter]
            else:
                #死亡率により死亡判定。死亡の場合はステータスを死亡に。
                #履歴に、死亡時（サイクル、移動距離）を記録
                if self.serious == I_RANK_NON:
                    dead_rate = main.up.ups_dic["n_dead_rate"].getvl()
                elif self.serious == I_RANK_LOW:
                    dead_rate = main.up.ups_dic["l_dead_rate"].getvl()
                else:   #I_RANK_HIGH
                    dead_rate = main.up.ups_dic["h_dead_rate"].getvl()
                if [True] == random.choices([True,False],weights=[dead_rate, 1-dead_rate],k=1):
                    self.stat = D_STATE
                    self.r_history = [main.now_cycle,self.odometter]
                #死ななかったら、次の症状にランダムに移行
                else:
                    if self.serious == I_RANK_NON:
                        if [True] == random.choices([True,False],weights=[main.up.ups_dic["i_n2l_tran_rate"].getvl(), 1-main.up.ups_dic["i_n2l_tran_rate"].getvl()],k=1):
                            self.serious = I_RANK_LOW
                    elif self.serious == I_RANK_LOW:
                        if [True] == random.choices([True,False],weights=[main.up.ups_dic["i_l2h_tran_rate"].getvl(), 1-main.up.ups_dic["i_l2h_tran_rate"].getvl()],k=1):
                            self.serious = I_RANK_HIGH

    def drow_p(self,refresh=MODE_MOVE):
        """図形描画
        
         シミュレーション画面に図形を描写or移動する。
            初期描画時：描画(create_oval)
            それ以外：移動(move)         

        Args:
            refresh:描画モード。以下のいずれか
                MODE_REFRESH:描画する
                MODE_MOVE:移動する(デフォルト)
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.stat == S_STATE:
            d_color = PERSON_S_CLR
        elif self.stat == I_STATE:
            if self.serious == I_RANK_NON:
                d_color = PERSON_I_N_CLR
            elif self.serious == I_RANK_LOW:
                d_color = PERSON_I_L_CLR
            else:    #I_RANK_HIGH
                d_color = PERSON_I_H_CLR
        elif self.stat == R_STATE:
            d_color = PERSON_R_CLR            
        else:       #D_STATE
            d_color = PERSON_D_CLR
        
        #中心点から  矩形座標（始点、終点）に変換
        dx1 = self.point[0]*main.disp_exp_rate
        dy1 = self.point[1]*main.disp_exp_rate
        dx2 = self.point[0]*main.disp_exp_rate + SIM_PERSONS_R
        dy2 = self.point[1]*main.disp_exp_rate + SIM_PERSONS_R

        if refresh == MODE_REFRESH:
            self.item_id=main.canvas_sim.create_oval(dx1,dy1,dx2,dy2,fill=d_color,tags=self.id)
        else:
            main.canvas_sim.itemconfig(self.item_id, fill=d_color)
            main.canvas_sim.move(self.id,self.delta_x*main.disp_exp_rate, self.delta_y*main.disp_exp_rate)

    def dump_dsp(self):
        """ダンプ
        
         インスタンスの情報を標準出力に書き出す。（デバッグ用）

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        print("{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}".format( self.id,self.stat,self.serious, \
            self.point[0],self.point[1],self.degree,self.delta_x,self.delta_y,  \
            self.r,self.odometter,self.i_history[0],self.i_history[1],  \
            self.r_history[0],self.r_history[1],self.item_id ))

class Prm_entry():
    """Prm_entry【パラメータ入力クラス】

        パラメータ入力用wedgitを構築します。
        項目名を示すラベル(label)と入力域(entry)をセットで構築
        します。(項目名：左側、入力域：右側)
        データの入出力は、パラメータとして渡されるUserPrmクラス
        内の、StiringVarクラス(Tkinter)を介して行われます。
        入力なし（データ表示のみ）の場合は、入力域(entry)のかわ
        りにラベル(label)を使ってデータを表示します。

    Attributes:
        parent(Frame):wedgitを配置する親フレーム
        row(int):配置する行数
        userprm(UserPrm):データ格納用クラス
        lb(Label):項目表示用のラベル(label)wedgit
        entry(Entory or Label):データ入力域wedgit
                ※入力なし（データ表示のみ）の場合は、ラベルwedgit
    """
    def __init__(self, parent, row, userprm):
        """コンストラクタ
        
         インスタンスの構築を行う

        Args:
            parent(Frame):wedgitを配置する親フレーム
            row(int):配置する行数
            userprm(UserPrm):データ格納用クラス
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        self.parent = parent    #wedgitを配置する親
        self.row = row    #配置する行数
        self.userprm=userprm
        self.lb = tkinter.Label(self.parent, text=self.userprm.gettitle(), anchor=tkinter.W, font=("", PRM_FONT_SIZE))
        self.lb.grid(row=self.row, column=0, columnspan=1,sticky=tkinter.W + tkinter.E)

        if self.userprm.getuitype() == MAKE_ENTRY:
            self.entry = tkinter.Entry(self.parent, textvariable=self.userprm.sv,  \
                width=TXT_ENTRY_W, justify=tkinter.RIGHT,   \
                validate = 'key', validatecommand = self.userprm.vcmd(self.parent),   \
                font=("", PRM_FONT_SIZE))
            self.entry.grid(row=self.row, column=1, columnspan=1,sticky=tkinter.W + tkinter.E)
        else:       #MAKE_LABEL
            self.entry = tkinter.Label(self.parent, textvariable=self.userprm.sv, anchor=tkinter.E, font=("", PRM_FONT_SIZE))
            self.entry.grid(row=self.row, column=1, columnspan=1,sticky=tkinter.W + tkinter.E)

class ResultSummry():
    """ResultSummry【サマリ表示ウインドウクラス】

        サマリ表示ウインドウを構築します。
        独立したウインドウとして構築し、複数行テキスト入力
        域(text)に、渡された文字列（複数行）を表示します。
        複数行テキスト入力域では編集が可能ですが、保存はできません。

    Attributes:
        frame_smry(Frame):外側のフレーム。
        textbox(Text):サマリデータ表示用複数行テキスト入力域
        button(Button):「閉じる」ボタン
    """
    def __init__(self,sectences):
        """コンストラクタ
        
         サマリ表示ウインドウの構築を行う

        Args:
            sectences(str[]):
                    表示する文字列のリスト(文字列末尾に"\n"を自動付加)
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        master=tkinter.Toplevel()
        master.geometry(RESULT_GIO)
        master.title("シミュレーション結果サマリ")
        
        #フレーム（外側）を作成
        self.frame_smry = tkinter.Frame(master)
        self.frame_smry.pack()
        self.textbox = tkinter.Text(self.frame_smry, height=len(sectences))
        self.textbox.pack()
        self.button = tkinter.Button(self.frame_smry,text="閉じる",command=master.destroy)
        self.button.pack()
        
        i=1
        for strline in sectences:
            self.textbox.insert(str(i)+".0",strline+"\n")
            i += 1

class HelpWindow():
    """HelpWindow【ヘルプウインドウクラス】

        ヘルプウインドウを構築します。
        ヘルプの内容は、本ソースのDocString(__dic__)です。

    Attributes:
        frame_help(Frame):外側のフレーム。
        textbox(ScrolledText):
                ヘルプ用スクロールバー付複数行テキスト入力域
        button(Button):「閉じる」ボタン
    """
    def __init__(self):
        """コンストラクタ
        
         ヘルプウインドウの構築を行う

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        master=tkinter.Toplevel()
        master.geometry(HELP_GIO)
        master.title("ヘルプ")
        
        #フレーム（外側）を作成
        self.frame_help = tkinter.Frame(master)
        self.frame_help.pack()
        self.button = tkinter.Button(self.frame_help,text="閉じる",command=master.destroy)
        self.button.grid(row=0,column=0,sticky=tkinter.W)

        self.textbox = tkinter.scrolledtext.ScrolledText(self.frame_help,width=HELP_WIDTH)
        self.textbox.grid(row=1,column=0,sticky=tkinter.W + tkinter.E)

        self.textbox.insert("1.0",__doc__)
        self.textbox.insert(tkinter.END,"\n□□□ 以下クラス説明 □□□\n")
        self.textbox.insert(tkinter.END,MainApp.__doc__+"\n")
        self.textbox.insert(tkinter.END,Person.__doc__+"\n")
        self.textbox.insert(tkinter.END,UserPrm.__doc__+"\n")
        self.textbox.insert(tkinter.END,UsrPrms.__doc__+"\n")
        self.textbox.insert(tkinter.END,Prm_entry.__doc__+"\n")
        self.textbox.insert(tkinter.END,Total4dncty.__doc__+"\n")
        self.textbox.insert(tkinter.END,FieldSize.__doc__+"\n")
        self.textbox.insert(tkinter.END,ResultSummry.__doc__+"\n")
        self.textbox.insert(tkinter.END,HelpWindow.__doc__+"\n")
        self.textbox.insert(tkinter.END,TimeRec.__doc__+"\n")
        self.textbox.insert(tkinter.END,StopWatch.__doc__+"\n")
        
class MainApp():
    """MainApp【アプリメインクラス】

        本アプリケーションのメインクラスです。
        画面を構築し、ユーザからの操作を受付ます。
        また、アプリ全体の各種オブジェクトを保持します。

    Attributes:
        <シミュレーション制御関連>
            *感染者数が最大となったタイミングの記録
            i_t_max[人数,サイクル](int,int):全体
            i_n_max[人数,サイクル](int,int):症状なし
            i_l_max[人数,サイクル](int,int):軽症 
            i_h_max[人数,サイクル](int,int):重症
        now_cycle(int):現在サイクル(現在表示中のサイクル番号)
        sim_history[
                サイクル(int),
                未感染者数(int),
                感染者(症状なし)数(int),
                感染者(軽症)数(int),
                感染者(重症)数(int),
                免疫保持者数(int),
                死亡者数(int),
                実行再生産数(float),
                経済活動(%)(float)]:サイクル毎の人数（グラフ表示用）
        sim_histories[](sim_history):
                シミュレーション履歴(sim_historyのリスト)
        persons[](Person):対象者オブジェクトのリスト
            *グラフ(多角形)生成用の座標リスト
            s_his[](float):未感染者数(多角形)
            i_n_his[](float):感染者(症状なし)数(多角形)
            i_l_his[](float):感染者(軽症)数(多角形)
            i_h_his[](float):感染者(重症)数(多角形)
            r_his[](float):免疫保持者数(多角形)
            d_his[](float):死亡者数(多角形)
            eco_his[](float):経済活動(%)(折線)
        sentences[](str):サマリ表示文字列(1行)のリスト
        stat_count[](int):ステータスカウント用のリスト
        up(UsrPrms):ユーザーパラメータの保持
        disp_exp_rate(float):
                シミュレーション座標と表示キャンバスの比率
        ecoact(float):本来の経済活動規模(分母)
        ecoeffect(float):実際の経済活動規模(分子)
        jobid(int):次回実行するシミュレーションスレッドのID
        tr(TimeRec):実行時間計測用オブジェクト
        run_mode(str):サイクル実行フラグ
            CYC_PAUSE:一時停止中
            CYC_RUN:実行中

        <画面関連>
        root(tkinter):tkinterのルートオブジェクト
        [画面左側]
        frame_wpain(Frame):画面左側の外枠フレーム
        frame_prms(Frame):パラメータ入力用フレーム
        ent_dic{key,value}(str,UserPrm):
            wedgit（パラメータ入力）の管理用辞書
        frame_butom(Frame):ボタン用フレーム
        load_json_buttom(Button):ロードボタン
        save_json_buttom(Button):セーブボタン
        set_default_buttom(Button):初期値ボタン
        setup_buttom(Button):セットアップボタン
        nodsp_checkbv(BooleanVar):画面更新モード変数
        nodsp_check(Checkbutton):画面更新モードチェックボタン
        run_buttom(Button):実行ボタン
        pause_buttom(Button):一時停止ボタン
        restart_buttom(Button):再開ボタン
        summry_buttom(Button):サマリ表示ボタン
        save_csv_buttom(Button):結果保存ボタン
        help_buttom(Button):ヘルプボタン
        close_buttom(Button):終了ボタン
        [画面右側]
        frame_epain(Frame):画面右側の外枠フレーム
        frame_stat(Frame):ステータス(人数)表示用フレーム
        canvas_graph(Canvas):グラフ表示用キャンバス
        canvas_sim(Canvas):シミュレーション用キャンバス

    """
    def __init__(self):
        """コンストラクタ
        
         アプリデータ/オブジェクトの構築を行う

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        ###実行用変数（オブジェクト）
        #最大感染者数（人数、サイクル）　※感染者数が最大となったタイミングの記録
        self.i_t_max = [0,0]        #全体
        self.i_n_max = [0,0]        #症状なし（移動制限なし）
        self.i_l_max = [0,0]        #軽症（隔離） 
        self.i_h_max = [0,0]        #重症（入院）
        
        self.now_cycle = 0       #現在サイクル　※現在表示中のサイクル番号
        
        #シミュレーション履歴　※サイクル毎の人数（グラフ表示用）、リスト形式
        self.sim_histories = []
        #no,s,i_n,i_l,i_h,r,d,R,ECO
        self.sim_history = [0,0,0,0,0,0,0,0.0,0.0]
        
        #対象者管理　※対象者オブジェクトをリストで管理
        self.persons = []
        
        #グラフ生成用のリスト
        self.s_his = []
        self.i_n_his =[]
        self.i_l_his =[]
        self.i_h_his =[]
        self.r_his =[]
        self.d_his =[]
        self.eco_his =[]
        
        #サマリ表示データのリスト
        self.sentences=[]
        
        #ステータスカウント用のリスト
        self.stat_count=[]

        #時間計測
        self.tr=TimeRec()
        
        #構築        
        self.buildapp()

    def buildapp(self):
        """メインウインドウの構築
        
         メインウインドウの構築を行う

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #実行時間計測
        self.tr.buildtime.start()
    
        #画面生成   ※これを最初にやらないと、なぜかStringVar()が画面表示されない
        #メインウインドウ
        self.root = tkinter.Tk()
        self.root.title("感染シミュレーション v0.011")
        self.root.geometry(str(WIN_W)+"x"+str(WIN_H))
        
        #ユーザーパラメータの構築
        self.up=UsrPrms()
        self.up.loaddefault()

        #シミュレーション座標と表示キャンバスの比率
        self.disp_exp_rate = SIM_CANVAS_BASE_H / self.up.ups_dic["field_size"].getvl()

        #画面構築
        #画面左側
        #フレーム（外側）を作成
        self.frame_wpain = tkinter.Frame(self.root)
        self.frame_wpain.grid(row=0, column=0, sticky=tkinter.N)
        
        #パラメータ入力用フレームを作成
        self.frame_prms = tkinter.Frame(self.frame_wpain, width=PRM_AREA_W , height=WIN_H)
        self.frame_prms.pack()
        
        #wedgit（パラメータ入力）の配置（２列×n行）
        self.ent_dic={}
        i=0
        for key, userprm in self.up.ups_dic.items():
            self.ent_dic[key]=Prm_entry(self.frame_prms,i, userprm)
            i += 1
        
        #ボタンの配置
        #ボタン用フレームを作成
        self.frame_butom = tkinter.Frame(self.frame_wpain)
        self.frame_butom.pack()
        #ロードボタン
        self.load_json_buttom = tkinter.Button(self.frame_butom, text="パラメータ読込", font=("", PRM_FONT_SIZE), command=self.up.loadprms)
        self.load_json_buttom.grid(row=0, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)
        #セーブボタン
        self.save_json_buttom = tkinter.Button(self.frame_butom, text="パラメータ書出", font=("", PRM_FONT_SIZE), command=self.up.saveprms)
        self.save_json_buttom.grid(row=0, column=1, columnspan=1, sticky=tkinter.W + tkinter.E)
        #初期値ボタン
        self.set_default_buttom = tkinter.Button(self.frame_butom, text="初期値に戻す", font=("", PRM_FONT_SIZE), command=self.up.loaddefault)
        self.set_default_buttom.grid(row=1, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)
        #セットアップボタン
        self.setup_buttom = tkinter.Button(self.frame_butom, text="セットアップ", font=("", PRM_FONT_SIZE), command=self.buildsim)
        self.setup_buttom.grid(row=1, column=1, columnspan=1, sticky=tkinter.W + tkinter.E)

        #画面更新モードチェックボタン
        self.nodsp_checkbv = tkinter.BooleanVar()       # チェックON・OFF変数
        self.nodsp_check = tkinter.Checkbutton(self.frame_butom, variable=self.nodsp_checkbv, text="画面更新しない(高速)",font=("", PRM_FONT_SIZE))
        self.nodsp_check.grid(row=2, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)

        #実行ボタン
        self.run_buttom = tkinter.Button(self.frame_butom, text="シミュレーション実行", font=("", PRM_FONT_SIZE), command=self.runsim)
        self.run_buttom.grid(row=2, column=1, columnspan=1, sticky=tkinter.W + tkinter.E)

        #一時停止ボタン
        self.pause_buttom = tkinter.Button(self.frame_butom, text="一時停止", font=("", PRM_FONT_SIZE), command=self.pause)
        self.pause_buttom.grid(row=3, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)
        #再開ボタン
        self.restart_buttom = tkinter.Button(self.frame_butom, text="再開", font=("", PRM_FONT_SIZE), command=self.restart)
        self.restart_buttom.grid(row=3, column=1, columnspan=1, sticky=tkinter.W + tkinter.E)
        #サマリ表示ボタン
        self.summry_buttom = tkinter.Button(self.frame_butom, text="結果サマリ表示", font=("", PRM_FONT_SIZE), command=self.dispsummry)
        self.summry_buttom.grid(row=4, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)
        #結果保存ボタン
        self.save_csv_buttom = tkinter.Button(self.frame_butom, text="結果保存", font=("", PRM_FONT_SIZE), command=self.savehistory)
        self.save_csv_buttom.grid(row=4, column=1, columnspan=1, sticky=tkinter.W + tkinter.E)
        #ヘルプボタン
        self.help_buttom = tkinter.Button(self.frame_butom, text="ヘルプ", font=("", PRM_FONT_SIZE), command=self.help)
        self.help_buttom.grid(row=5, column=0, columnspan=1, sticky=tkinter.W + tkinter.E)
        #終了ボタン
        self.close_buttom = tkinter.Button(self.frame_butom, text="終了", font=("", PRM_FONT_SIZE), command=sys.exit)
        self.close_buttom.grid(row=5, column=1, columnspan=1, sticky=tkinter.W + tkinter.E)

        #実行ボタン・一時停止ボタン・再開ボタン・サマリ表示ボタン・結果保存ボタンは最初は非活性
        self.run_buttom.configure(state = WG_DISABLE)        
        self.pause_buttom.configure(state = WG_DISABLE)        
        self.restart_buttom.configure(state = WG_DISABLE)
        self.summry_buttom.configure(state = WG_DISABLE)
        self.save_csv_buttom.configure(state = WG_DISABLE)        
        
        #画面右側
        #フレーム（外側）を作成
        self.frame_epain = tkinter.Frame(self.root)
        self.frame_epain.grid(row=0, column=1, sticky=tkinter.N)
        #フレーム（ステータス(人数)表示用）を作成
        self.frame_stat = tkinter.Frame(self.frame_epain, width=STAT_CANVAS_W, height=STAT_CANVAS_H)
        self.frame_stat.pack(fill=tkinter.X)
        self.frame_stat.configure(bg=CANVAS_BACK_CLR)
        #キャンバス（グラフ用）を作成
        self.canvas_graph = tkinter.Canvas(self.frame_epain, width=GRAPH_CANVAS_W, height=GRAPH_CANVAS_H)
        self.canvas_graph.pack()
        self.canvas_graph.create_rectangle(0,0,GRAPH_CANVAS_W,GRAPH_CANVAS_H,fill=CANVAS_BACK_CLR)
        self.canvas_graph.update()
        #キャンバス（シミュレーション用）を作成    
        self.canvas_sim = tkinter.Canvas(self.frame_epain, width=SIM_CANVAS_W, height=SIM_CANVAS_H)
        self.canvas_sim.pack()
        self.canvas_sim.create_rectangle(0,0,SIM_CANVAS_W,SIM_CANVAS_H,fill=CANVAS_BACK_CLR)
        self.canvas_sim.update()
        
        #ステータスフレームにテキスト表示
        c_idx=0
        for lb in DSP_TITLES_DIC:
            #項目名表示
            stat_title = tkinter.Label(self.frame_stat, text = lb[0], font=("", "10"), fg=lb[1], bg=lb[2])
            stat_title.grid(row=0,column=c_idx,sticky=tkinter.W + tkinter.E)
            #データ表示(初期表示はスペース)
            svar = tkinter.StringVar()
            svar.set("-")
            slabel = tkinter.Label(self.frame_stat, textvariable = svar, font=("", "12", "bold"), fg=lb[1], bg=lb[2])
            slabel.grid(row=1,column=c_idx,sticky=tkinter.W + tkinter.E)
            self.stat_count.append(svar)
            c_idx += 1
        
        #実行時間計測
        self.tr.buildtime.stop()
        
    def buildsim(self):
        """シミュレーション環境のセットアップ
        
         シミュレーションデータの初期化・セットアップを行う
         (「セットアップボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #実行時間計測
        self.tr.clearsimrec()
        self.tr.buildsimtime.start()
    
        #すべての要素を一度削除
        self.persons.clear()
        #グラフデータのクリア
        self.s_his.clear()
        self.i_n_his.clear()
        self.i_l_his.clear()
        self.i_h_his.clear()
        self.r_his.clear()
        self.d_his.clear()
        self.eco_his.clear()
        #ヒストリーデータのクリア
        self.sim_history = [0,0,0,0,0,0,0,0.0,0.0]
        self.sim_histories.clear()
        #サマリ表示データのクリア
        self.sentences.clear()
    
        #シミュレーション座標と表示キャンバスの比率
        self.disp_exp_rate = SIM_CANVAS_BASE_H / self.up.ups_dic["field_size"].getvl()
        
        #経済活動割合（分母）の再計算 ※経済活動は移動距離の総計で決める
        self.ecoact=self.up.ups_dic["total_persons_count"].getvl()*self.up.ups_dic["move_r"].getvl()
        self.ecoeffect=0.0

        self.jobid=None
        self.now_cycle=0
    
        #初期インスタンスの生成
        total_persons_count =0
        for i in  range(self.up.ups_dic["s_persons_count"].getvl()):
            self.persons.append( Person(id=i) )
        total_persons_count =i+1  #0 origin
    
        for i in  range(self.up.ups_dic["i_persons_count"].getvl()):
            self.persons.append( Person(id=(i+total_persons_count), stat=I_STATE, serious=I_RANK_NON ) )
        total_persons_count +=(i+1)
        
        for i in  range(self.up.ups_dic["r_persons_count"].getvl()):
            self.persons.append( Person(id=(i+total_persons_count), stat=R_STATE ) )
        total_persons_count +=(i+1)
        
        for i in  range(self.up.ups_dic["d_persons_count"].getvl()):
            self.persons.append( Person(id=(i+total_persons_count), stat=D_STATE ) )
        
        #now_cycle==0 は初期表示（初期配置）
        # no,s,i_n,i_l,i_h,r,d,R (最初は無症状の感染者しかいない)
        sim_history_ini = [ "init", \
            self.up.ups_dic["s_persons_count"].getvl(), self.up.ups_dic["i_persons_count"].getvl(), 0,  0,    \
            self.up.ups_dic["r_persons_count"].getvl(), self.up.ups_dic["d_persons_count"].getvl(), 0.0 ,0.0 ]
        
        c_idx=0
        for lb in self.stat_count:
            lb.set(str(sim_history_ini[c_idx]))
            c_idx += 1
    
        #表示のリフレッシュ
        self.canvas_sim.delete("all")
        self.canvas_sim.create_rectangle(0,0,SIM_CANVAS_W,SIM_CANVAS_H,fill=CANVAS_BACK_CLR)
        for p in self.persons:
            p.drow_p(refresh=MODE_REFRESH)
    
        #グラフ表示のクリア(グラフ)
        self.canvas_graph.delete("all")
        self.canvas_graph.create_rectangle(0,0,GRAPH_CANVAS_W,GRAPH_CANVAS_H,fill=CANVAS_BACK_CLR)
        self.canvas_graph.update()

        #実行ボタンは活性化
        self.run_buttom.configure(state = WG_NORMAL)        
        #サマリ表示ボタン・結果保存ボタンは非活性
        self.summry_buttom.configure(state = WG_DISABLE)
        self.save_csv_buttom.configure(state = WG_DISABLE)        

        #実行時間計測
        self.tr.buildsimtime.stop()
        
    def makegraph(self):
        """グラフ作成
        
         シミュレーションの履歴グラフを作成する

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        entries_len = len(self.sim_histories)
        
        if 0 == entries_len:
            return
        x_exp_rate = GRAPH_CANVAS_W/entries_len
        y_exp_rate = GRAPH_CANVAS_H/self.up.ups_dic["total_persons_count"].getvl()
    
        #グラフの生成(座標は原点)
        self.s_his = [0,GRAPH_CANVAS_H]
        self.i_n_his =[0,GRAPH_CANVAS_H]
        self.i_l_his =[0,GRAPH_CANVAS_H]
        self.i_h_his =[0,GRAPH_CANVAS_H]
        self.r_his =[0,GRAPH_CANVAS_H]
        self.d_his =[0,GRAPH_CANVAS_H]
        
        self.eco_his =[0,0]             #%のグラフなので、一番上（１００％）から描く
        
        #履歴を図形化([0]はサイクル番号なので省く)
        #上の方から描く（重ねていく（上から）D→R→S→I(n→l→h)）
        
        for i in range(entries_len):
    
            x_point = (self.sim_histories[i][0])*x_exp_rate
            
            stack_d = sum(self.sim_histories[i][1:7])
            stack_r = sum(self.sim_histories[i][1:6])
            stack_s = sum(self.sim_histories[i][1:5])
            stack_i_n = sum(self.sim_histories[i][2:5])
            stack_i_l = sum(self.sim_histories[i][3:5])
            stack_i_h = self.sim_histories[i][4]
            
            self.d_his.append( x_point )  #x
            self.d_his.append( GRAPH_CANVAS_H-(stack_d*y_exp_rate)) #y
            self.r_his.append( x_point )  #x
            self.r_his.append( GRAPH_CANVAS_H-(stack_r*y_exp_rate)) #y
            self.s_his.append( x_point )  #x
            self.s_his.append( GRAPH_CANVAS_H-(stack_s*y_exp_rate)) #y
            self.i_n_his.append( x_point )  #x
            self.i_n_his.append( GRAPH_CANVAS_H-(stack_i_n*y_exp_rate)) #y
            self.i_l_his.append( x_point )  #x
            self.i_l_his.append( GRAPH_CANVAS_H-(stack_i_l*y_exp_rate)) #y
            self.i_h_his.append( x_point )  #x
            self.i_h_his.append( GRAPH_CANVAS_H-(stack_i_h*y_exp_rate)) #y
            
            self.eco_his.append( x_point )  #x
            self.eco_his.append( GRAPH_CANVAS_H-(self.sim_histories[i][8]*GRAPH_CANVAS_H/100) ) #y
        
        #終端処理用
        self.d_his.append(x_point)
        self.d_his.append(GRAPH_CANVAS_H)
        self.r_his.append(x_point)
        self.r_his.append(GRAPH_CANVAS_H)
        self.s_his.append(x_point)
        self.s_his.append(GRAPH_CANVAS_H)
        self.i_n_his.append(x_point)
        self.i_n_his.append(GRAPH_CANVAS_H)
        self.i_l_his.append(x_point)
        self.i_l_his.append(GRAPH_CANVAS_H)
        self.i_h_his.append(x_point)
        self.i_h_his.append(GRAPH_CANVAS_H)
       
        self.canvas_graph.create_polygon(self.d_his,fill=PERSON_D_CLR)
        self.canvas_graph.create_polygon(self.r_his,fill=PERSON_R_CLR)
        self.canvas_graph.create_polygon(self.s_his,fill=PERSON_S_CLR)
        self.canvas_graph.create_polygon(self.i_n_his,fill=PERSON_I_N_CLR)
        self.canvas_graph.create_polygon(self.i_l_his,fill=PERSON_I_L_CLR)
        self.canvas_graph.create_polygon(self.i_h_his,fill=PERSON_I_H_CLR)

        #経済活動（折れ線）グラフで描く
        self.canvas_graph.create_line(self.eco_his,fill=PERSON_ECO_CLR, width=2)

    def run_cycle(self):
        """シミュレーション実行
        
         シミュレーションを１サイクル分実行する
         一時停止中でなければ、自分自身で、次の実行をスケジュールする

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        if self.run_mode == CYC_PAUSE:
            return

        #移動
        #実行時間計測
        self.tr.movetime.reset()
        self.tr.movetime.start()

        for i in self.persons:
            i.move()
    
        #実行時間計測
        self.tr.movetime.stop()
        self.tr.addmovetime(self.tr.movetime.getelapsedtime())

        #判定＋表示
        #実行時間計測
        self.tr.renewtime.reset()
        self.tr.renewtime.start()

        self.ecoeffect=0.0
        for i in self.persons:
            i.stat_renew()
    
            #件数カウント
            # no,s,i_n,i_l,i_h,r,d,R
            self.sim_history[0] = self.now_cycle
            if i.stat == S_STATE:
                self.sim_history[1] += 1
            elif i.stat == I_STATE:
                if i.serious == I_RANK_NON:
                    self.sim_history[2] += 1
                elif i.serious == I_RANK_LOW:
                    self.sim_history[3] += 1
                else:       # I_RANK_HIGH
                    self.sim_history[4] += 1
            elif i.stat == R_STATE:
                self.sim_history[5] += 1
            else:           # D_STATE
                self.sim_history[6] += 1
                
            self.ecoeffect += i.r

        #実行再生産数：直近の免疫獲得サイクルので計測
        if self.now_cycle > 0 :
            bf_his = self.sim_histories[self.now_cycle-1]
            bf_his_i = sum(bf_his[2:5])
            now_i = sum(self.sim_history[2:5])
            
            if bf_his_i > 1 and now_i > 0:
                self.sim_history[7] =round( math.log(now_i,bf_his_i),4)
            else:
                self.sim_history[7] = 0.0

                       
        #経済活動割合
        self.sim_history[8] = round(self.ecoeffect/ self.ecoact*100,2)

        #実行時間計測
        self.tr.renewtime.stop()
        self.tr.addrenewtime(self.tr.renewtime.getelapsedtime())

        #実行時間計測
        self.tr.drawtime.reset()
        self.tr.drawtime.start()

        #表示のリフレッシュ
        if self.nodsp_checkbv.get():
            pass
        else:
            for p in self.persons:
                p.drow_p(refresh=MODE_MOVE)
        
    
        #ヒストリーに追加
        self.sim_histories.append(self.sim_history) 
        
        #テキスト表示
        c_idx=0
        for lb in self.stat_count:
            lb.set(str(self.sim_history[c_idx]))
            c_idx += 1
        
        #表示のリフレッシュ(グラフ)
        if self.nodsp_checkbv.get():
            pass
        else:
            self.canvas_graph.delete("all")
            self.canvas_graph.create_rectangle(0,0,GRAPH_CANVAS_W,GRAPH_CANVAS_H,fill=CANVAS_BACK_CLR)
            self.makegraph()
            self.canvas_graph.update()
        
    
        #実行時間計測
        self.tr.drawtime.stop()
        self.tr.adddrawtime(self.tr.drawtime.getelapsedtime())

        #終了判定
        if self.now_cycle > (self.up.ups_dic["cycle_max"].getvl()) or 0 == (sum(self.sim_history[2:5])):
            if self.jobid is not None:
                self.root.after_cancel(self.jobid)
                self.jobId=None
                self.terminat()
        else:
            #次のサイクル
            self.now_cycle += 1
            #カウンタクリア
            self.sim_history = [0,0,0,0,0,0,0,0.0,0.0]
            self.jobid=self.root.after(self.up.ups_dic["cycle_speed"].getvl(),self.run_cycle)
        
    def runsim(self):
        """シミュレーション開始
        
         シミュレーションを開始（キック）する
         (「実行ボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #実行時間計測
        self.tr.allsimtime.start()

        #実行ボタンは非活性化
        self.run_buttom.configure(state = WG_DISABLE)        
        #ロードボタン・セーブボタン・初期値ボタン・セットアップボタンは非活性
        self.load_json_buttom.configure(state = WG_DISABLE)
        self.save_json_buttom.configure(state = WG_DISABLE)
        self.set_default_buttom.configure(state = WG_DISABLE)
        self.setup_buttom.configure(state = WG_DISABLE)
        #パラメータ入力エリアも非活性
        for key in self.ent_dic.keys():
            self.ent_dic[key].entry.configure(state = WG_DISABLE)
        #画面更新モードチェックボタンも非活性
        self.nodsp_check.configure(state = WG_DISABLE)
        #一時停止ボタンは活性
        self.pause_buttom.configure(state = WG_NORMAL) 
        
        self.run_mode=CYC_RUN
       
    
        self.run_cycle()

    def hist_summry(self):
        """サマリ作成
        
         ヒストリーを集計してサマリを作成する。
         サマリはサマリ表示用リストに格納する。

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #表示
        self.sentences.append("画面初期構築時間(ms)={}".format(self.tr.buildtime.getelapsedtime()))
        self.sentences.append("シミュレーションセットアップ時間(ms)={}".format(self.tr.buildsimtime.getelapsedtime()))
        self.sentences.append("シミュレーション総実行時間(ms)={}".format(self.tr.allsimtime.getelapsedtime()))
        self.sentences.append("　移動実行時間(ms)={}".format(self.tr.allmovetime))
        self.sentences.append("　判定実行時間(ms)={}".format(self.tr.allrenewtime))
        self.sentences.append("　画面描写時間(ms)={}".format(self.tr.alldrawtime))
        self.sentences.append("-"*50)

        #人数カウント
        all_stat_lst = [p.stat for p in self.persons]
        s_cnt=all_stat_lst.count(S_STATE)
        r_cnt=all_stat_lst.count(R_STATE)
        d_cnt=all_stat_lst.count(D_STATE)
        i_cnt=r_cnt+d_cnt
        all_seri_lst = [p.serious for p in self.persons]
        i_n_cnt=all_seri_lst.count(I_RANK_NON)
        i_l_cnt=all_seri_lst.count(I_RANK_LOW)
        i_h_cnt=all_seri_lst.count(I_RANK_HIGH)
    
        self.sentences.append("収束までのサイクル={}".format(self.now_cycle))    
        self.sentences.append("非感染者人数={} 非感染率(対人口)={}%".format(s_cnt,round(s_cnt/self.up.ups_dic["total_persons_count"].getvl()*100,2)))
        self.sentences.append("回復者人数={} 回復率(対感染者)={}%".format(r_cnt,round(r_cnt/i_cnt*100,2)))
        self.sentences.append("死亡者人数={} 死亡率(対人口)={}%".format(d_cnt,round(d_cnt/self.up.ups_dic["total_persons_count"].getvl()*100,2)))
        self.sentences.append("死亡者人数={} 死亡率(対感染者)={}%".format(d_cnt,round(d_cnt/i_cnt*100,2)))
        self.sentences.append("症状なし人数={} 発生率(対感染者)={}%".format(i_n_cnt,round(i_n_cnt/i_cnt*100,2)))
        self.sentences.append("軽症人数={} 発生率(対感染者)={}%".format(i_l_cnt,round(i_l_cnt/i_cnt*100,2)))
        self.sentences.append("重症人数={} 発生率(対感染者)={}%".format(i_h_cnt,round(i_h_cnt/i_cnt*100,2)))

        #ピーク時感染者数（合計）・感染者数（軽症＋重症）
        max_i_lst = [(sum(i[2:5]),i[0]) for i in self.sim_histories]
        max_i = max(max_i_lst)
        self.sentences.append("ピーク時感染者(合計)：サイクル={} 人数={}".format(max_i[1],max_i[0]))
        max_i_lh_lst = [(sum(i[3:5]),i[0]) for i in self.sim_histories]
        max_i_lh = max(max_i_lh_lst)
        self.sentences.append("ピーク時感染者(軽症＋重症)：サイクル={} 人数={}".format(max_i_lh[1],max_i_lh[0]))

        #最大経済影響・平均経済影響
        min_eco_lst = [(i[8],i[0]) for i in self.sim_histories]
        min_eco = min(min_eco_lst)
        self.sentences.append("最大経済影響：サイクル={} 割合={}%".format(min_eco[1],min_eco[0]))
        avr_eco = sum( i[8] for i in self.sim_histories )/len(self.sim_histories)
        self.sentences.append("平均経済影響：{}%".format(round(avr_eco,2)))

    def terminat(self):
        """シミュレーション終了処理
        
         シミュレーション終了時にサマリを作成し、ウインドウ表示する

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #実行時間計測
        self.tr.allsimtime.stop()
        
        self.hist_summry()
        self.dispsummry()
       
        #ロードボタン・セーブボタン・初期値ボタン・セットアップボタン・サマリ表示ボタンは活性
        self.load_json_buttom.configure(state = WG_NORMAL)
        self.save_json_buttom.configure(state = WG_NORMAL)
        self.set_default_buttom.configure(state = WG_NORMAL)
        self.setup_buttom.configure(state = WG_NORMAL)
        self.summry_buttom.configure(state = WG_NORMAL)  
        self.save_csv_buttom.configure(state = WG_NORMAL)
        #画面更新モードチェックボタンも非活性
        self.nodsp_check.configure(state = WG_NORMAL)

        #パラメータ入力エリアも活性
        for key in self.ent_dic.keys():
            self.ent_dic[key].entry.configure(state = WG_NORMAL)
        #一時停止ボタンは非活性
        self.pause_buttom.configure(state = WG_DISABLE)     
            
    def pause(self):
        """シミュレーション一時停止
        
         シミュレーションを一時停止する
         (「一時停止ボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #サイクルスレッドの一時停止
        self.run_mode=CYC_PAUSE
        self.jobid=None

        #パラメータ入力エリアも活性
        self.ent_dic["s_move_limit_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["i_n_move_limit_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["i_l_move_limit_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["i_h_move_limit_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["r_move_limit_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["s_move_disable_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["i_n_move_disable_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["i_l_move_disable_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["i_h_move_disable_rate"].entry.configure(state = WG_NORMAL)
        self.ent_dic["r_move_disable_rate"].entry.configure(state = WG_NORMAL)
        #一時停止ボタンは非活性
        self.pause_buttom.configure(state = WG_DISABLE)
        #再開ボタンは活性
        self.restart_buttom.configure(state = WG_NORMAL) 
        
    def restart(self):
        """シミュレーション再開
        
         シミュレーションを再開する
         (「再開ボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        #パラメータ入力エリアも非活性
        self.ent_dic["s_move_limit_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["i_n_move_limit_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["i_l_move_limit_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["i_h_move_limit_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["r_move_limit_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["s_move_disable_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["i_n_move_disable_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["i_l_move_disable_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["i_h_move_disable_rate"].entry.configure(state = WG_DISABLE)
        self.ent_dic["r_move_disable_rate"].entry.configure(state = WG_DISABLE)
        #一時停止ボタンは活性
        self.pause_buttom.configure(state = WG_NORMAL)
        #再開ボタンは非活性
        self.restart_buttom.configure(state = WG_DISABLE)     

        #サイクルスレッド再開
        self.run_mode=CYC_RUN
        self.jobid=self.root.after(self.up.ups_dic["cycle_speed"].getvl(),self.run_cycle)

    def dispsummry(self):
        """サマリウインドウの表示
        
         サマリウインドウを表示する
         (「サマリ表示ボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        ResultSummry(self.sentences)
        
    def savehistory(self):
        """シミュレーション結果保存
        
         シミュレーション結果をファイル(csv)に保存する
         (「結果保存ボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        # ファイル選択ダイアログの表示
        fTyp = [("CSVファイル", "*.csv")]
        out_f = tkinter.filedialog.asksaveasfilename(filetypes = fTyp, title='保存ファイル（csv）を選択してくだい。')
        
        #キャンセルが押された
        if 0 == len(out_f):
            return False
        
        csv_title = [titles[0] for titles in DSP_TITLES_DIC]
        a = open(out_f, "w")
        csvout = csv.writer(a)
        csvout.writerow(csv_title)
        csvout.writerows(self.sim_histories)
        a.close()
        
        return True

    def help(self):
        """ヘルプウインドウ表示
        
         ヘルプウインドウを表示する
         (「ヘルプボタン」押下時の処理)

        Args:なし
        Returns:なし
        Raises:なし
        Yields:なし
        Examples:なし
        Note:なし
        """
        HelpWindow()
        
#ここからメインロジック##################################

main=MainApp()
main.root.mainloop()
