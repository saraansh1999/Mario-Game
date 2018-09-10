import signal
import sys
import os
import time
import random
import signal
from alarmexception import *
from screen import Screen
from getchunix import _getChUnix as getChar
from environment_maker import *
from environment import Player_Bullet
from collectibles import Gun
from player import Player
from boss import Boss
from scoreboard import Scoreboard


# initializing global variables
score = Scoreboard()
scrdim = (500, 50)
base_bottom = scrdim[1] - 5
base_up = 2
base_left = 1
base_right = scrdim[0] - 2
start = 0
end = 100
shift_cue = (start + end) / 2
scr = Screen(scrdim)
scr.make_grid()
player = Player(
    1,
    base_bottom - 1,
    base_up,
    base_bottom,
    base_left,
    base_right,
    scr.grid)
player.put(1)
facing = 1
clouds_object = Cloud_Maker(
    base_up,
    scrdim[0] - 150,
    base_bottom,
    base_left,
    base_right,
    scr.grid)
clouds = clouds_object()
pipes_object = Pipe_Maker(
    shift_cue,
    base_bottom,
    base_left,
    base_right,
    scr.grid)
pipes = pipes_object()
enemies_object = Enemy_Maker(base_bottom, base_left, base_right, scr.grid)
enemies = enemies_object()
bricks_object = Brick_Maker(base_bottom, base_left, base_right, scr.grid)
bricks = bricks_object()
moving_brick_object = Moving_Brick_Maker(
    base_bottom, base_left, base_right, scr.grid)
moving_bricks = moving_brick_object()
pits_object = Pit_Maker(
    shift_cue,
    base_bottom,
    base_left,
    base_right,
    scr.grid,
    scrdim[1] - 1)
pits = pits_object()
coins_object = Coin_Maker(base_bottom - 1, scr.grid)
coins = coins_object()
gun_upgrades_object = Gun_Upgrade_Maker(base_bottom - 1, scr.grid)
gun_upgrades = gun_upgrades_object()
spring_object = Spring_Maker(base_bottom, base_left, base_right, scr.grid)
springs = spring_object()
player_bullets = []
enemy_bullets = []
boss = Boss(
    scrdim[0] - 10,
    base_up,
    base_up,
    base_bottom,
    scrdim[0] - 30,
    base_right,
    scr.grid)
boss.put(1)


# input funtions
def alarmhandler(signum, frame):
    raise AlarmException


def get_input(timeout=0.2):
    signal.signal(signal.SIGALRM, alarmhandler)
    signal.setitimer(signal.ITIMER_REAL, timeout)
    try:
        text = getChar()()
        signal.alarm(0)
        return text
    except AlarmException:
        pass
    signal.signal(signal.SIGALRM, signal.SIG_IGN)
    return ''


# helper funtions
def respawn():
    play("die.wav")
    print('POOR MARIO :(')
    time.sleep(3)
    player.remove()
    player.x = start + 1
    player.y = 10
    player.gun_mode = 0
    player.put(1)


def over():
    play("gameover.wav")
    time.sleep(6)
    print('GAME OVER!!! :(')
    sys.exit()


def over_success():
    play("win.wav")
    time.sleep(6)
    print('CONGRATULATIONS YOU BEAT THE BOSS!!! :)')
    sys.exit()


def play(sound):
    try:
        os.system("aplay -q " + sound + " 2>/dev/null &")
    except BaseException:
        pass


