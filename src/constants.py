from src.stage import Stage

SCREEN = (800, 600)
SCREENX, SCREENY = SCREEN

CITYX1, CITYX2 = 224, SCREENX-25
CITYY1, CITYY2 = 49, SCREENY-59

DISINF_APPEAR, DISINF_URGENT, DISINF_DEAD = 5, 8, 10

WAREHOUSE_POS = (SCREENX//2, SCREENY//2)

STAGES = []
STAGES.append( Stage(0, 0, None, 0, 0, False, None) )
STAGES.append( Stage(8, 8, 'naolejuj rikšu', 0, 1, False, 'Máš dosť peňazí na to, aby si naolejoval(a) rikši prevody.') )
STAGES.append( Stage(12, 9, 'lepšie prevody', 0, 1, False, 'Prenajmi si rikšu s lepšou prehadzovačkou.') )
STAGES.append( Stage(20, 12, 'väčší vozík', 0, 3, False, 'S väčším vozíkom vieš doručiť viac tovaru.') )
STAGES.append( Stage(100, 30, 'brigádnik', 0, 20, True, 'Zaplať brigádnika, čo bude šľapať namiesto teba.') )
STAGES.append( Stage(220, 110, 'reklamné letáky', 0, 10, False, 'Letáková kampaň pritiahne viac zákazníkov.') )
STAGES.append( Stage(4000, 300, 'motorikše', 0, 1, False, 'Vybav rikše pomocným motorom.') )
STAGES.append( Stage(10**15, 1000, 'sterilný bunker', 0, 1, True, 'TVOJ SEN: v sterilnom bunkri si netreba dezinfikovať ruky!') )
STAGES.append( Stage(10000, 3000, 'dodávka', 0, 50, True, 'Investuj do svojej prvej dodávky.') )
STAGES.append( Stage(18000, 9000, 'logistika', 0, 1, False, 'Logistické centrum naplánuje optimálnu cestu pre rozvoz.') )
STAGES.append( Stage(22000, 11000, 'lepšie balenie', 0, 3, False, 'Vďaka úspornejšiemu baleniu obslúžime viac klientov jednou jazdou.') )
STAGES.append( Stage(120000, 30000, 'airdrop', 0, 20, True, 'Zhadzuj tovar z lietadla.') )
STAGES.append( Stage(450000, 95000, 'palivové nádrže', 0, 5, False, 'Udrž lietadlá dlhšie vo vzduchu.') )
STAGES.append( Stage(15 * 10**6, 500000, 'klonovanie', 0, 1, False, 'Preži aj smrť vďaka klonovacím technológiám.') )
STAGES.append( Stage(30 * 10**6, 14 * 10**6, 'miniaturizácia', 0, 1, False, 'Miniaturizovaného tovaru sa dá doručiť viac.') )
STAGES.append( Stage(25 * 10**7, 25 * 10**6, 'teleport', 0, 7, True, 'Teleportuj tovar ľuďom do domov.') )
STAGES.append( Stage(10**9, 2 * 10**8, 'zrýchli teleport', 0, 5, False, '') )
STAGES.append( Stage(10**9, 2 * 10**8, 'zväčši teleport', 0, 5, False, 'Investuj do zrýchlenia alebo zväčšenia teleportačnej technológie.') )
STAGES.append( Stage(33 * 10**9, 3 * 10**9, 'masívna reklama', 0, 1, False, 'Každý musí vidieť našu reklamu!') )
STAGES.append( Stage(333 * 10**9, 77 * 10**9, 'replikátor', 0, 7, True, 'Vyrábaj tovar priamo u ľudí doma.') )
STAGES.append( Stage(4 * 10**12, 10**12, 'zväčši replikátor', 0, 7, False, '') )
STAGES.append( Stage(6 * 10**12, 10**12, 'zrýchli replikátor', 0, 3, False, 'Investuj do zväčšenia alebo zrýchlenia replikačnej technológie.') )
STAGES.append( Stage(97 * 10**12, 12 * 10**12, 'reklama do hlavy', 0, 1, False, 'Vysielaj reklamu priamo do hláv zákazníkov.') )

STAGE_OIL = 1
STAGE_GEARS = 2
STAGE_BIGGER = 3
STAGE_INTERN = 4
STAGE_ADS = 5
STAGE_MOTO = 6
STAGE_STERILE = 7
STAGE_VAN = 8
STAGE_LOGISTICS = 9
STAGE_PACKING = 10
STAGE_AIRDROP = 11
STAGE_FUELTANK = 12
STAGE_CLONE = 13
STAGE_SHRINK = 14
STAGE_TELEPORT = 15
STAGE_FASTER_TELEPORT = 16
STAGE_BIGGER_TELEPORT = 17
STAGE_MASSIVE_ADS = 18
STAGE_REPLICATOR = 19
STAGE_BIGGER_REPLICATOR = 20
STAGE_FASTER_REPLICATOR = 21
STAGE_HUMUNGOUS_ADS = 22

FINGERPRINT = [ STAGE_INTERN, STAGE_STERILE, STAGE_VAN, STAGE_AIRDROP, STAGE_TELEPORT, STAGE_REPLICATOR ]

MENU_NEW_GAME = 1
MENU_CONTINUE_GAME = 2
MENU_INSTRUCTIONS = 3

MESSAGE_WELCOME = 'Vitaj!'
MESSAGE_PICK_UP_GOODS = 'Choď do skladu po tovar!'
MESSAGE_DELIVER_GOODS = 'Doruč tovar zákazníkovi!'
MESSAGE_FIRST_BLOOD = 'Výborne, zarobil(a) si jedno euro.'
MESSAGE_DISINFECT = 'Kliknutím na tlačidlo vpravo hore si dezinfikuj ruky.'
MESSAGE_DISINFECT_URGENT = 'Kliknutím na tlačidlo vpravo hore si dezinfikuj ruky. Rýchlo!'

COLOR_BLACK = (0, 0, 0, 1)
COLOR_DISABLED = (0.7, 0.7, 0.7, 1)
COLOR_LIGHTGRAY = (0.9, 0.9, 0.9, 1)
COLOR_URGENT_BG = (0.9, 0.8, 0.8, 1)
COLOR_URGENT_FG = (1, 0.1, 0.1, 1)
COLOR_WHITE = (1, 1, 1, 1)

