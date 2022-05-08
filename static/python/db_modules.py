from app import db, Broadcaster, Account
import re
import os
import json
import requests

SCRAPED_URL = os.environ.get('SCRAPED_URL')
API_URL = os.environ.get('API_URL')


def lang():
    with open(os.path.abspath('resources/lang.json'), encoding='utf8') as json_file:
        lang = json.load(json_file)
        return lang


def idCheck(riotId):
    regex = "[\w|\s]{3,16}[#]\w{3,5}"
    if re.match(regex, riotId):
        riotId = riotId.split('#')
        if len(riotId[0]) < 17 and len(riotId[1]) < 6:
            return True
        else:
            return False


def createHash(riotId):
    riotId = riotId.replace('#', '/')
    return requests.get(f'{SCRAPED_URL}/{riotId}').text


def get_channels():
    CHANNELS = []
    for i in range(len(db.session.query(Broadcaster.twitch_id).where(Broadcaster.is_active == True).all())):
        CHANNELS.append(db.session.query(Broadcaster.twitch_id).where(
            Broadcaster.is_active == True).all()[i][0])
    return CHANNELS


def add_channel(value):
    if db.session.query(db.exists().where(Broadcaster.twitch_id == value, Broadcaster.is_active == False)).scalar():
        Broadcaster.query.filter_by(twitch_id=value, is_active=False).update({
            Broadcaster.is_active: True})
        db.session.commit()
        return
    else:
        db.session.add(Broadcaster(twitch_id=value))
        db.session.commit()
        return


def del_channel(value):
    if db.session.query(db.exists().where(Broadcaster.twitch_id == value, Broadcaster.is_active == True)).scalar():
        Broadcaster.query.filter_by(twitch_id=value, is_active=True).update({
            Broadcaster.is_active: False})
        db.session.commit()
        return


def get_elo(key, channel):
    hash = Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(
        twitch_id=channel).first().id).first().hash
    return requests.get(f'{API_URL}{hash}/br').text


def get_accounts(channel, type):
    id_list = []
    elo_list = []
    list = Account.query.filter_by(broadcaster_id=Broadcaster.query.filter_by(
        twitch_id=channel).all()[0].id).all()
    for account in list:
        id_list.append(account.acc_id)
    id_list.sort()
    for i in id_list:
        elo_list.append(get_elo(i, channel))
    if type == 'elo':
        return elo_list
    elif type == 'id':
        return id_list


def update_riot_id(key, value, channel):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()
    account = Account.query.filter_by(acc_id=key, broadcaster_id=b_id.id).update(
        {Account.hash: value})
    if account == 0:
        account = Account(hash=value, acc_id=key,
                          broadcaster=b_id)
        db.session.add(account)
    db.session.commit()
    return


def get_lang(channel):
    return Broadcaster.query.filter_by(twitch_id=channel).first().lang


def change_lang(value, channel):
    Broadcaster.query.filter_by(twitch_id=channel).update({
        Broadcaster.lang: value})
    db.session.commit()
    return