# Main game loop
while True:

    # Boss Control
    try:
        if boss.x >= start and boss.x <= end:
            ret13 = boss.gravity_check()
            boss.random_jump(ret13)
            boss.horizontal_move()
            boss.shoot(enemy_bullets, player.x)
            ret11 = boss.check_collision(player.x, player.y)
            if ret11 == 1:
                ret12 = score.die()
                if ret12 == 1:
                    player.remove()
                    del player
                    over()
                else:
                    respawn()
    except SystemExit:
        sys.exit()
    except BaseException:
        pass

    # Elements Control
    for moving in moving_bricks:
        if moving.x >= start and moving.x <= end:
            ret11 = moving.check_player_above(player.x, player.y)
            if ret11 != 0:
                player.remove()
                player.y -= 1
                player.put(0)
            moving.move()
        moving.put()

    for cloud in clouds:
        if cloud.x <= end and cloud.x >= start:
            cloud.put()

    for coin in coins:
        if coin.x <= end and coin.x >= start:
            ret9 = coin.check_collection(player.x, player.y)
            if ret9 == 1:
                play("collect_coin.wav")
                score.increment_coins()
                coins.remove(coin)
                del coin

    for gun in gun_upgrades:
        if gun.x <= end and gun.x >= start:
            collected = gun.check_collection(player.x, player.y)
            if collected == 1:
                play("colect_gun.wav")
                player.gun_mode = 1
                if gun.type == 2:
                    gun_upgrades.remove(gun)
                    del gun

    try:
        for bullet in player_bullets:
            ret6 = bullet.hitormiss(boss.x, boss.y, 2)
            if ret6 == 1:
                play("enemy_hit.wav")
                score.increment_kills()
                player_bullets.remove(bullet)
                del bullet
                ret7 = boss.die()
                if ret7 == 1:
                    boss.remove()
                    del boss
                    over_success()
    except SystemExit:
        sys.exit()
    except BaseException:
        pass

    for enemy in enemies:
        if enemy.x <= end and enemy.x >= start:

            enemy.gravity_check(player.x)

            flag = 0

            for bullet in player_bullets:
                ret6 = bullet.hitormiss(enemy.x, enemy.y, 1)
                if ret6 == 1:
                    play("enemy_hit.wav")
                    score.increment_kills()
                    player_bullets.remove(bullet)
                    del bullet
                    enemy.remove()
                    enemies.remove(enemy)
                    del enemy
                    flag += 1
                    break

            if flag == 0:
                ret3 = enemy.check_collision(player.x, player.y)
                if ret3 == 1:
                    play("stomp.wav")
                    score.increment_kills()
                    enemies.remove(enemy)
                    del enemy
                elif ret3 == 2:

                    ret10 = score.die()
                    if ret10 == 1:
                        player.remove()
                        del player
                        over()
                    else:
                        respawn()
                else:
                    if enemy.type == 1:
                        enemy.move()
                    elif enemy.type == 2:
                        enemy.move(player.x, enemy_bullets)
                    else:
                        enemy.move(player.x)

    for pit in pits:
        ret4 = pit.pitfall(player.x, player.y)
        if ret4 == 1:

            ret10 = score.die()
            if ret10 == 1:
                player.remove()
                del player
                over()
            else:
                respawn()

    for bullet in player_bullets:
        ret5 = bullet.move(start, end)
        if ret5 == 1:
            player_bullets.remove(bullet)
            del bullet

    for bullet in enemy_bullets:
        ret8 = bullet.move(start, end)
        if ret8 == 1:
            enemy_bullets.remove(bullet)
            del bullet
        else:
            ret7 = bullet.hitormiss(player.x, player.y)
            if ret7 == 1:

                ret10 = score.die()
                if ret10 == 1:
                    player.remove()
                    del player
                    over()
                else:
                    respawn()
                enemy_bullets.remove(bullet)
                del bullet

    for spring in springs:
        spring.put()
        ret7 = spring.check_application(player.x, player.y)
        if ret7 == 1:
            play("jump.wav")
            player.remove()
            player.y -= 20
            player.put(0)

    # Shift Screen
    if player.x >= shift_cue and player.dir == 3 and end < scrdim[0]:
        start += 1
        end += 1
        shift_cue = (start + end) / 2

    # Player fall
    ret = player.gravity_check()

    # Event Handling
    try:

        key_in = get_input()

        if key_in == 'w' and ret:
            play("jump.wav")
            ret2 = player.move(1)
            for coin in coins:
                if coin.x <= end and coin.x >= start:
                    ret9 = coin.check_collection_jump(player.x, player.y, ret2)
                    if ret9 == 1:
                        play("collect_coin.wav")
                        score.increment_coins()
                        coins.remove(coin)
                        del coin

            for gun in gun_upgrades:
                if gun.x <= end and gun.x >= start:
                    ret9 = gun.check_collection_jump(player.x, player.y, ret2)
                    if ret9 == 1:
                        play("collect_gun.wav")
                        player.gun_mode = 1
                        if gun.type == 2:
                            gun_upgrades.remove(gun)
                            del gun
            player.put(0)

        if key_in == 'a':
            if player.x > start:
                player.move(2)
            facing = -1

        if key_in == 'd':
            player.move(3)
            facing = 1

        if key_in == 'g':
            if player.gun_mode == 1:
                play("shoot.wav")
                if facing == 1:
                    player_bullets.append(
                        Player_Bullet(
                            player.x + 1,
                            player.y + 1,
                            1,
                            base_bottom,
                            base_left,
                            base_right,
                            scr.grid))
                else:
                    player_bullets.append(
                        Player_Bullet(
                            player.x, player.y + 1, -1, base_bottom, base_left, base_right, scr.grid))
                player_bullets[-1].put()

        if key_in == '0':
            print('Game Closed.')
            break

    except BaseException:
        # no movement
        player.put(1)

    # Update Score
    score.update_score()

    # Clear Screen
    os.system('tput reset')

    # Printing everything on screen
    scr.blit(start, end)
    try:
        print(
            "Scoreboard:\nCoins : ",
            score.coins,
            "   Kills : ",
            score.kills,
            " Lives : ",
            score.lives,
            " SCORE : ",
            score.score,
            " BOSS : ",
            boss.lives,
            "\n")
    except BaseException:
        print(
            "Scoreboard:\nCoins : ",
            score.coins,
            "   Kills : ",
            score.kills,
            " Lives : ",
            score.lives,
            " SCORE : ",
            score.score,
            "\n")


sys.exit()
