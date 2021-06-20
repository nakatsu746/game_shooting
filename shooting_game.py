import pygame
import sys
import math
import random

# ******************** 色の定義 ********************
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
SILVER = (192, 208, 224)
CYAN = (0, 224, 255)

# ******************** 画像の読み込み ********************
img_player = pygame.image.load("image/player.png")
img_enemy = [
    pygame.image.load("image/enemy_0.png"), # 弾：直線タイプ／破壊不可
    pygame.image.load("image/enemy_1.png"), # 弾：直線タイプ／破壊可
    pygame.image.load("image/enemy_2.png"), # 弾：追尾タイプ
    pygame.image.load("image/enemy_3.png"), # 敵：BOSS(無敵状態)
    pygame.image.load("image/enemy_4.png"), # 敵：BOSS(無敵状態)
    pygame.image.load("image/enemy_5.png"), # 敵：BOSS
    pygame.image.load("image/enemy_6.png"), # 敵：設置タイプ
    pygame.image.load("image/enemy_7.png"), # 敵：追尾タイプ
    pygame.image.load("image/enemy_8.png")  # 敵：追尾タイプ
    
]
img_block = [
    pygame.image.load("image/block_0.png"), # 破壊不可
    pygame.image.load("image/block_1.png"), # 破壊不可／ダメージあり
    pygame.image.load("image/block_2.png")  # 破壊可
]
img_explode = [
    None,
    pygame.image.load("image/explode_1.png"),
    pygame.image.load("image/explode_2.png"),
    pygame.image.load("image/explode_3.png"),
    pygame.image.load("image/explode_4.png"),
    pygame.image.load("image/explode_5.png"),
    pygame.image.load("image/explode_6.png"),
    pygame.image.load("image/explode_7.png"),
    pygame.image.load("image/explode_8.png"),
    pygame.image.load("image/explode_9.png"),
    pygame.image.load("image/explode_10.png")
]
img_weapon = pygame.image.load("image/weapon_0.png")
img_title = pygame.image.load("image/title.png")

# ******************** 変数／定数の宣言 ********************
idx = 0
tmr = 0

FIELD_SIZE = 960
SCREEN_SIZE = 960
HALF_SCREEN_SIZE = int(SCREEN_SIZE/2)
PIXEL_SIZE = 80
HALF_PIXEL_SIZE = int(PIXEL_SIZE/2)
# フィールドの領域
LINE_T = 0 + HALF_PIXEL_SIZE
LINE_B = FIELD_SIZE - HALF_PIXEL_SIZE
LINE_L = 0 + HALF_PIXEL_SIZE
LINE_R = FIELD_SIZE - HALF_PIXEL_SIZE
# 移動方向
DIR_UP = 0
DIR_DOWN = 1
DIR_LEFT = 2
DIR_RIGHT = 3

# =============== PLAYER ===============
# プレイヤー
pl_x = 0                    # x座標(機体の中心)
pl_y = 0                    # y座標(機体の中心)
pl_a = 0                    # 角度
pl_d = 0                    # 移動方向(キー入力)
pl_s = 20                   # 移動スピード
pl_shield = 3               # シールド(体力)
pl_muteki = 0               # 無敵状態(時間)
click_1 = 0
# 弾(プレイヤー)
MISSILE_MAX = 200           # 弾の最大数
msl_no = 0                  # 弾の配列の添字
msl_f = [False]*MISSILE_MAX # 弾が存在するか
msl_x = [0]*MISSILE_MAX     # x座標(弾の中心)
msl_y = [0]*MISSILE_MAX     # y座標(弾の中心)
msl_a = [0]*MISSILE_MAX     # 角度
msl_p = [0]*MISSILE_MAX     # 弾の移動範囲

