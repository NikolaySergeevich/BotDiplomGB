import data_frame as wor
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter
import text as t
from sqlyghter import Sqloghter

db = Sqloghter()

def plt_result(us_id):
    N = 15
    df = wor.get_data_frame(us_id)
    r = np.array(wor.get_data_frame_only_value(df))
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    width = np.array([0.42] * N)
    title = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    sum_bals = wor.get_sum_data(df)

    plt.figure(figsize=(12,10), facecolor='#f9f9ff')
    ax = plt.subplot(111, polar=True)

    plt.text(-1, -1, sum_bals, size = 40, horizontalalignment='center',
        verticalalignment='center', color = '#500805')
    ax.set_rticks(np.arange(1, 6, 1))
    ax.set_rorigin(-1)
    ax.set_thetagrids(theta * 180 / np.pi, title)
    ax.grid(color ="black", linewidth=3)
    ax.set_rlim(0)
    ax.yaxis.set_major_formatter(NullFormatter())

    db.update_degry_whis_dinamic_reqest(us_id, 'sum_general_bals', sum_bals)
    db.commit() 
   
    ycoord = 0.45
    for num in 1,2,3,4,5:
        xcoord = 0.20943951
        ygol = -85
        i = 0
        while i != N:
            plt.text(xcoord, ycoord, num, rotation=ygol, size=13, horizontalalignment='center', verticalalignment='center', alpha=0.5)
            xcoord += 0.41887902
            ygol += 24.8
            i += 1
        ycoord +=1
        
    ycoord = 0.20943951
    for lab in t.get_list_whis_title_on_russian():
        xcoord = 6.3
        plt.text(ycoord, xcoord, lab, size=9, horizontalalignment='center', verticalalignment='center', weight='medium', family='serif')
        ycoord += 0.41887902

    bars_user = ax.bar(x=theta, height=r-.0, width=width, bottom=0, alpha=0.7, tick_label=title, align='edge')
    
    for rr, bar in zip(r, bars_user):
        if rr == 1: color = '#505160' 
        if rr == 2: color = '#6a71' 
        if rr == 3: color = '#68829e' 
        if rr == 4: color = '#aebd38' 
        if rr == 5: color = '#598234' 
        bar.set_facecolor(color)
    way = t.get_way_of_img(us_id)
    plt.savefig(way)

def create_5_pl_compare(us_id):
    N = 15
    df = wor.get_data_frame(us_id)
    r = np.array(wor.get_data_frame_only_value(df))
    theta = np.linspace(0.0, 2 * np.pi, N, endpoint=False)
    width = np.array([0.42] * N)
    title = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    
    for name, name_compare in zip(t.name_specific, t.name_compare_specific):
        plt.figure(figsize=(12,10), facecolor='#f9f9ff')
        ax = plt.subplot(111, polar=True)

        ax.set_rticks(np.arange(1, 6, 1))
        ax.set_rorigin(-1)
        ax.set_thetagrids(theta * 180 / np.pi, title)
        ax.grid(color ="black", linewidth=3)
        ax.set_rlim(0)
        ax.yaxis.set_major_formatter(NullFormatter())

    # --------------------Заполнение окружности по уровням 
        ycoord = 0.45
        for num in 1,2,3,4,5:
            xcoord = 0.20943951
            ygol = -85
            i = 0
            while i != N:
                plt.text(xcoord, ycoord, num, rotation=ygol, size=13, horizontalalignment='center', verticalalignment='center', alpha=0.5)
                xcoord += 0.41887902
                ygol += 24.8
                i += 1
            ycoord +=1
        
    #------------заполнение качеств по окружности
        ycoord = 0.20943951
        for lab in t.get_list_whis_title_on_russian():
            xcoord = 6.3
            plt.text(ycoord, xcoord, lab, size=9, horizontalalignment='center', verticalalignment='center', weight='medium', family='serif')
            ycoord += 0.41887902

        bars_user = ax.bar(x=theta, height=r-.0, width=width, bottom=0, alpha=0.7, tick_label=title, align='edge')
        df_const = wor.get_data_frame(name)
        r_cons = np.array(wor.get_data_frame_only_value(df_const))
        bar_cons = ax.bar(x=theta, height=r_cons-.0, width=width, bottom=0, alpha=0.7, tick_label=title, align='edge')
        
        color_green = '#2e8b57'#зелёный
        color_red = '#cc0605'#красный
        color_wite = '#ffffff'#белый
        bals = 0
        for r_user, r_cons, bar_user, bar_cons in zip (r, r_cons, bars_user, bar_cons):
            bar_user.set_facecolor(color_wite)
            bar_cons.set_facecolor(color_wite)
            if r_user > r_cons and r_cons > 0:
                bar_cons.set_facecolor(color_red)
                bar_user.set_facecolor(color_green)
                bals += r_user
            elif r_user == r_cons:
                bar_cons.set_facecolor(color_green)
                bar_user.set_facecolor(color_wite)
                bals += r_user
            elif r_user < r_cons:
                bar_cons.set_facecolor(color_red)
                bar_user.set_facecolor(color_green)
            elif r_cons == 0:
                bar_user.set_facecolor(color_red)
        plt.text(-1, -1, bals, size = 40, horizontalalignment='center',
            verticalalignment='center', color = '#500805')
        db.update_degry_whis_dinamic_reqest(us_id, name_compare, bals)
        db.commit()
        
        way = t.get_way_of_img_compare(us_id, name)
        plt.savefig(way)
