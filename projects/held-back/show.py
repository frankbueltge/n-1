import json, sys, re
from pageread import entry
NO = {'CERD': 'IV-2', 'ICESCR': 'IV-3', 'ICCPR': 'IV-4', 'CEDAW': 'IV-8', 'CAT': 'IV-9', 'CRC': 'IV-11', 'CRMW': 'IV-13', 'CRPD': 'IV-15'}
def main():
  items = json.load(open('sheet.json'))['items']
  for it in items[int(sys.argv[1]) - 1:int(sys.argv[2])]:
    print('\n########', it)
    out, res = entry(NO[it['treaty']], it['state'])
    txt = '\n'.join(t for _, t, _ in out if t) + '\n' + '\n'.join('[note %s] %s' % r for r in res)
    print(txt[:int(sys.argv[3]) if len(sys.argv) > 3 else 3500])

if __name__ == '__main__':
  main()
