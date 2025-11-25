import os
import random
import sys
import time
import pygame as pg



WIDTH, HEIGHT = 1100, 650
DELTA = {
    pg.K_UP:(0,-5),
    pg.K_DOWN:(0,+5),
    pg.K_LEFT:(-5,0),
    pg.K_RIGHT:(+5,0),
}

os.chdir(os.path.dirname(os.path.abspath(__file__)))


def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    """
    引数：こうかとんRectまたは爆弾Rect
    戻り値：判定結果タプル（横方向，縦方向）
    画面内ならTrue，画面外ならFalse
    """
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right: # 横のチェック
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom: # 縦のチェック
        tate = False
    return yoko, tate


def gameover(screen: pg.Surface) -> None:
    """
    こうかとんに爆弾が着弾した際に、画面をブラックアウトし、
    泣いてるこうかとん画像と
    「Game Over」の文字列を5秒間表示させる
    """
    bg = pg.Surface((WIDTH, HEIGHT)) # 黒い背景
    bg.fill((0,0,0))
    bg.set_alpha(200) # 透過度
    screen.blit(bg,[0,0])

    fonto = pg.font.Font(None, 80) # 文字設定
    txt = fonto.render("Game Over", True, (255, 255, 255))
    txt_rct = txt.get_rect(center = (WIDTH//2, HEIGHT//2))
    screen.blit(txt, txt_rct)

    kk_img = pg.image.load("fig/8.png") # こうかとんを左右に設定
    screen.blit(kk_img, [txt_rct.left - 70, txt_rct.top - 10]) # 左のこうかとん
    screen.blit(kk_img, [txt_rct.right + 20, txt_rct.top - 10]) # 右のこうかとん
    pg.display.update()
    time.sleep(5)
    

# 爆弾が拡大、加速する定義
def init_bb_imgs() -> tuple[list[pg.Surface], list[int]]:
    """
    無限に拡大、加速するのはおかしいので、10段階程度の大きさを変えた爆弾surfaceのリストと加速度のリストを準備する
    """
    bb_imgs = []
    for r in range(1,11):
        bb_img = pg.Surface((20*r, 20*r))
        pg.draw.circle(bb_img, (255,0,0), (10*r,10*r), 10*r)
        bb_img.set_colorkey((0,0,0)) # 四隅を透過
        bb_imgs.append(bb_img)
    bb_accs = [a for a in range(1,11)]
    return bb_imgs, bb_accs


def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")    
    kk_img = pg.transform.rotozoom(pg.image.load("fig/3.png"), 0, 0.9)
    kk_rct = kk_img.get_rect()
    kk_rct.center = 300, 200
    bb_img = pg.Surface((20,20))
    pg.draw.circle(bb_img,(255,0,0),(10,10),10)
    bb_img.set_colorkey((0,0,0)) # 四隅の黒を透過
    bb_rct = bb_img.get_rect()
    bb_rct.center = random.randint(0,WIDTH), random.randint(0,HEIGHT) # 爆弾の縦と横座標
    vx, vy = +5, +5 # 爆弾の縦と横の速度
    clock = pg.time.Clock()
    tmr = 0

    bb_imgs, bb_accs = init_bb_imgs() # 2つのリストを取得

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bb_rct):
            gameover(screen)
            return 
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, mv in DELTA.items():
            if key_lst[k]:
                sum_mv[0] += mv[0] # 横方向の移動量
                sum_mv[1] += mv[1] # 縦方向の移動量
        # if key_lst[pg.K_UP]:
        #     sum_mv[1] -= 5
        # if key_lst[pg.K_DOWN]:
        #     sum_mv[1] += 5
        # if key_lst[pg.K_LEFT]:
        #     sum_mv[0] -= 5
        # if key_lst[pg.K_RIGHT]:
        #     sum_mv[0] += 5
        kk_rct.move_ip(sum_mv)
        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])
        screen.blit(kk_img, kk_rct)
        yoko, tate = check_bound(bb_rct)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1

        avx = vx*bb_accs[min(tmr//500, 9)] # while文の中でtmrの値に応じて，リストから適切な要素を選択する
        avy = vy*bb_accs[min(tmr//500, 9)]
        bb_img = bb_imgs[min(tmr//500, 9)]
        bb_rct.width = bb_img.get_rect().width # Surfaceの大きさが変わった場合は，Rectのwidth属性とheight属性を更新する
        bb_rct.height = bb_img.get_rect().height
        bb_rct.move_ip(avx,avy) # avxとavyをmove_ipメソッドに渡す
        screen.blit(bb_img, bb_rct)

        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()