# =============== ENEMY ===============
# 敵
ENEMY_MAX = 1000            # 敵の最大数
emy_no = 0                  # 敵の配列の添字
emy_f = [False]*ENEMY_MAX   # 敵が存在するか
emy_x = [0]*ENEMY_MAX       # x座標(敵の中心)
emy_y = [0]*ENEMY_MAX       # y座標(敵の中心)
emy_a = [0]*ENEMY_MAX       # 角度
emy_type = [0]*ENEMY_MAX    # 敵のタイプ
emy_speed = [0]*ENEMY_MAX   # 移動スピード
emy_shield = [0]*ENEMY_MAX  # シールド(体力)
# 敵のタイプ
BOSS_MUTEKI = 3
muteki = 0
BOSS = 5
EMY_FIXED = 6
EMY_TRACKING_0 = 7
EMY_TRACKING_1 = 8
# 敵の移動スピード
BOSS_SPEED = 1
EMY_SPEED_0 = 0
EMY_LOW_SPEED = 2
EMY_NORMAL_SPEED = 6
EMY_HIGH_SPEED = 10
# 敵のシールド
EMY_SHIELD = 5
BOSS_SHIELD = 30
# =============== ENEMY(BULLET) ===============
# 弾(敵)
EFFECT_MAX = 100            # 爆発の最大数
eff_no = 0                  # 爆発の配列の添字
eff_p = [0]*EFFECT_MAX      # 爆発のエフェクトの進行管理
eff_x = [0]*EFFECT_MAX      # x座標(爆発の中心)
eff_y = [0]*EFFECT_MAX      # y座標(爆発の中心)
# 弾のタイプ
BUL_STRAIGHT_0 = 0
BUL_STRAIGHT_1 = 1
BUL_TRACKING = 2
# 弾のスピード
BUL_LOW_SPEED = 4
BUL_NORMAL_SPEED = 8
BUL_HIGH_SPEED = 12
# 弾のシールド
BUL_SHIELD_1 = 1
BUL_SHIELD_3 = 3
# 弾の打つ種類
SINGLE_SHOT = 1
FOUR_SHOT = 2
CIRCLE_SHOT = 3
RANDOM_SHOT = 4

# =============== BLOCK ===============
# ブロック
BLOCK_MAX = 50              # ブロックの最大数
block_no = 0                # ブロックの配列の添字
block_f = [False]*BLOCK_MAX # ブロックが存在するか
block_x = [0]*BLOCK_MAX     # x座標(ブロックの中心)
block_y = [0]*BLOCK_MAX     # y座標(ブロックの中心)
block_type = [0]*BLOCK_MAX  # ブロックのタイプ
block_b = [0]*BLOCK_MAX     # ブロックが黒色の場合、破壊可能(弾に当たった回数をカウント)
block_d = [False]*BLOCK_MAX # ブロックが黒色の場合、弾が当たった時に点滅する
# ブロックの種類
WHITE_BLOCK = 0
RED_BLOCK = 1
BLACK_BLOCK = 2

course_clear = False

# ============================================================
#                       TEXT / CALC
# ============================================================

# ******************** 立体的な文字の表示 ********************
def draw_text(sc, txt, x, y, siz, col):
    fnt = pygame.font.Font(None, siz)
    cr = int(col[0]/2)
    cg = int(col[1]/2)
    cb = int(col[2]/2)
    sur = fnt.render(txt, True, (cr,cg,cb))
    
    x = x - sur.get_width()/2
    y = y - sur.get_height()/2
    sc.blit(sur, [x+1, y+1])

    cr = col[0] + 128
    if cr > 255: cr = 255
    cg = col[1] + 128
    if cg > 255: cg = 255
    cb = col[2] + 128
    if cb > 255: cb = 255

    sur = fnt.render(txt, True, (cr,cg,cb))
    sc.blit(sur, [x-1, y-1])

    sur = fnt.render(txt, True, col)
    sc.blit(sur, [x, y])


# ******************** 2点間の距離を求める ********************
def get_dis(x1, y1, x2, y2):
    return ( (x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) )


# ============================================================
#                         PLAYER
# ============================================================

