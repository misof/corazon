from stage import Stage

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
STAGES.append( Stage(20, 12, 'väčší vozík', 0, 3, True, 'S väčším vozíkom vieš doručiť viac tovaru.') )
STAGES.append( Stage(100, 30, 'brigádnik', 1, 20, True, 'Zaplať brigádnika, čo bude šľapať namiesto teba.') )
STAGES.append( Stage(250, 120, 'reklamné letáky', 0, 10, False, 'Letáková kampaň pritiahne viac zákazníkov.') )
STAGES.append( Stage(10**15, 500, 'sterilný office', 0, 1, True, 'V sterilnom office si netreba dezinfikovať ruky.') )
STAGES.append( Stage(4000, 600, 'motorikše', 0, 1, True, 'Prenajmi rikše s motorom.') )
STAGES.append( Stage(10000, 3000, 'dodávka', 0, 50, True, 'Investuj do svojej prvej dodávky.') )
STAGES.append( Stage(18000, 9000, 'logistika', 0, 1, False, 'Logistické centrum efektívnejšie plánuje rozvoz.') )
STAGES.append( Stage(22000, 11000, 'lepšie balenie', 0, 3, False, 'Vďaka úspornejšiemu baleniu obslúžime viac klientov.') )
STAGES.append( Stage(120000, 30000, 'airdrop', 0, 20, True, 'Zhadzuj tovar z lietadla.') )
STAGES.append( Stage(450000, 90000, 'palivové nádrže', 0, 5, True, 'Udrž lietadlá dlhšie vo vzduchu.') )
STAGES.append( Stage(15 * 10**6, 500000, 'klonovanie', 0, 1, False, 'Preži aj smrť vďaka klonovacím technológiám.') )
STAGES.append( Stage(30 * 10**6, 14 * 10**6, 'miniaturizácia', 0, 1, False, 'Miniaturizovaného tovaru sa dá doručiť viac.') )
STAGES.append( Stage(25 * 10**7, 25 * 10**6, 'teleporty', 0, 1, False, 'Teleportuj tovar ľuďom do domov.') )
STAGES.append( Stage(10**10, 10**9, 'replikátory', 0, 1, False, 'Vyrábaj tovar priamo u ľudí doma.') )

STAGE_OIL = 1
STAGE_GEARS = 2
STAGE_BIGGER = 3
STAGE_INTERN = 4
STAGE_ADS = 5
STAGE_STERILE = 6
STAGE_MOTO = 7
STAGE_VAN = 8
STAGE_LOGISTICS = 9
STAGE_PACKING = 10
STAGE_AIRDROP = 11
STAGE_FUELTANK = 12
STAGE_CLONE = 13
STAGE_SHRINK = 14
STAGE_TELEPORT = 15
STAGE_REPLICATOR = 16

MENU_NEW_GAME = 1
MENU_CONTINUE_GAME = 2
MENU_INSTRUCTIONS = 3

MESSAGE_WELCOME = 'Vitaj!'
MESSAGE_PICK_UP_GOODS = 'Choď do skladu po tovar!'
MESSAGE_DELIVER_GOODS = 'Doruč tovar zákazníkovi!'
MESSAGE_FIRST_BLOOD = 'Výborne, zarobil(a) si jedno euro.'
MESSAGE_DISINFECT = 'Kliknutím na button vpravo hore si dezinfikuj ruky.'
MESSAGE_DISINFECT_URGENT = 'Kliknutím na button vpravo hore si dezinfikuj ruky. Rýchlo!'

