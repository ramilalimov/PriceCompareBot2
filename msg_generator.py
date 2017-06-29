def msgSessions(idUser):
    from dtb_functions import fExecute, fGetSql
    arr_sSessions = fExecute("SELECT name FROM sqlite_master WHERE name LIKE 'temp_TblToFill_" + str(int(idUser)) + "%'")
    sMsg = ''
    sMsg += 'Choose your session :' + chr(10)
    sMsg += '1. Begin new'
    dict_sCodes = {"1": "new"}
    i = 1
    for sSession in arr_sSessions:
        i = i+1
        res = fExecute('SELECT MAX(b.sName), MAX(a.dDate) FROM ' + fGetSql(sSession[0], "TEXT") + " as a JOIN dicNetwork as b ON a.idNetwork = b.rowid")[0]
        sMsg += chr(10) + str(i) + '. ' + str(res[0]) + " [" + str(res[1]) + "]"
        dict_sCodes.update({str(i): sSession[0]})
    return {'sMsg': sMsg, 'dict_sCodes': dict_sCodes}

def msgInsertField(sSession):
    sSession = str(sSession)
    sMsg = "Price XX.XX"
    dict_sCodes = {}
    from dtm_functions import fGetSessionStatus
    from dtb_functions import fExecute, fGetSql
    iStatus = fGetSessionStatus(sSession)
    sFieldName = {1: 'Shop/Network', 2: 'Product Group', 3: 'product to Product Group', 4: 'Trademark', 5: None}[iStatus]
    sTblName = {1: 'dicNetwork', 2: 'dicProductGroup', 3: 'dicProductType', 4: 'dicTrademark', 5: None}[iStatus]
    res = fExecute("SELECT MAX(rowid) FROM " + sSession)
    iNRows = int(res[0][0]) if len(res) > 0 and res[0][0] is not None else 0
    sFilter = ''
    if iNRows > 0:
        if iStatus == 3:
            res = fExecute("SELECT idProductGroup FROM " + sSession + " WHERE rowid = " + fGetSql(iNRows, 'INT'))
            sFilter = 'WHERE idProductGroup = ' + fGetSql(res[0][0], 'INT') if len(res) > 0 and res[0][0] is not None else ''
    if iStatus in range(1, 5):
        arr_sValues = fExecute("SELECT rowid, sName FROM " + sTblName + " " + sFilter)
        sMsg = ''
        sMsg += '1. Add new ' + sFieldName
        dict_sCodes = {"1": "add"}
        i = 1
        for sValue in arr_sValues:
            i = i+1
            sMsg += chr(10) + str(i) + '. ' + sValue[1]
            dict_sCodes.update({str(i): sValue[0]})
    elif iStatus == 5:
        if iNRows > 0:
            res = fExecute("SELECT a.sParamAmount, a.sParam1, a.sParam2, a.sParam3 FROM dicUnit as a JOIN " + sSession + " as b on a.idProduct = b.idProduct and a.idTradeMark = b.idTrademark")
            if len(res) > 0:
                sMsg += ".."
                sMsg += res[0][0] if res[0][0] is not None else ''
                sMsg += ".."
                sMsg += res[0][1] if res[0][1] is not None else ''
                sMsg += ".."
                sMsg += res[0][2] if res[0][2] is not None else ''
                sMsg += ".."
                sMsg += res[0][3] if res[0][3] is not None else ''
                dict_sCodes = {}
    return {'sMsg': sMsg, 'dict_sCodes': dict_sCodes}