# ******************** プレイヤーの移動 ********************
def move_player(sc, key):
    global idx, tmr
    global pl_x, pl_y, pl_a, pl_d, pl_s, pl_shield, pl_muteki, click_1
    
    if key[pygame.K_w] == 1: # 上方向
        pl_d = DIR_UP
        if check_block(pl_x, pl_y, pl_d, pl_s, False) == False:
            pl_y = pl_y - pl_s
            if pl_y < LINE_T:
                pl_y = LINE_T
    if key[pygame.K_s] == 1: # 下方向
        pl_d = DIR_DOWN
        if check_block(pl_x, pl_y, pl_d, pl_s, False) == False:
            pl_y = pl_y + pl_s
            if pl_y > LINE_B:
                pl_y = LINE_B
    if key[pygame.K_a] == 1: # 左方向
        pl_d = DIR_LEFT
        if check_block(pl_x, pl_y, pl_d, pl_s, False) == False:
            pl_x = pl_x - pl_s
            if pl_x < LINE_L:
                pl_x = LINE_L
    if key[pygame.K_d] == 1: # 右方向
        pl_d = DIR_RIGHT
        if check_block(pl_x, pl_y, pl_d, pl_s, False) == False:
            pl_x = pl_x + pl_s
            if pl_x > LINE_R:
                pl_x = LINE_R
    
    # マウスのx座標とy座標 -> プレイヤーとマウスの座標の距離 -> 角度の算出
    mouseX, mouseY = pygame.mouse.get_pos()
    x_dis = mouseX - pl_x
    y_dis = mouseY - pl_y
    pl_a = math.degrees(math.atan2(y_dis, x_dis))
    # 回転させた画像
    img_rz = pygame.transform.rotozoom(img_player, -90-pl_a, 1.0)

    # マウス入力
    mBtn_1, mBtn_2, mBtn_3 = pygame.mouse.get_pressed()
    # 弾を発射するか
    click_1 = (click_1+1) * mBtn_1
    if click_1%3 == 1:
        set_missile()
    # プレイヤーの機体を描く(点滅)
    if pl_muteki%2 == 0:
        sc.blit(img_rz, [pl_x-img_rz.get_width()/2, pl_y-img_rz.get_height()/2])
    # 無敵状態の時はダメージを受けない
    if pl_muteki > 0:
        pl_muteki -= 1
        return

    # 敵と弾のヒットチェック
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            w = img_enemy[emy_type[i]].get_width()
            h = img_enemy[emy_type[i]].get_height()
            r = int((w+h)/4 + (80+80)/4)
            # ヒットチェック
            if get_dis(emy_x[i], emy_y[i], pl_x, pl_y) < r*r:
                set_effect(pl_x, pl_y, False)
                pl_shield -= 1
                # シールドが0の場合はゲームオーバー
                if pl_shield <= 0:
                    pl_shield = 0
                    idx = -2
                    tmr = 0
                # 無敵状態を設定
                if pl_muteki == 0:
                    pl_muteki = 60
                # 接触した敵のシールドを減らす
                emy_shield[i] -= 1
                break


# ******************** プレイヤーの発射する弾をセット ********************
def set_missile():
    global msl_no, msl_f, msl_x, msl_y, msl_a, msl_p

    msl_f[msl_no] = True
    msl_x[msl_no] = pl_x
    msl_y[msl_no] = pl_y
    msl_a[msl_no] = pl_a
    msl_p[msl_no] = 0
    msl_no = (msl_no+1)%MISSILE_MAX


# ******************** 弾の移動 ********************
def move_missile(sc): # 弾の移動
    for i in range(MISSILE_MAX):
        if msl_f[i] == True:
            msl_p[i] += 1
            
            move_x = msl_x[i] + 36*math.cos(math.radians(msl_a[i]))
            move_y = msl_y[i] + 36*math.sin(math.radians(msl_a[i]))
            # 弾がブロックに接触しないか
            if check_block(move_x, move_y, -1, -1, True) == False:
                msl_x[i] = move_x
                msl_y[i] = move_y

                img_rz = pygame.transform.rotozoom(img_weapon, -90-msl_a[i], 1.0)
                sc.blit(img_rz, [msl_x[i]-img_rz.get_width()/2, msl_y[i]-img_rz.get_height()/2])

                if msl_y[i] < LINE_T or LINE_B < msl_y[i] or msl_x[i] < LINE_L or LINE_R < msl_x[i]:
                    msl_f[i] = False

                if msl_p[i] > 20:
                    msl_f[i] = False

            else:
                msl_f[i] = False

                
# ============================================================
#                         ENEMY
# ============================================================

