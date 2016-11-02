from flask import render_template, flash, redirect, url_for, request,json
from App import app

from .forms import Emuform
from flask_table import Table, Col
import pandas as pd
import numpy as np

# csv読み込み
data = pd.read_csv("App/static/data/test_data.csv")
data["合計"] =data.iloc[:,3:].apply(sum, axis=1)
sougouunivs = ["東北","慶應義塾","早稲田","明海","日大","中央","法政","同志社","京都","関西学院","関西","広島","九州"]
# 470個人
data470 = data.ix[data["クラス"]=="470",:]
del data470["クラス"]
# スナイプ個人
datasnipe = data.ix[data["クラス"]=="snipe",:]
del datasnipe["クラス"]
# 470団体
team470 = data470.groupby("大学名")[["race"+str(x) for x in range(1,12)]].sum()
team470["合計"] = team470.apply(sum, axis=1)
team470 = team470.sort_values("合計")
team470["大学名"] = team470.index
# スナイプ団体
teamsnipe = datasnipe.groupby("大学名")[["race"+str(x) for x in range(1,12)]].sum()
teamsnipe["合計"] = teamsnipe.apply(sum, axis=1)
teamsnipe = teamsnipe.sort_values("合計")
teamsnipe["大学名"] = teamsnipe.index
# 総合
teamsg = data.ix[[y in sougouunivs for y in data["大学名"]],: ].groupby("大学名")[["race"+str(x) for x in range(1,12)]].sum()
teamsg_cp = teamsg.copy()
teamsg["合計"] = teamsg.apply(sum, axis=1)
teamsg_goukei_cp = teamsg["合計"].to_dict()
teamsg = teamsg.sort_values("合計")
teamsg["大学名"] = teamsg.index

#総合累積
teamsg_cp  = teamsg_cp.replace(0,np.nan) # 0の列は削除
teamsg_cp =  teamsg_cp.dropna(axis=1)
teamsg_ruiseki = teamsg_cp.apply(np.cumsum,axis=1)
ruiseki = pd.concat([pd.DataFrame(teamsg_ruiseki.index), teamsg_ruiseki.reset_index(drop=True)], axis=1)
ruiseki_lists = [list(x) for  x in np.array(ruiseki)]
# Declare your table
class ItemTable(Table):
    classes = ['table-bordered',"text-center"]
    univname = Col('大学名')
    team = Col('艇')
    R1 = Col('R1')
    R2 = Col('R2')
    R3 = Col('R3')
    R4 = Col('R4')
    R5 = Col('R5')
    R6 = Col('R6')
    R7 = Col('R7')
    R8 = Col('R8')
    R9 = Col('R9')
    R10 = Col('R10')
    R11 = Col('R11')
    score = Col('計')

# Get some objects
class Item(object):
    def __init__(self, univname, team, race1,race2,race3,race4,race5,race6,race7,race8,race9,race10,race11,score):
        self.univname = univname
        self.team = team
        self.R1 = race1
        self.R2 = race2
        self.R3 = race3
        self.R4 = race4
        self.R5 = race5
        self.R6 = race6
        self.R7 = race7
        self.R8 = race8
        self.R9 = race9
        self.R10 = race10
        self.R11 = race11
        self.score = score

class ItemTableTeam(Table):
    classes = ['table-bordered',"text-center"]
    univname = Col('大学名')
    R1 = Col('R1')
    R2 = Col('R2')
    R3 = Col('R3')
    R4 = Col('R4')
    R5 = Col('R5')
    R6 = Col('R6')
    R7 = Col('R7')
    R8 = Col('R8')
    R9 = Col('R9')
    R10 = Col('R10')
    R11 = Col('R11')
    score = Col('合計')

# Get some objects
class ItemTeam(object):
    def __init__(self, race1,race2,race3,race4,race5,race6,race7,race8,race9,race10,race11,score,univname):
        self.univname = univname
        self.R1 = race1
        self.R2 = race2
        self.R3 = race3
        self.R4 = race4
        self.R5 = race5
        self.R6 = race6
        self.R7 = race7
        self.R8 = race8
        self.R9 = race9
        self.R10 = race10
        self.R11 = race11
        self.score = score

