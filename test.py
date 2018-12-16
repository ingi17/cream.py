import re
season = re.findall(r'^(\d{1})\d{2}[^\d]', 'Klovn - 205') # 3 tölur í byrjun strengs

season = re.findall(r'[^\d](\d{1})\d{2}$', 'Klovn - 205') # 3 tölur í miðju strengs
print(season)
season = re.findall(r'^(\d{2})\d{2}[^\d]', '0101 - My First Day') # 4 tölur í byrjun strengs
season = re.findall(r'[^\d](\d{2})\d{2}[^\d]', 'Adventures In Babysitting 1987 DvDrip[Eng]-greenbud1969') # 4 tölur í miðju strengs
season = re.findall(r'season (i+)', 'QI XL season iii Episode 12 Illumination.avi')
season[0] = len(season[0])
season = 'Season ' + "{:02d}".format(int(season[0]))
season = re.findall(r'[^\d](\d{1,2}).\d{1,2}[^\d]', '30 Rock [2.01] SeinfeldVision')

#season = re.findall(r'\s([00-18])\d{2}\s', 'Adventures In Babysitting 1987 DvDrip[Eng]-greenbud1969')
season = re.findall(r'[^\d]([0-1][0-8])\d{2}[^\d]', 'Seinfeld 1987 The Caddy')
print(season)