# ******************* 敵を出す ********************
def bring_enemy(): # 敵を出す
    global idx, tmr
    
    if idx == 1 and tmr == 1:
        set_enemy(FIELD_SIZE/2, 200, BOSS, 0, EMY_SPEED_0, BOSS_SHIELD)

    if idx == 2 and tmr == 1:
        set_enemy(FIELD_SIZE/2, 200, BOSS, 0, EMY_SPEED_0, BOSS_SHIELD)

    if idx == 3 and tmr == 1:
        # ボス
        set_enemy(FIELD_SIZE/2, 100, BOSS_MUTEKI, 0, BOSS_SPEED, BOSS_SHIELD)
        # 敵：追尾タイプ
        for x in range(80, 890, 100):
            set_enemy(x, 200, EMY_TRACKING_0, 0, EMY_NORMAL_SPEED, EMY_SHIELD)

    if idx == 4 and tmr == 1:
        # ボス
        set_enemy(FIELD_SIZE/2, FIELD_SIZE/2, BOSS_MUTEKI, 0, EMY_SPEED_0, BOSS_SHIELD)
        # 敵：設置タイプ
        pos = 150
        set_enemy(pos, pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(150, FIELD_SIZE-pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(FIELD_SIZE-pos, pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(FIELD_SIZE-pos, FIELD_SIZE-pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)

    if idx == 5 and tmr == 1:
        # ボス
        set_enemy(FIELD_SIZE/2, 100, BOSS_MUTEKI, 0, BOSS_SPEED, BOSS_SHIELD)
        # 敵：設置タイプ
        pos = 150
        set_enemy(pos, pos, EMY_FIXED, 0, 0, EMY_SHIELD)
        set_enemy(150, FIELD_SIZE-pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(FIELD_SIZE-pos, pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(FIELD_SIZE-pos, FIELD_SIZE-pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        # 敵：追尾タイプ
        for xpos in range(320, 320+80*4+10, 80):
            set_enemy(xpos, 300, EMY_TRACKING_1, 0, EMY_LOW_SPEED, EMY_SHIELD)

    if idx == 6 and tmr == 1:
        # ボス
        set_enemy(FIELD_SIZE/2, 100, BOSS_MUTEKI, 0, EMY_HIGH_SPEED, BOSS_SHIELD)
        # 敵：設置タイプ
        pos = 150
        set_enemy(pos, pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(150, FIELD_SIZE-pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(FIELD_SIZE-pos, pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(FIELD_SIZE-pos, FIELD_SIZE-pos, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(FIELD_SIZE/2, 360, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(300, FIELD_SIZE/2, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        set_enemy(660, FIELD_SIZE/2, EMY_FIXED, 0, EMY_SPEED_0, EMY_SHIELD)
        
            
        

# ******************** 敵機をセット ********************
def set_enemy(x, y, ty, a, sp, sh):
    global emy_no

    while True:
        if emy_f[emy_no] == False:
            emy_f[emy_no] = True
            emy_x[emy_no] = x
            emy_y[emy_no] = y
            emy_a[emy_no] = a
            emy_type[emy_no] = ty
            emy_speed[emy_no] = sp
            emy_shield[emy_no] = sh
            break
        emy_no = (emy_no+1)%ENEMY_MAX
        


# ******************** 敵機の移動 ********************
def move_enemy(sc):
    global tmr, muteki
    
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            # プレイヤーと敵の座標の距離
            x_dis = pl_x - emy_x[i]
            y_dis = pl_y - emy_y[i]

            # 弾の移動
            if emy_type[i] <= 2:
                # 追尾するタイプの弾 -> プレイヤー方向の角度を計算
                if emy_type[i] == BUL_TRACKING:
                    emy_a[i] = math.degrees(math.atan2(y_dis, x_dis))
                move_x = emy_x[i] + emy_speed[i]*math.cos(math.radians(emy_a[i]))
                move_y = emy_y[i] + emy_speed[i]*math.sin(math.radians(emy_a[i]))
                # 弾がブロックと衝突しない -> 弾を移動
                if check_block(move_x, move_y, -1, -1, False) == False:
                    emy_x[i] = move_x
                    emy_y[i] = move_y
                # 直線に移動する弾はブロックに衝突すると消える
                elif emy_type[i] == BUL_STRAIGHT_0 or emy_type[i] == BUL_STRAIGHT_1:
                    emy_f[i] = False
                    

            # 敵の移動
            else:                
                # プレイヤー方向の角度を計算
                emy_a[i] = math.degrees(math.atan2(y_dis, x_dis))
                
                # BOSS
                if emy_type[i] == BOSS or emy_type[i] == BOSS_MUTEKI:
                    move_x = emy_x[i] + emy_speed[i]*math.cos(math.radians(emy_a[i]))
                    move_y = emy_y[i] + emy_speed[i]*math.sin(math.radians(emy_a[i]))
                    # ボスが衝突しない -> ボスを移動
                    if check_block(move_x, move_y, -1, -1, False) == False:
                        emy_x[i] = move_x
                        emy_y[i] = move_y
                        
                    set_bullet(i)

                # 設置タイプの敵
                elif emy_type[i] == EMY_FIXED:
                    set_bullet(i)
                    
                # 追尾タイプの敵
                elif emy_type[i] == EMY_TRACKING_0 or emy_type[i] == EMY_TRACKING_1:
                    move_x = emy_x[i] + emy_speed[i]*math.cos(math.radians(emy_a[i]))
                    move_y = emy_y[i] + emy_speed[i]*math.sin(math.radians(emy_a[i]))
                    # 敵が衝突しない -> 敵を移動
                    if check_block(move_x, move_y, -1, -1, False) == False:
                        emy_x[i] = move_x
                        emy_y[i] = move_y
                    
                    set_bullet(i)
                        
            # 枠外に出た敵(弾)を削除
            if emy_x[i] < LINE_L or LINE_R < emy_x[i] or emy_y[i] < LINE_T or LINE_B < emy_y[i]:
                emy_f[i] = False

            # プレイヤーの弾とのヒットチェック
            if emy_type[i] > 0:
                w = img_enemy[emy_type[i]].get_width()
                h = img_enemy[emy_type[i]].get_height()
                r = int((w+h)/4)+15

                for j in range(MISSILE_MAX):
                    if msl_f[j] == True and get_dis(emy_x[i], emy_y[i], msl_x[j], msl_y[j]) < r*r:
                        msl_f[j] = False
                        # ボスの無敵状態以外
                        if emy_type[i] != BOSS_MUTEKI:
                            if emy_type[i] >= 3:
                                set_effect(emy_x[i], emy_y[i], True)
                            if emy_type[i] >= 1:
                                emy_shield[i] -= 1

                            if emy_shield[i] <= 0:
                                emy_f[i] = False
            
            # ボスの無敵状態の画像
            if tmr%20 == 0:
                muteki = 0
            elif tmr%10 == 0:
                muteki = 1
                
            # 回転させた画像
            if emy_type[i] == BOSS_MUTEKI: # BOSS + 無敵の場合
                img_rz = pygame.transform.rotozoom(img_enemy[emy_type[i]+muteki], 0, 1.0)
            elif emy_type[i] == EMY_FIXED: # 固定の敵
                img_rz = pygame.transform.rotozoom(img_enemy[emy_type[i]], 0, 1.0)
            else:
                img_rz = pygame.transform.rotozoom(img_enemy[emy_type[i]], -90-emy_a[i], 1.0)
                
            # 敵の機体を描く
            sc.blit(img_rz, [emy_x[i]-img_rz.get_width()/2, emy_y[i]-img_rz.get_height()/2])

# ******************** 敵機の弾の出し方 ********************
def set_bullet(no):
    global idx, tmr
    
    if idx == 1 and tmr > 10:
        # ボス：プレイヤーに向かって打つ
        if tmr%5 == 0:
            rand_num = random.randint(0, 10)
            if rand_num <= 2:
                set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_0, emy_a[no], EMY_HIGH_SPEED, BUL_SHIELD_1)
            else:
                set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_1, emy_a[no], EMY_HIGH_SPEED, BUL_SHIELD_1)

    if idx == 2 and tmr > 10:
        # ボス：ランダムの角度に打つ
        rand_num = random.randint(0, 10)
        rand_a = random.randint(0, 360)

        if rand_num <= 2:
            set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_0, rand_a, EMY_HIGH_SPEED, BUL_SHIELD_1)
        else:
            set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_1, rand_a, EMY_HIGH_SPEED, BUL_SHIELD_1)

    if idx == 3 and tmr > 10:
        # ボス：ランダムの角度に打つ
        if emy_type[no] == BOSS or emy_type[no] == BOSS_MUTEKI:
            if tmr%2 == 0:
                rand_a = random.randint(0, 360)
                set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_0, rand_a, BUL_NORMAL_SPEED, BUL_SHIELD_1)
        # 敵：プレイヤーに向かって打つ
        else:
            if tmr%30 == 0:
                set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_1, emy_a[no], BUL_NORMAL_SPEED, BUL_SHIELD_1)

    if idx == 4 and tmr > 10:
        # ボス：プレイヤーに向かって打つ
        if emy_type[no] == BOSS or emy_type[no] == BOSS_MUTEKI:
            if tmr%10 == 0:
                set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_1, emy_a[no], BUL_NORMAL_SPEED, BUL_SHIELD_1)
        #　敵：4方向に向かって打つ
        if emy_type[no] == EMY_FIXED:
            if tmr%60 == 0:
                for a in range(0, 370, 90):
                    set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_0, a+tmr%360, BUL_NORMAL_SPEED, BUL_SHIELD_1)

    if idx == 5 and tmr > 10:
        # ボス：プレイヤーに向かって打つ
        if emy_type[no] == BOSS or emy_type[no] == BOSS_MUTEKI:
            if tmr%10 == 0:
                rand_num = random.randint(0, 1)
                if rand_num == 0:
                    set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_0, emy_a[no], BUL_NORMAL_SPEED, BUL_SHIELD_1)
                elif rand_num == 1:
                    set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_1, emy_a[no], BUL_NORMAL_SPEED, BUL_SHIELD_1)
        # 敵：設置タイプ
        if emy_type[no] == EMY_FIXED:
            if tmr%60 == 0:
                set_enemy(emy_x[no], emy_y[no], BUL_TRACKING, emy_a[no], BUL_LOW_SPEED, BUL_SHIELD_3)
        # 敵：追尾タイプ
        if emy_type[no] == EMY_TRACKING_1:
            if tmr%30 == 0:
                set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_1, emy_a[no], BUL_LOW_SPEED, BUL_SHIELD_1)

    if idx == 6 and tmr > 10:
        # ボス：ランダムの角度に打つ
        if emy_type[no] == BOSS or emy_type[no] == BOSS_MUTEKI:
            if tmr%2 == 0:
                rand_a = random.randint(0, 360)
                set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_1, rand_a, BUL_HIGH_SPEED, BUL_SHIELD_1)
        # 敵：設置タイプ
        if emy_type[no] == EMY_FIXED:
            if tmr%15 == 0:
                for a in range(0, 370, 60):
                    set_enemy(emy_x[no], emy_y[no], BUL_STRAIGHT_0, a+tmr%360, BUL_NORMAL_SPEED, BUL_SHIELD_1)
                    
                

