import socket
import ssl
import redirecturl
# http/2 check with h2c
def checkH2(domain):
    # send GET request with the upgrade headers
    try:
        r = redirecturl.getURL(domain);
    # except ConnectionError:
    except IOError:
        #response = "Failed to open URL"
        return 2
    else:
        # check the status code if it is 101 Switching Protocols based on http1.1 first
        if r.status_code == 101:
            return 0
            #response = 'This domain supports HTTP/2 with h2c - HTTP'
        # the status code must be 200 ok or something else based on http1.1 if the server does not support http/2
        else:
            return 1
            #response = 'This domain does not support HTTP/2 with h2c - HTTP'


# http/2 check with h2
def checkH2S(domain):
    # create a context for communiation
    ctx = ssl.create_default_context()

    # list up protocol candidates
    ctx.set_alpn_protocols(['h2', 'spdy/3', 'http/1.1'])

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(10)

    # create a socket connection using the context and the fefault https port
    conn = ctx.wrap_socket(sock, server_hostname=domain)

    try:
        conn.connect((domain, 443))
    except ConnectionRefusedError:
        # print('Connection refused error')
        return 5
        #response = 'HTTP/2 test not possible. Host not found or connection refused.'
    except socket.timeout:
        # print('response timeout')
        #response = 'HTTP/2 test not possible. Host not found or connection refused.'
        return 5
    except ssl.CertificateError:
        # print(ssl.CertificateError)
        return 5
        #response = 'HTTP/2 test not possible. Host not found or connection refused.'
    except ssl.SSLError:
        return 5
        # print(ssl.SSLError)
        #response = 'HTTP/2 test not possible. Host not found or connection refused.'
    except socket.gaierror:
        # print(socket.gaierror)
        return 2
        #response = 'HTTP/2 test not possible. Host not found or connection refused.'
    else:
        # check the selected protocol by the server
        if conn.selected_alpn_protocol() == 'h2':
            return 3
            #response = 'This domain supports HTTP/2 with h2 - HTTPS'
        else:
            return 4
            #response = 'This domain does not support HTTP/2 with h2 - HTTPS but ' + str(conn.selected_alpn_protocol())
    finally:
        conn.close()
