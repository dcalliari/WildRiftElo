import aiohttp
import re
import os
import json
from app import Base, Broadcaster, Account, async_session, engine
from sqlalchemy.future import select

SCRAPED_URL = os.environ.get('SCRAPED_URL')
API_URL = os.environ.get('API_URL')


def lang():
    with open(os.path.abspath('resources/lang.json'), encoding='utf8') as json_file:
        lang = json.load(json_file)
        return lang


async def idCheck(riotId):
    regex = "[\w|\s]{3,16}[#]\w{3,5}"
    if re.match(regex, riotId):
        riotId = riotId.split('#')
        if len(riotId[0]) < 17 and len(riotId[1]) < 6:
            return True
        else:
            return False


async def createHash(riotId):
    riotId = riotId.replace('#', '/')
    async with aiohttp.ClientSession() as session:
        resp = await session.get(f'{SCRAPED_URL}/{riotId}')
        return await resp.text()


async def get_channels():
    channels = []
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        query = select(Broadcaster).where(Broadcaster.is_active == True)
        result = await session.execute(query)
        for i in result.scalars():
            channels.append(i.twitch_id)
        await session.commit()
    await engine.dispose()
    return channels


async def add_channel(value):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        query = select(Broadcaster).where(
            Broadcaster.twitch_id == value, Broadcaster.is_active == False)
        result = await session.execute(query)
        channel = result.scalars().first()
        if channel:
            channel.is_active = True
        else:
            session.add(Broadcaster(twitch_id=value))
        await session.commit()
    await engine.dispose()


async def del_channel(value):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        query = select(Broadcaster).where(
            Broadcaster.twitch_id == value, Broadcaster.is_active == True)
        result = await session.execute(query)
        channel = result.scalars().first()
        if channel:
            channel.is_active = False
        await session.commit()
    await engine.dispose()


async def get_elo(key, channel):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channels = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
            id = channels.scalars().first().id
            query = select(Account).where(Account.broadcaster_id ==
                                          id, Account.acc_id == key)
            result = await session.execute(query)
            account = result.scalars().first()
            hash = account.hash
            cache = account.cache
            lang = await get_lang(channel)
    await engine.dispose()
    try:
        async with aiohttp.ClientSession() as req:
            resp = await req.get(f'{API_URL}/{hash}/{lang}')
            elo = await resp.text()
            if '#' in elo:
                account.cache = elo
                await session.commit()

                return elo
            else:
                return cache
    except:
        return cache


async def get_accounts(channel, type):
    id_list = []
    elo_list = []
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channels = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
            id = channels.scalars().first().id
            query = select(Account).where(Account.broadcaster_id == id)
            list = await session.execute(query)
        for account in list.scalars():
            id_list.append(account.acc_id)
        id_list.sort()
        for i in id_list:
            elo_list.append(await get_elo(i, channel))
        if type == 'elo':
            return elo_list
        elif type == 'id':
            return id_list
    await engine.dispose()


async def update_riot_id(key, value, channel):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channels = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
            id = channels.scalars().first().id
            query = select(Account).where(Account.broadcaster_id ==
                                          id, Account.acc_id == key)
            result = await session.execute(query)
            account = result.scalars().first()
            if account:
                account.hash = value
            else:
                session.add(Account(hash=value, acc_id=key, broadcaster_id=id))
        await session.commit()
    await engine.dispose()


async def del_account(key, channel):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        channels = await session.execute(select(Broadcaster).where(
            Broadcaster.twitch_id == channel))
        id = channels.scalars().first().id
        query = select(Account).where(Account.broadcaster_id ==
                                      id, Account.acc_id == key)
        result = await session.execute(query)
        account = result.scalars().first()
        if account:
            await session.delete(account)
            await session.commit()
            return True
        else:
            return False


async def get_lang(channel):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channel = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
    return channel.scalars().first().lang


async def change_lang(value, channel):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        async with session.begin():
            channels = await session.execute(select(Broadcaster).where(
                Broadcaster.twitch_id == channel))
            channels = channels.scalars().first()
            channels.lang = value
            await session.commit()
    await engine.dispose()