# ============================================================
#                           BLOCK
# ============================================================

# ******************** ブロックを作る ********************
def make_block():
    global idx

    if idx == 5:
        # 黒いブロック
        for ypos in range(440, FIELD_SIZE, 80):
            set_block(280, ypos, BLACK_BLOCK)
            set_block(680, ypos, BLACK_BLOCK)

    if idx == 6:
        # 白いブロック
        set_block(150, 480, WHITE_BLOCK)
        set_block(810, 480, WHITE_BLOCK)
        # 赤いブロック
        set_block(240, 240, RED_BLOCK)
        set_block(720, 240, RED_BLOCK)
        set_block(480, 480, RED_BLOCK)
        set_block(240, 720, RED_BLOCK)
        set_block(720, 720, RED_BLOCK)

        
# ******************** ブロックをセット ********************
def set_block(x, y, ty):
    global block_no

    while True:
        if block_f[block_no] == False:
            block_f[block_no] = True
            block_x[block_no] = x
            block_y[block_no] = y
            block_type[block_no] = ty
            block_b[block_no] = 0
            block_d[block_no] = False
            break
        block_no = (block_no+1) % BLOCK_MAX
        

# ******************** ブロックを描画 ********************
def draw_block(sc):
    for i in range(BLOCK_MAX):
        # ブロックの色を変えたことを記録(黒->白)
        change_color = False
        
        if block_f[i] == True:
            # 黒いブロック + プレイヤーの弾が当たった時
            if block_type[i] == BLACK_BLOCK and block_d[i] == True:
                block_d[i] = False
                # 一瞬だけ白いボックスにして、ボックスにダメージがあることを表現
                block_type[i] = WHITE_BLOCK
                change_color = True
                
            # ブロックの表示
            sc.blit(img_block[block_type[i]],
                [block_x[i]-img_block[block_type[i]].get_width()/2,
                 block_y[i]-img_block[block_type[i]].get_height()/2])

            # 黒から白に変えたボックス -> 黒に戻す
            if change_color == True:
                block_type[i] = BLACK_BLOCK