items470 = [Item(*row) for key, row, in  data470.iterrows()]
itemssnipe = [Item(*row) for key, row, in  datasnipe.iterrows()]
itemsteam470 = [ItemTeam(*row) for key, row, in  team470.iterrows()]
itemsteamsnipe = [ItemTeam(*row) for key, row, in  teamsnipe.iterrows()]
itemsteamsg = [ItemTeam(*row) for key, row, in  teamsg.iterrows()]

# Populate the table
table470 = ItemTable(items470)
tablesnipe = ItemTable(itemssnipe)
tableteam470 = ItemTableTeam(itemsteam470)
tableteamsnipe = ItemTableTeam(itemsteamsnipe)
tableteamsg = ItemTableTeam(itemsteamsg)

xticks = ["x"]
for x in range(1,len(ruiseki_lists[0])):
    xticks.append(x)
ruiseki_lists.insert(0, xticks)

@app.route('/')
def hello_world():
    return render_template("index.html",
                            table470 = table470,
                            tablesnipe =  tablesnipe,
                            tableteam470 = tableteam470,
                            tableteamsnipe = tableteamsnipe,
                            tableteamsg = tableteamsg,
                            ruiseki_lists = json.dumps(ruiseki_lists)
                            )
@app.route('/emurator', methods=['GET', 'POST'])
def emu():
    form = Emuform()
    print(request.method,form.validate())
    if request.method == 'POST'  and form.validate():
        tohoku = teamsg_goukei_cp["東北"] + form.tohoku1.data + form.tohoku2.data
        keio = teamsg_goukei_cp["慶應義塾"] + form.keio1.data + form.keio2.data
        waseda = teamsg_goukei_cp["早稲田"] + form.waseda1.data + form.waseda2.data
        meikai = teamsg_goukei_cp["明海"] + form.meikai1.data + form.meikai2.data
        nihon = teamsg_goukei_cp["日大"] + form.nihon1.data + form.nihon2.data
        tyuou = teamsg_goukei_cp["中央"] + form.tyuou1.data + form.tyuou2.data
        hosei = teamsg_goukei_cp["法政"] + form.hosei1.data + form.hosei2.data
        dosisha = teamsg_goukei_cp["同志社"] + form.dosisha1.data + form.dosisha1.data
        kyoto = teamsg_goukei_cp["京都"] + form.kyoto1.data + form.kyoto2.data
        kwansei = teamsg_goukei_cp["関西学院"] + form.kwansei1.data + form.kwansei2.data
        kansai = teamsg_goukei_cp["関西"] + form.kansai1.data + form.kansai2.data
        hirosima = teamsg_goukei_cp["広島"] + form.hirosima1.data + form.hirosima2.data
        kyushu = teamsg_goukei_cp["九州"] + form.kyushu1.data + form.kyushu2.data
        flash("tohoku:{tohoku},keio:{keio},waseda:{waseda},meikai:{meiai},nihon:{nihon},tyuou:{tyuou},hosei:{hosei},dosisha:{dosisha},kyoto:{kyoto},kwansei:{kwansei},kansai:{kansai},hirosima:{hirosima},kyushu:{kyushu}"
            .format(tohoku=tohoku,
                            keio=keio,
                            waseda=waseda,
                            meikai=meikai,
                            nihon=nihon,
                            tyuou=tyuou,
                            hosei=hosei,
                            dosisha=dosisha,
                            kyoto=kyoto,
                            kwansei=kwansei,
                            kansai=kansai,
                            hirosima=hirosima,
                            kyushu=kyushu
                            ))
        return redirect(url_for('register'))

    return render_template("emurator.html",
                            form = form,
                            tohokunow = teamsg_goukei_cp["東北"],
                            keionow = teamsg_goukei_cp["慶應義塾"],
                            wasedanow = teamsg_goukei_cp["早稲田"],
                            meikainow = teamsg_goukei_cp["明海"],
                            nihonnow = teamsg_goukei_cp["日大"],
                            tyuounow = teamsg_goukei_cp["中央"],
                            hoseinow = teamsg_goukei_cp["法政"],
                            dosishanow = teamsg_goukei_cp["同志社"],
                            kyotonow = teamsg_goukei_cp["京都"],
                            kwanseinow = teamsg_goukei_cp["関西学院"],
                            kansainow = teamsg_goukei_cp["関西"],
                            hirosimanow = teamsg_goukei_cp["広島"],
                            kyushunow = teamsg_goukei_cp["九州"],
                            )

