# coding: utf-8
def vPriceCompareBot2 ():
    from bot_functions import fStartBot, fGetUpdates, fGetIdUpdate, fSetIdUpdate
    from dtm_functions import fGetCurrentSessionTable, fSetSessionStatus, fGetSessionStatus, fCreateTempFillTable, pFillTempFillTable, fFillDictionnary, pPauseTempFillTable
    from dlg_functions import fGetDialogStatus, fSetDialogStatus
    from msg_generator import msgInsertField, msgSessions
    arr_msg = fGetUpdates(fGetIdUpdate()+1)
    for msg in arr_msg:
        sSession = fGetCurrentSessionTable(idUser=msg['idUser'])
        iStatus = fGetDialogStatus(msg['idUser'])
        # Computing pre-defined commands/status
        bRunAskAnswerSysthem = 0
        if msg['sText'].lower()[0:4] == 'test':
            fStartBot().sendMessage(msg['idChat'], msg['sText'])
            bRunAskAnswerSysthem = 0
        elif msg['sText'].lower() == "..":
            if sSession is None:
                fStartBot().sendMessage(msg['idChat'], msgSessions(msg['idUser'])['sMsg'])
                fSetDialogStatus(msg['idUser'], 1)
            else:
                iStatus = fGetSessionStatus(sSession)
                if iStatus in [0, 1]:
                    pPauseTempFillTable(sSession)
                    fStartBot().sendMessage(msg['idChat'], msgSessions(msg['idUser'])['sMsg'])
                    fSetDialogStatus(msg['idUser'], 1)
                elif iStatus in [2, 3, 4, 5]:
                    fSetDialogStatus(msg['idUser'], None)
                    fSetSessionStatus(sSession, iStatus - 1)
                    fStartBot().sendMessage(msg['idChat'], msgInsertField(sSession)['sMsg'])
        elif msg['sText'].lower() == "...":
            if sSession is not None:
                pPauseTempFillTable(sSession)
                fStartBot().sendMessage(msg['idChat'], msgSessions(msg['idUser'])['sMsg'])
            fSetDialogStatus(msg['idUser'], 0)
        else:
            if sSession is None:
                if iStatus == 1:
                    sSession = msgSessions(msg['idUser'])['dict_sCodes'][msg['sText'].split(' ')[0]]
                    if sSession.upper() == 'NEW':
                        sSession = fCreateTempFillTable(msg['idUser'])
                    fSetDialogStatus(msg['idUser'], None)
                    fStartBot().sendMessage(msg['idChat'], 'Session ' + sSession + ' is running')
                    fStartBot().sendMessage(msg['idChat'], msgInsertField(sSession)['sMsg'])
                else:
                    fStartBot().sendMessage(msg['idChat'], msgSessions(msg['idUser'])['sMsg'])
                    fSetDialogStatus(msg['idUser'], 1)
            else:
                if iStatus == 1:
                    #   ... TO FILL ...
                    sValue = fFillDictionnary(sSession, msg['sText'])
                    fSetDialogStatus(msg['idUser'], None)
                else:
                    dict_sCodes = msgInsertField(sSession)['dict_sCodes']
                    sValue = dict_sCodes[msg['sText'].split(' ')[0]] if len(dict_sCodes) > 0 else msg['sText']
                    if str(sValue).upper() == 'ADD' and len(dict_sCodes) > 0:
                        sNewName = msg['sText'].split(" ")
                        if len(sNewName) > 1 and sNewName[1] is not None:
                            #   ... TO FILL ...
                            sValue = fFillDictionnary(sSession, sNewName[1])
                        else:
                            fSetDialogStatus(msg['idUser'], 1)
                            fStartBot().sendMessage(msg['idChat'], 'Waiting for your input')
                if fGetDialogStatus(msg['idUser']) != 1:
                    pFillTempFillTable(sSession, sValue)
                    fStartBot().sendMessage(msg['idChat'], msgInsertField(sSession)['sMsg'])
        idUpdate = msg['idUpdate'] if msg['idUpdate'] >= fGetIdUpdate() else fGetIdUpdate()
        fSetIdUpdate(idUpdate)
    return