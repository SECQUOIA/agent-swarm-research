"""(Run as an inline heredoc on 2026-10-01; saved here for the record.)
Re-fetch the four OSIL models and compare with the cache."""
import urllib.request, time, os
for n in ['eniplac', 'lop97icx', 'spring', 'stockcycle']:
    data = urllib.request.urlopen('https://www.minlplib.org/osil/%s.osil' % n, timeout=60).read()
    old = open(os.path.expanduser('~/.cache/minlplib/minlplib/osil/%s.osil' % n), 'rb').read()
    print(n, 'osil bytes', len(data), 'identical to cache:', data == old)
    time.sleep(1)
