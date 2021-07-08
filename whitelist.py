from string import digits
from itertools import chain
import json
import hashlib

flat_file = open('20210707.json')
MF_DATA = json.load(flat_file)
flat_file.close()
DATE = MF_DATA['naglowek']['dataGenerowaniaDanych']
ITER_COUNT = int(MF_DATA['naglowek']['liczbaTransformacji'])
OK_HASHES = MF_DATA['skrotyPodatnikowCzynnych']


def mf_key(nip, nrb):
    key = DATE + nip + nrb
    for _i in range(ITER_COUNT):
        key = hashlib.sha512(key.encode()).hexdigest()
    return key


def mask_match(mask, nrb):
    return all((x[0] not in digits or x[0] == x[1] for x in zip(mask, nrb)))


def mask_nrb(mask, nrb):
    return ''.join((x[1] if x[0] == 'Y' else x[0] for x in zip(mask, nrb)))


with open('20210707.txt') as in_file:
    for in_line in (_l for _l in in_file if _l.strip()):
        clear_l = ''.join((x for x in in_line if x in digits))
        nip, nrb = clear_l[:10], clear_l[10:36]
        print(any(
            (mf_key(nip, l_nrb) in OK_HASHES
             for l_nrb in chain([nrb], (mask_nrb(m, nrb) for m in MF_DATA['maski'] if mask_match(m, nrb))))),
            in_line.strip())
