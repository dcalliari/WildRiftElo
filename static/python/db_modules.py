from app import db, Broadcaster, Account

dorito = ['ferro', 'iron', 'bronze', 'prata', 'silver', 'ouro',
          'gold', 'plat', 'platinum', 'platina', 'esmeralda', 'emerald']


def get_channel():
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
        db.session.add(db.Broadcaster(twitch_id=value))
        db.session.commit()
        return


def del_channel(value):
    if db.session.query(db.exists().where(Broadcaster.twitch_id == value, Broadcaster.is_active == True)).scalar():
        Broadcaster.query.filter_by(twitch_id=value, is_active=True).update({
            Broadcaster.is_active: False})
        db.session.commit()
        return


def get(key, channel, type):
    if type == 'conta':
        return Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().riot_id
    if type == 'elo':
        return Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().elo
    elif type == 'div':
        return Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().div
    elif type == 'pdl':
        return Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().pdl
    elif type == 'drt':
        if Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().elo.lower() in dorito:
            drt = 'DoritosChip '
        else:
            drt = 'PdL'
        return drt


def update_riot_id(key, value, channel):
    try:
        db.session.add(Account(acc_id=key, riot_id=value, broadcaster=db.session.query(
            Broadcaster).where(Broadcaster.twitch_id == channel).one()))
        db.session.commit()
    except:
        db.session.rollback()
        Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(
            twitch_id=channel).first().id).update({Account.riot_id: value})
        db.session.commit()
    return


def update_elo(key, value, channel):
    try:
        db.session.add(Account(acc_id=key, elo=value, broadcaster=db.session.query(
            Broadcaster).where(Broadcaster.twitch_id == channel).one()))
        db.session.commit()
    except:
        db.session.rollback()
        Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(
            twitch_id=channel).first().id).update({Account.elo: value})
        db.session.commit()
    return


def update_div(key, value, channel):
    try:
        db.session.add(Account(acc_id=key, div=value, broadcaster=db.session.query(
            Broadcaster).where(Broadcaster.twitch_id == channel).one()))
        db.session.commit()
    except:
        db.session.rollback()
        Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(
            twitch_id=channel).first().id).update({Account.div: value})
        db.session.commit()
    return


def update_pdl(key, value, channel):
    try:
        db.session.add(Account(acc_id=key, pdl=value, broadcaster=db.session.query(
            Broadcaster).where(Broadcaster.twitch_id == channel).one()))
        db.session.commit()
    except:
        db.session.rollback()
        Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(
            twitch_id=channel).first().id).update({Account.pdl: value})
        db.session.commit()
    return
