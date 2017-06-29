#   =====================================================
#       rollback block
#   =====================================================
from dtb_functions import fSelect, fExecute
from dtm_functions import pDropTempFillTable
for i in fSelect('sqlite_master'):
    if i[1].find('temp_TblToFill_')>-1:
        print i[1]
        pDropTempFillTable(i[1])

from dlg_functions import fGetDialogStatus, fSetDialogStatus
print fGetDialogStatus(104739991)
print fGetDialogStatus(212821593)
fSetDialogStatus(104739991, None)
fSetDialogStatus(212821593, None)

from bot_functions import fGetUpdates,  fSetIdUpdate
for i in fGetUpdates(0): print i['idUpdate']
for i in fGetUpdates(0): fSetIdUpdate(i['idUpdate'])

fSetIdUpdate(119910354)

fExecute("DELETE FROM dicNetwork")
fExecute("DELETE FROM dicProductGroup")
fExecute("DELETE FROM dicProductType")
fExecute("DELETE FROM dicTrademark")
fExecute("DELETE FROM dicUnit")

#   =====================================================
#       garbage
#   =====================================================
from dtm_functions import fGetCurrentSessionTable
from msg_generator import msgInsertField
print msgInsertField(fGetCurrentSessionTable(212821593))['sMsg']



from dtb_functions import fSelect
for i in fSelect('tblCurrentInsertSessions'): print i

from dtb_functions import fSelect
for i in fSelect('tblInsertSessionsStatus'): print i

from dtb_functions import fSelect
for i in fSelect('sqlite_master'): print i[4]

from dtb_functions import fSelect
for i in fSelect('temp_TblToFill_212821593_0'): print i

from bot_functions import fGetUpdates
print fGetUpdates(0)

from bot_functions import fSetIdUpdate
fSetIdUpdate(119910314)





from dtm_functions import pCreateTempFillTable
pCreateTempFillTable(212821593)


from dtm_functions import pFillTempFillTable
from dtb_functions import fSelect
pFillTempFillTable('temp_TblToFill_212821593_1', '')
for i in fSelect('tblCurrentInsertSessions'): print i
for i in fSelect('tblInsertSessionsStatus'): print i
fSelect('temp_TblToFill_212821593_1 WHERE rowid=1')[0]


#   temp_TblToFill_212821593_1 212821593
#   temp_TblToFill_104739991_0 104739991
from msg_generator import msgInsertField
msgInsertField('temp_TblToFill_212821593_0')