# ******************** 各方向にブロックがあるか調べる ********************
def check_block(cx, cy, di, dot, pl_bul):
    global pl_shield, pl_muteki
    
    for i in range(BLOCK_MAX):
        if block_f[i] == True:
            # プレイヤーとボックスの接触
            if di == DIR_UP: # 上方向
                if get_dis(cx, cy-dot, block_x[i], block_y[i]) < PIXEL_SIZE*PIXEL_SIZE:
                    # 赤いブロックに接触した時 -> プレイヤーはダメージを受ける
                    if block_type[i] == RED_BLOCK:
                        if pl_muteki > 0:
                            return True
                        pl_shield -= 1
                        pl_muteki = 60
                    return True
            elif di == DIR_DOWN: # 下方向
                if get_dis(cx, cy+dot, block_x[i], block_y[i]) < PIXEL_SIZE*PIXEL_SIZE:
                    # 赤いブロックに接触した時 -> プレイヤーはダメージを受ける
                    if block_type[i] == RED_BLOCK:
                        if pl_muteki > 0:
                            return True
                        pl_shield -= 1
                        pl_muteki = 60
                    return True
            elif di == DIR_LEFT: # 左方向
                if get_dis(cx-dot, cy, block_x[i], block_y[i]) < PIXEL_SIZE*PIXEL_SIZE:
                    # 赤いブロックに接触した時 -> プレイヤーはダメージを受ける
                    if block_type[i] == RED_BLOCK:
                        if pl_muteki > 0:
                            return True
                        pl_shield -= 1
                        pl_muteki = 60
                    return True
            elif di == DIR_RIGHT: # 右方向
                if get_dis(cx+dot, cy, block_x[i], block_y[i]) < PIXEL_SIZE*PIXEL_SIZE:
                    # 赤いブロックに接触した時 -> プレイヤーはダメージを受ける
                    if block_type[i] == RED_BLOCK:
                        if pl_muteki > 0:
                            return True
                        pl_shield -= 1
                        pl_muteki = 60
                    return True
            # プレイヤー意外とボックスの接触
            else:
                if get_dis(cx, cy, block_x[i], block_y[i]) < PIXEL_SIZE*PIXEL_SIZE:
                    # プレイヤーの弾が黒いブロックに当たった場合は、破壊可能
                    if pl_bul == True and block_type[i] == BLACK_BLOCK:
                        block_b[i] = block_b[i] + 1
                        block_d[i] = True
                        if block_b[i] >= 5:
                            block_f[i] = False
                    return True

    return False
  

