import supabase
from supabase._sync.client import SyncClient


def init_db(url: str, key: str) -> SyncClient:
    return supabase.create_client(url, key)


def add_user(db: SyncClient, tg_id: int, username: str, name: str, surname: str) -> None:
    data = {
        "id": tg_id,
        "username": username,
        "name": name,
        "surname": surname
    }
    db.table("users").insert(data).execute()


def get_user(db: SyncClient, tg_id: int) -> dict:
    resp = db.table("users").select("*").eq("id", tg_id).execute()
    if resp.data:
        return resp.data[0]
    else:
        return {}


def delete_user(db: SyncClient, tg_id: int) -> None:
    db.table('users').delete().eq('id', tg_id).execute()


def update_user(db: SyncClient,
    tg_id: int,
    username: str,
    name: str,
    surname: str) -> str:

    data = {
        "id": tg_id,
        "username": username,
        "name": name,
        "surname": surname
    }
    old_data = get_user(db, tg_id)
    db.table("users").update(data).eq('id', tg_id).execute()
    res = ''
    for key in data:
        if data[key] != old_data[key]:
            res += f'{old_data[key]} -> {data[key]}\n'
    if not res:
        return 'Все данные уже актуальны!'
    return 'Изменения:\n' + res


def record_message(db: SyncClient, tg_id: int, message: str) -> None:
    data = {
        "id": tg_id,
        "message": message
    }
    db.table("message").insert(data).execute()


def get_taric(db, code):
    resp = db.table("codes").select("*").eq("code", code).execute()
    if resp.data:
        return resp.data[0]
    else:
        return {}


def write_taric(db, code, description):
    data = {
        "code": code,
        "description": description
    }
    db.table("codes").insert(data).execute()


def get_offices(db, city):
    resp = db.table("offices").select("*").eq("city", city).execute()
    if resp.data:
        return resp.data
    else:
        return {}


def write_office(db, city, ref_number, description, link):
    data = {
        "city": city,
        "description": description,
        'ref_number': ref_number,
        'link': link
    }
    db.table("offices").insert(data).execute()

def search_taric(db, description):
    resp = db.table("codes").select("*").ilike("description", f"%{description}%").execute()
    if resp.data:
        return resp.data[0]
    else:
        return {}
