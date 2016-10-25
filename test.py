def application(env, start_response):
    start_reponse('200 OK', [('content-Type', 'text/html')]
    return 'Hello uWSGI'
