from Databases.redis.redis_client import r
key = "example"
r.set(key, "1111")
r.delete("timwes21")
print(r.get(key).decode())