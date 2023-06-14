import random


def play_baccarat(t, amount):
    odds = {'banker': 1.95, 'player': 2, 'tie': 9, 'pair': 12}
    playing_result = random.random()

    if playing_result < 0.458597 and t == 'banker':
        return amount * odds[t]
    elif 0.458597 <= playing_result < 0.904844 and t == 'player':
        return amount * odds[t]
    elif 0.904844 <= playing_result < 1 and t == 'tie':
        return amount * odds[t]
    elif t == 'pair' and playing_result < 0.074683:
        return amount * odds[t]

    return 0


def daily_process():
    a = 1
#    feedback_current_data
#    investment_data_update
#    decision_making
#    gambling_result


if __name__ == '__main__':
    for _ in range(100):
        print(play_baccarat('banker', 10000))
