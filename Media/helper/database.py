from pymongo import MongoClient

from Media.config import LOGGER, MONGO_DB_URL 

mongo_client = MongoClient(MONGO_DB_URL)
db = mongo_client["media-bot"]

accesdb = db.acces
gcastdb = db['GCAST']
logger_collection = db['logger']
forcesub_collection = db['forcesub']
broadcast_collection = db['broadcast']
maintenance_collection = db['maintenance']
cancellation_collection = db['cancellations']
deleted_accounts_collection = db['deleted_accounts']
bot_removed_users_collection = db['bot_removed_users']
transactions_collection = db["nama_koleksi_transaksi"]

C15 = """
WAJIB BACA RULES!
Kami tidak bertanggung jawab atas segala apa yang terjadi,
*Jika group terban maka akan dibuat group baru(Bayar Lagi)
*Group kena BAN tidak ada refund
*Group tidak memiliki backup
*Join Group = Tau Resiko
"""

C20 = """
TERIMAKASIH SUDAH JOIN!
LINK HANYA BISA DIAKSES 1x (JANGAN OUT)
LINK HANYA BERLAKU SATU JAM - JANGAN SAMPE EXPIRED
"""

async def set_orkut(qris_code, merchant, api_key):
    try:
        result = accesdb.users.update_one(
            {"_id": 1},
            {"$set": {"qris_code": qris_code, "merchant": merchant, "api_key": api_key}},
            upsert=True
        )
        return result.modified_count > 0 or result.upserted_id is not None
    except Exception as e:
        return

async def get_orkut():
    user = accesdb.users.find_one({"_id": 1})
    if user:
        return {
            "qris_code": user.get("qris_code"),
            "merchant": user.get("merchant"),
            "api_key": user.get("api_key")
        }
    else:
        return None
        
async def del_orkut():
    try:
        result = accesdb.users.update_one(
            {"_id": 1},
            {"$unset": {"qris_code": "", "merchant": "", "api_key": ""}}
        )
        return result.modified_count > 0
    except Exception as e:
        return
        
async def create_pending_transaction(user_id):
    transaction_data = {
        "user_id": user_id,
        "status": "pending"
    }
    transactions_collection.insert_one(transaction_data)

async def check_pending_transaction(user_id):
    pending_transaction = transactions_collection.find_one({
        "user_id": user_id,
        "status": "pending" 
    })
    return pending_transaction is not None

async def delete_pending_transaction(user_id):
    result = transactions_collection.delete_many({
        "user_id": user_id,
        "status": "pending"
    })
    return result.deleted_count
    
async def increment_deleted_accounts():
    try:
        deleted_accounts_collection.update_one(
            {"_id": "count"},
            {"$inc": {"count": 1}},
            upsert=True
        )
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan: {e}")
        
async def increment_bot_removed_users():
    try:
        bot_removed_users_collection.update_one(
            {"_id": "count"},
            {"$inc": {"count": 1}},
            upsert=True
        )
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan: {e}")
        
async def get_deleted_accounts_count():
    try:
        document = deleted_accounts_collection.find_one({"_id": "count"})
        return document['count'] if document else 0
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan: {e}")

async def get_bot_removed_users_count():
    try:
        document = bot_removed_users_collection.find_one({"_id": "count"})
        return document['count'] if document else 0
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan: {e}")
        
async def set_price(price):
    try:
        accesdb.users.update_one({"_id": 1}, {"$set": {"price": price}}, upsert=True)
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengupdate harga: {e}")

async def get_price():
    try:
        user = accesdb.users.find_one({"_id": 1})
        if user:
            return user.get("price", "500")
        else:
            return 0
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengambil harga: {e}")
        return
        
async def set_welcome(text):
    try:
        accesdb.users.update_one({"_id": 1}, {"$set": {"welcome": text}}, upsert=True)
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengupdate welcome: {e}")

async def get_welcome():
    try:
        user = accesdb.users.find_one({"_id": 1})
        if user:
            return user.get("welcome", C15)
        else:
            return C15
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengambil welcome: {e}")
        return

async def set_text_two(text):
    try:
        accesdb.users.update_one({"_id": 1}, {"$set": {"text_two": text}}, upsert=True)
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengupdate welcome: {e}")

async def get_text_two():
    try:
        user = accesdb.users.find_one({"_id": 1})
        if user:
            return user.get("text_two", C20)
        else:
            return C20
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengambil welcome: {e}")
        return
        