# ============================================================
#                         EFFECT
# ============================================================

# ******************** 爆発をセット ********************
def set_effect(x, y, emy):
    global eff_no
    
    if emy == True:
        eff_p[eff_no] = 1
    else:
        eff_p[eff_no] = 6
    eff_x[eff_no] = x
    eff_y[eff_no] = y
    eff_no = (eff_no+1)%EFFECT_MAX


# ******************** 爆発の演出 ********************
def draw_effect(sc):
    for i in range(EFFECT_MAX):
        if eff_p[i] > 0:
            img = img_explode[eff_p[i]]
            sc.blit(img, [eff_x[i]-img.get_width()/2, eff_y[i]-img.get_height()/2])

            if eff_p[i] >= 6:
                for j in range(ENEMY_MAX):
                    if emy_f[j] == True:
                        # 無敵状態のボス以外
                        if emy_type[j] != BOSS_MUTEKI:
                            # 爆発の範囲に敵がいる場合、敵と敵の弾にダメージ
                            if get_dis(emy_x[j], emy_y[j], pl_x, pl_y) < (100+200*(eff_p[i]-6))/2 * (100+200*(eff_p[i]-6))/2:
                                emy_shield[j] -= 1
                                set_effect(emy_x[j], emy_y[j], True)
                            if emy_shield[j] <= 0:
                                emy_f[j] = False
            
            eff_p[i] = eff_p[i] + 1

            if eff_p[i] == 6 or eff_p[i] == 11:
                eff_p[i] = 0


        

