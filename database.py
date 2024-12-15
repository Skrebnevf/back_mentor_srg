import supabase as sp

def init_db(url, key):
    return sp.create_client(url, key)

def add_user(supabase, user_id, username, name, surname):
    data = {
        "id": user_id,
        "username": username,
        "name": name,
        "surname": surname
    }

    resp = supabase.table("users").insert(data).execute()

def get_user(supabase, user_id):
    resp = supabase.table("users").select("*").eq("id", user_id).execute()
    return resp.data
