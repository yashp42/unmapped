import socket
import ssl

hosts = [
    'ac-7gpc8bh-shard-00-00.umzi7be.mongodb.net',
    'ac-7gpc8bh-shard-00-01.umzi7be.mongodb.net',
    'ac-7gpc8bh-shard-00-02.umzi7be.mongodb.net',
]

contexts = [
    ('default', ssl.create_default_context()),
]

try:
    contexts.append(('TLSv1_2', ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)))
except Exception:
    pass

try:
    contexts.append(('TLSv1_3', ssl.SSLContext(ssl.PROTOCOL_TLSv1_3)))
except Exception:
    pass

try:
    legacy = ssl.create_default_context()
    legacy.options |= ssl.OP_LEGACY_SERVER_CONNECT
    contexts.append(('legacy', legacy))
except Exception:
    pass

try:
    insecure = ssl.create_default_context()
    insecure.check_hostname = False
    insecure.verify_mode = ssl.CERT_NONE
    contexts.append(('insecure', insecure))
except Exception:
    pass

for h in hosts:
    print('----', h, '----')
    try:
        addrs = socket.getaddrinfo(h, None)
        print('DNS:', {addr[4][0] for addr in addrs})
    except Exception as e:
        print('DNS error:', repr(e))

    try:
        with socket.create_connection((h, 27017), timeout=5) as sock:
            print('TCP connect: ok')
    except Exception as e:
        print('TCP connect error:', repr(e))

    for name, ctx in contexts:
        print('testing SSL context:', name)
        try:
            with ctx.wrap_socket(socket.socket(socket.AF_INET), server_hostname=h) as ssock:
                ssock.settimeout(5)
                ssock.connect((h, 27017))
                print('  SSL handshake: ok')
                print('  SSL cipher:', ssock.cipher())
        except Exception as e:
            print('  SSL handshake error:', repr(e))
    print()
