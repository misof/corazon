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
STAGES.append( Stage(12, 9, 'lepšie prevody', 0, 1, False, '') )
STAGES.append( Stage(20, 12, 'väčší vozík', 0, 3, True, '') )
STAGES.append( Stage(100, 30, 'brigádnik', 1, 20, True, 'Zaplať brigádnika, čo bude šľapať namiesto teba.') )
STAGES.append( Stage(250, 120, 'reklama', 0, 10, False, '') )
STAGES.append( Stage(10**15, 500, 'sterilný office', 0, 1, True, 'V sterilnom office si netreba dezinfikovať ruky.') )
STAGES.append( Stage(4000, 600, 'motorikše', 0, 1, True, '') )
STAGES.append( Stage(10000, 3000, 'dodávka', 0, 50, True, '') )
STAGES.append( Stage(18000, 9000, 'logistika', 0, 1, False, '') )
STAGES.append( Stage(22000, 11000, 'lepšie balenie', 0, 3, False, '') )
STAGES.append( Stage(120000, 30000, 'airdrop', 0, 20, True, '') )
STAGES.append( Stage(450000, 90000, 'palivové nádrže', 0, 5, True, '') )
STAGES.append( Stage(15 * 10**6, 500000, 'miniaturizácia tovaru', 0, 1, False, '') )
STAGES.append( Stage(70 * 10**7, 10**7, 'teleporty', 0, 1, False, '') )
STAGES.append( Stage(10**10, 10**9, 'replikátory', 0, 1, False, '') )

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
STAGE_SHRINK = 13
STAGE_TELEPORT = 14
STAGE_REPLICATOR = 15

MENU_NEW_GAME = 1
MENU_CONTINUE_GAME = 2
MENU_INSTRUCTIONS = 3

