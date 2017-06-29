def fStartBot():
    import telepot
    sToken = '375021608:AAFAYx5mIqcIzBQ0bsEE2jvUXZFjesYIjC8'
    return telepot.Bot(sToken)

def fGetUpdates(idUpdate):
    idUpdate = int(idUpdate)
    botBot = fStartBot()
    arr_upd = botBot.getUpdates(idUpdate)
    arr_Answer = []
    for n in arr_upd:
        arr_Answer.append({'idUpdate': n['update_id']
                              , 'idChat': n['message']['chat']['id']
                              , 'sText': n['message']['text']
                              , 'sUser': n['message']['from']['first_name'] + u' ' + n['message']['from']['last_name']
                              , 'idUser': n['message']['from']['id']
                           })
    return arr_Answer

def fGetIdUpdate():
    from dtb_functions import fExecute
    return int(fExecute("SELECT sValue FROM tblOptionsPAram WHERE sParam='idUpdate'")[0][0])

def fSetIdUpdate(idUpdate):
    from dtb_functions import fExecute
    idUpdate=str(int(idUpdate))
    res=fExecute("UPDATE tblOptionsParam SET sValue = " + idUpdate + " WHERE sParam='idUpdate'")
    return