async def set_forcesub(username):
    try:
        accesdb.users.update_one({"_id": 1}, {"$set": {"forcesub": username}}, upsert=True)
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat menyetel forcesub:: {e}")
        return
        
async def get_forcesub():
    try:
        user = accesdb.users.find_one({"_id": 1})
        if user:
            return user.get("forcesub")
        else:
            return 0
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mendapatkan forcesub: {e}")
        return

async def set_logger(chat_id):
    try:
        accesdb.users.update_one({"_id": 1}, {"$set": {"logger": chat_id}}, upsert=True)
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat menyimpan logger: {e}")
        return
        
async def get_logger():
    try:
        user = accesdb.users.find_one({"_id": 1})
        if user:
            return user.get("logger")
        else:
            return 0
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengambil logger: {e}")
        return
        
async def set_chat_id(chat_id):
    try:
        accesdb.users.update_one({"_id": 1}, {"$set": {"chat_id": chat_id}}, upsert=True)
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat memperbarui link: {e}")
        return
        
async def get_chat_id():
    try:
        user = accesdb.users.find_one({"_id": 1})
        if user:
            return user.get("chat_id")
        else:
            return 0
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengambil link: {e}")
        return

async def get_broadcast():
    try:
        setting = broadcast_type.find_one({"name": "type"})
        return setting["value"] if setting else True
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengambil type broadcast: {e}")
        return

async def set_broadcast(value):
    try:
        broadcast_type.update_one(
            {"name": "type"},
            {"$set": {"value": value}},
            upsert=True
        )
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat menyimpan type broadcast: {e}")
        return

async def get_maintenance():
    try:
        setting = maintenance_collection.find_one({"name": "maintenance"})
        return setting["value"] if setting else True
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengambil pengaturan maintenance: {e}")
        return

async def set_maintenance(value):
    try:
        maintenance_collection.update_one(
            {"name": "maintenance"},
            {"$set": {"value": value}},
            upsert=True
        )
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengatur pengaturan maintenance: {e}")
        return

async def get_status_logger():
    try:
        setting = logger_collection.find_one({"name": "loggs"})
        return setting["value"] if setting else False
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengatur pengaturan logger: {e}")
        return
        
async def set_status_logger(value):
    try:
        logger_collection.update_one(
            {"name": "loggs"},
            {"$set": {"value": value}},
            upsert=True
        )
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengatur pengaturan logger: {e}")
        return

async def get_force_status():
    try:
        setting = forcesub_collection.find_one({"name": "force_sub"})
        return setting["value"] if setting else False
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengatur pengaturan Forcesub: {e}")
        return
        
async def set_force_status(value):
    try:
        forcesub_collection.update_one(
            {"name": "force_sub"},
            {"$set": {"value": value}},
            upsert=True
        )
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengatur pengaturan Forcesub: {e}")
        return

async def get_broadcast():
    try:
        setting = broadcast_collection.find_one({"name": "type"})
        return setting["value"] if setting else True
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengatur pengaturan broadcast: {e}")
        return
        
async def set_broadcast(value):
    try:
        broadcast_collection.update_one(
            {"name": "type"},
            {"$set": {"value": value}},
            upsert=True
        )
    except Exception as e:
        LOGGER("INFO").info(f"Terjadi kesalahan saat mengatur pengaturan broadcast: {e}")
        return
        
async def get_gcast() -> list:
    gcast = gcastdb.find_one({"gcast_id": "gcast_id"})
    if not gcast:
        return []
    return gcast["gcast"]
    
async def add_gcast(user_id: int) -> bool:
    gcast = await get_gcast()
    gcast.append(user_id)
    gcastdb.update_one(
        {"gcast_id": "gcast_id"}, {"$set": {"gcast": gcast}}, upsert=True
    )
    return True

async def remove_gcast(user_id: int) -> bool:
    gcast = await get_gcast()
    gcast.remove(user_id)
    gcastdb.update_one(
        {"gcast_id": "gcast_id"}, {"$set": {"gcast": gcast}}, upsert=True
    )
    return True

async def clear_gcast() -> bool:
    gcast = await get_gcast()
    gcast.clear()
    gcastdb.update_one(
        {"gcast_id": "gcast_id"}, {"$set": {"gcast": gcast}}, upsert=True
    )
    return True
