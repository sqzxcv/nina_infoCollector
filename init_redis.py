from config import config
from redis import StrictRedis
import json

Redis2Info = config.info["Redis2Info"]
redis_db = StrictRedis(
    host=Redis2Info['host'],
    port=Redis2Info['port'],
    password=Redis2Info['pwd'],
    db=Redis2Info['db']
)


# catalogs = redis_db.smembers("kejiliechannels")

# # print (catalogs)
# catalist = []
# for c in catalogs:
#     catalist.append(c.decode('utf-8'))
# cata_str = json.dumps(catalist)

# fp = open('./urllist.txt', 'w')
# fp.write(cata_str)


fp = open('./urllist.txt', 'r')
init_db_content = fp.read()

cat = json.loads(init_db_content)

aset = set()
for c in cat:
    redis_db.sadd("kejiliechannels", c)
