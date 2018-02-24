# 2015.01.14 22:43:00 CET
from live_crc import *
accountPersistentCacheDataScheme = {INCLUDE: {'economics', 'inventory'},
 'stats': {INCLUDE: {'dossier',
                     'eliteVehicles',
                     'unlocks',
                     'vehTypeXP'}}}
accountDataPersistentHash = gen_livehash_fn(accountPersistentCacheDataScheme)
accountDataDelPersistent = gen_delSubkeys_fn(accountPersistentCacheDataScheme)
accountDataMergePersistent = gen_mergeCache_fn(overwrite=False)
accountDataExtractPersistent = gen_extract_fn(accountPersistentCacheDataScheme)

def accountDataGetDiffForPersistent(diff):
    good_keys = {'economics', 'inventory', 'stats'}
    mydiff = {}
    for (k, v,) in diff.items():
        if k in good_keys or isinstance(k, tuple) and k[0] in good_keys:
            mydiff[k] = v

    return mydiff



+++ okay decompyling live_crc_accountdata.pyc 
# decompiled 1 files: 1 okay, 0 failed, 0 verify failed
# 2015.01.14 22:43:00 CET
