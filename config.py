import configparser


def load_config(filename: str = 'config.ini') -> dict:
    config = configparser.ConfigParser()
    config.read(filename)
    return {
        "BOT_TOKEN": config['settings']['BOT_TOKEN'],
        "SUPABASE_URL": config['settings']['SUPABASE_URL'],
        "SUPABASE_API_KEY": config['settings']['SUPABASE_API_KEY'],
    }
