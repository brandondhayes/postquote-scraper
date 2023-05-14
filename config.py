##########################################
# Since the forum isn't public, we want
# to use the credentials of a logged
# in user while scraping content
# NOTE: the cookie variables have been
# anonymized for privacy
##########################################

headers = {
    'Host':                         'forums.example.com',
    'User-Agent':                   'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/112.0',
    'Accept':                       'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language':              'en-US,en;q=0.5',
    'Accept-Encoding':              'gzip, deflate, br',
    'Connection':                   'keep-alive',
    'Cookie':                       'vbulletin_collapse=bb_password=a94a8fe5ccb19ba61c4c0873d391e987982fbbd3; bb_lastvisit=1672670345; bb_lastactivity=0; bb_userid=5472; bb_sessionhash=082f4f9e3f8a4f1bcb4c4fb4b161df8e;',
    'Upgrade-Insecure-Requests':    '1',
    'Sec-Fetch-Dest':               'document',
    'Sec-Fetch-Mode':               'navigate',
    'Sec-Fetch-Site':               'cross-site',
    'Sec-Fetch-User':               '?1',
    'Pragma':                       'no-cache',
    'Cache-Control':                'no-cache'
}