# ============================================================
#                           GAME
# ============================================================

# ******************** コースクリア判定 ********************
def clear_judge():
    # ボスを倒したら(存在しない) -> ゲームクリア(True)
    clear = True
    boss_num = 0
    emy_count = 0
    
    for i in range(ENEMY_MAX):
        if emy_f[i] == True:
            # ボスが生きている
            if emy_type[i] == BOSS or emy_type[i] == BOSS_MUTEKI:
                clear = False
                boss_num = i
            # ボス以外の敵の数
            elif emy_type[i] == EMY_FIXED or emy_type[i] == EMY_TRACKING_0 or emy_type[i] == EMY_TRACKING_1:
                emy_count += 1

    # ボスのみの場合、ボスの無敵状態を解く
    if emy_count == 0:
        emy_type[boss_num] = BOSS
        
    return clear

# ******************** メインループ ********************
def main():
    global idx, tmr
    global pl_x, pl_y, pl_shield, pl_muteki
    
    pygame.init()
    pygame.display.set_caption("Hacking Game")

    screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
    clock = pygame.time.Clock()

    while True:
        tmr = tmr + 1
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
                
        screen.fill(WHITE)
        key = pygame.key.get_pressed()
        
        # タイトル
        if idx == 0:
            screen.blit(img_title, [0, 0])
            draw_text(screen, "Press [SPACE] to start!", SCREEN_SIZE/2, SCREEN_SIZE/2, 50, CYAN)

            if key[pygame.K_SPACE] == 1:
                course_clear = False
                idx = 6
                tmr = 1

        # ゲームプレイ
        if idx >= 1:
            print(pl_shield)
            # 初期設定
            if tmr == 1:
                pl_x = FIELD_SIZE/2
                pl_y = FIELD_SIZE - 200
                pl_shield = 3
                pl_muteki = 0
                
                for i in range(MISSILE_MAX):
                    msl_f[i] = False
                for i in range(ENEMY_MAX):
                    emy_f[i] = False
                for i in range(BLOCK_MAX):
                    block_f[i] = False
                for i in range(EFFECT_MAX):
                    eff_p[i] = 0
                    
                make_block()

            # ボスを倒すまでのゲーム操作
            if course_clear == False:
                draw_effect(screen)
                draw_block(screen)
                
                move_player(screen, key)
                move_missile(screen)
                bring_enemy()
                move_enemy(screen)

                # ボスを倒した場合
                if clear_judge() == True:
                    course_clear = True
                    tmr = 1
                    
            # ボスを倒す -> コースクリア表示
            if course_clear == True:
                draw_text(screen, "CLEAR COURSE ".format(idx), FIELD_SIZE/2, FIELD_SIZE/2, 80, CYAN)
            # ボスを倒す -> 一定時間が経ったら次のコースへ
            if tmr == 50 and course_clear == True:
                course_clear = False
                idx += 1
                tmr = 0

        # ゲームオーバー
        if idx == -2:
            if tmr == 1:
                move_missile(screen)

            if tmr > 120:
                draw_text(screen, "GAME OVER", SCREEN_SIZE/2, SCREEN_SIZE/2, 80, RED)

            if tmr == 200:
                idx = 0
                tmr = 0

        # ゲームクリア
        if idx == -3:
            move_missile(screen)

            if tmr > 20:
                draw_text(screen, "GAME CLEAR", SCREEN_SIZE/2, SCREEN_SIZE/2, 80, SILVER)

            if tmr == 300:
                idx = 0
                tmr = 0
            
        

        pygame.display.update()
        clock.tick(30)

if __name__ == '__main__':
    main()
    
