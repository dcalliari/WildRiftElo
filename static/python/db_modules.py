from app import db, Broadcaster, Account

dorito = ['ferro', 'iron', 'bronze', 'prata', 'silver', 'ouro',
          'gold', 'plat', 'platinum', 'platina', 'esmeralda', 'emerald']


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


def get(key, channel, type):
    if type == 'conta':
        return Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().riot_id
    elif type == 'elo':
        return Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().elo
    elif type == 'div':
        div = Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(
            twitch_id=channel).first().id).first().div
        if div == None:
            div = ''
        return div
    elif type == 'pdl':
        pdl = Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(
            twitch_id=channel).first().id).first().pdl
        if pdl == None:
            pdl = 0
        return pdl
    elif type == 'drt':
        if Account.query.filter_by(acc_id=key, broadcaster_id=Broadcaster.query.filter_by(twitch_id=channel).first().id).first().elo.lower() in dorito:
            drt = 'DoritosChip '
        else:
            drt = 'PdL'
        return drt


def update_riot_id(key, value, channel):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()

    account = Account.query.filter_by(
        acc_id=key, broadcaster_id=b_id.id).update({Account.riot_id: value})
    if account == 0:
        account = Account(riot_id=value, acc_id=key, broadcaster=b_id)
        db.session.add(account)
    db.session.commit()
    return


def update_elo(key, value, channel):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()

    account = Account.query.filter_by(
        acc_id=key, broadcaster_id=b_id.id).update({Account.elo: value})
    if account == 0:
        account = Account(elo=value, acc_id=key, broadcaster=b_id)
        db.session.add(account)
    db.session.commit()
    return


def update_div(key, value, channel):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()

    account = Account.query.filter_by(
        acc_id=key, broadcaster_id=b_id.id).update({Account.div: value})
    if account == 0:
        account = Account(div=value, acc_id=key, broadcaster=b_id)
        db.session.add(account)
    db.session.commit()
    return


def update_pdl(key, value, channel):
    b_id = db.session.query(Broadcaster).where(
        Broadcaster.twitch_id == channel).first()

    account = Account.query.filter_by(
        acc_id=key, broadcaster_id=b_id.id).update({Account.pdl: value})
    if account == 0:
        account = Account(pdl=value, acc_id=key, broadcaster=b_id)
        db.session.add(account)
    db.session.commit()
    return
