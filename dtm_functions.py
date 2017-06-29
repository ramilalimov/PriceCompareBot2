# coding: utf-8
# линейный процессор//каждый объект делает правильно единственную задачу
def fGetCurrentSessionTable(idUser):
    #hypothesis:: if is none, then go to select current session
    idUser = int(idUser)
    from dtb_functions import fExecute
    res = fExecute('SELECT sCurrentSessionTable FROM tblCurrentInsertSessions WHERE idUser = ' + str(idUser))
    return str(res[0][0]) if len(res) > 0 and res[0][0] is not None else None


def fSetCurrentSessionTable(idUser, sSession):
    from dtb_functions import fExecute, fGetSql
    res = fExecute("SELECT sCurrentSessionTable FROM tblCurrentInsertSessions WHERE idUser = " + fGetSql(idUser, 'INT'))
    if len(res) > 0:
        res = fExecute("UPDATE tblCurrentInsertSessions SET sCurrentSessionTable = " + fGetSql(sSession, 'TEXT') + " WHERE idUser = " + fGetSql(idUser, 'INT'))
    else:
        res = fExecute("INSERT INTO tblCurrentInsertSessions VALUES (" + fGetSql(idUser, 'INT') + ", " + fGetSql(sSession, 'TEXT') + ")")
    return sSession


def fGetSessionStatus(sSessionTable):
    from dtb_functions import fExecute
    res = fExecute("SELECT iStatus FROM tblInsertSessionsStatus WHERE sSessionTable = '" + str(sSessionTable) + "'")
    return int(res[0][0]) if len(res) > 0 and res[0][0] is not None else None


def fSetSessionStatus(sSessionTable, iValue):
    from dtb_functions import fExecute, fGetSql
    res = fExecute("SELECT iStatus FROM tblInsertSessionsStatus WHERE sSessionTable = " + fGetSql(sSessionTable, 'TEXT'))
    if len(res) > 0:
        res = fExecute("UPDATE tblInsertSessionsStatus SET iStatus = " + fGetSql(iValue, 'INT') + " WHERE sSessionTable = " + fGetSql(sSessionTable, 'TEXT'))
    else:
        res = fExecute("INSERT INTO tblInsertSessionsStatus VALUES (" + fGetSql(sSessionTable, 'TEXT') + ", " + fGetSql(iValue, 'INT') + ")")
    return iValue


def fCreateTempFillTable(idUser):
    idUser = int(idUser)
    from dtb_functions import fExecute
    sTblName = 'temp_TblToFill_' + str(int(idUser))
    arr_records = fExecute("SELECT name FROM sqlite_master WHERE name LIKE '" + sTblName + "%'")
    iTblIndex = len(arr_records)
    s_iIndexes = set([0])
    s_iIndexes1 = set([1])
    i = 0
    for arr_record in arr_records:
        i = int(arr_record[0].replace(sTblName + '_', ''))
        s_iIndexes.add(i)
        s_iIndexes1.add(i+1)
    iTblIndex = 0 if iTblIndex == 0 else list(s_iIndexes1.difference(s_iIndexes))[0]
    sTblName = sTblName + '_' + str(iTblIndex)
    fExecute('CREATE TABLE ' + sTblName + ' (idUser int' +
                                                ', idSession' +
                                                ', dDate DATETIME' +
                                                ', idNetwork INT' +
                                                ', idProductGroup INT' +
                                                ', idProduct INT' +
                                                ', idTrademark INT' +
                                                ', sParam1 TEXT' +
                                                ', sParam2 TEXT' +
                                                ', sParam3 TEXT' +
                                                ', fPrice REAL)')
    if len(fExecute('SELECT idUser FROM tblCurrentInsertSessions WHERE idUser = ' + str(idUser))) == 0:
        res = fExecute('INSERT INTO tblCurrentInsertSessions VALUES (' + str(idUser) + ', NULL)')
    res = fExecute("UPDATE tblCurrentInsertSessions SET sCurrentSessionTable = '" + sTblName + "' WHERE idUser = " + str(idUser))

    if len(fExecute("SELECT sSessionTable FROM tblInsertSessionsStatus WHERE sSessionTable = '" + str(sTblName) + "'")) == 0:
        res = fExecute("INSERT INTO tblInsertSessionsStatus VALUES ('" + str(sTblName) + "', NULL)")
    res = fExecute("UPDATE tblInsertSessionsStatus SET iStatus = 1 WHERE sSessionTable = '" + str(sTblName) + "'")
    return str(sTblName)


def pDropTempFillTable(sSessionTable):
    sSessionTable = str(sSessionTable)
    from dtb_functions import fExecute, fDropTable
    if len(fExecute("SELECT sCurrentSessionTable FROM tblCurrentInsertSessions WHERE sCurrentSessionTable = '" + sSessionTable + "'")) != 0:
        res = fExecute("UPDATE tblCurrentInsertSessions SET sCurrentSessionTable = NULL WHERE sCurrentSessionTable = '" + sSessionTable + "'")
    res = fExecute("DELETE FROM tblInsertSessionsStatus WHERE sSessionTable = '" + sSessionTable + "'")
    res = fDropTable(sSessionTable)


def pPauseTempFillTable(sSessionTable):
    from dtb_functions import fExecute
    from dtb_functions import fGetSql
    iNRows = int(fExecute("SELECT MAX(rowid) FROM " + fGetSql(sSessionTable, "TEXT"))[0][0])
    if iNRows > 0:
        res = fExecute("DELETE FROM " + sSessionTable + " WHERE fPrice IS NULL AND rowid = " + fGetSql(iNRows, "INT"))
    res = fSetSessionStatus(sSessionTable, None)
    res = fExecute("UPDATE tblCurrentInsertSessions SET sCurrentSessionTable = NULL WHERE sCurrentSessionTable = " + fGetSql(sSessionTable, "TEXT"))
    res = fExecute("UPDATE tblInsertSessionsStatus SET iStatus = 2 WHERE sSessionTable = " + fGetSql(sSessionTable, "TEXT"))
    iNRows = int(fExecute("SELECT COUNT(*) FROM " + fGetSql(sSessionTable, "TEXT"))[0][0])
    if iNRows == 0:
        pDropTempFillTable(sSessionTable)


def pFillTempFillTable(sSessionTable, sValue):
    sSessionTable = str(sSessionTable)
    sValue = str(sValue)
    from dtb_functions import fExecute
    iStatus = fGetSessionStatus(sSessionTable)
    # 0 - таблица дополнена
    # 1 - таблица не коректно занесена
    # 2
    # 3
    # 4
    # 5 - прочая ошибка
    iAnswer = 5
    sidUser = sSessionTable.replace("temp_TblToFill_", "")
    sidSession = sidUser[sidUser.find("_")+1:len(sidUser)]
    sidUser = sidUser[0:sidUser.find("_")]
    if iStatus is None:
        iAnswer = 1
    elif iStatus == 1:
        print type(sSessionTable)
        print type(sidUser)
        print type(sidSession)
        print type(sValue)
        res = fExecute("INSERT INTO " + sSessionTable + " VALUES ("
                       + sidUser + ", "
                       + sidSession + ", "
                       + "date('now'), "
                       + "'"+sValue + "', "
                       + "NULL, "
                       + "NULL, "
                       + "NULL, "
                       + "NULL, "
                       + "NULL, "
                       + "NULL, "
                       + "NULL)"
                       )
    elif iStatus == 2:
        res = fExecute("SELECT idUser FROM " + sSessionTable + " WHERE fPrice IS NULL")
        iNRows = fExecute("SELECT MAX(rowid) FROM " + sSessionTable)
        if len(res) > 0:
            res = fExecute("UPDATE " + sSessionTable + " SET "
                           + "idProductGroup = '" + sValue + "', "
                           + "idProduct = NULL, "
                           + "idTradeMark = NULL, "
                           + "sParam1 = NULL, "
                           + "sParam2 = NULL, "
                           + "sParam3 = NULL"
                           + " WHERE fPrice IS NULL")
        else:
            iNRows = int(fExecute("SELECT MAX(rowid) FROM " + sSessionTable)[0][0])
            res = fExecute("INSERT INTO " + sSessionTable + " SELECT "
                           + "idUser, "
                           + "idSession, "
                           + "dDate, "
                           + "idNetwork, "
                           + "'" + sValue + "', "
                           + "NULL, "
                           + "NULL, "
                           + "NULL, "
                           + "NULL, "
                           + "NULL, "
                           + "NULL "
                           + "FROM " + sSessionTable + " "
                           + "WHERE rowid = " + str(iNRows)
                           )
    elif iStatus == 3:
        res = fExecute("SELECT idUser FROM " + sSessionTable + " WHERE fPrice IS NULL")
        if len(res) > 0:
            res = fExecute("UPDATE " + sSessionTable + " SET "
                           + "idProduct = '" + sValue + "', "
                           + "idTradeMark = NULL, "
                           + "sParam1 = NULL, "
                           + "sParam2 = NULL, "
                           + "sParam3 = NULL"
                           + " WHERE fPrice IS NULL")
        else:
            iNRows = int(fExecute("SELECT MAX(rowid) FROM " + sSessionTable)[0][0])
            res = fExecute("INSERT INTO " + sSessionTable + " SELECT "
                           + "idUser, "
                           + "idSession, "
                           + "dDate, "
                           + "idNetwork, "
                           + "idProductGroup, "
                           + "'" + sValue + "', "
                           + "NULL, "
                           + "NULL, "
                           + "NULL, "
                           + "NULL, "
                           + "NULL "
                           + "FROM " + sSessionTable + " "
                           + "WHERE rowid = " + str(iNRows)
                           )
    elif iStatus == 4:
        res = fExecute("SELECT idUser FROM " + sSessionTable + " WHERE fPrice IS NULL")
        if len(res) > 0:
            res = fExecute("UPDATE " + sSessionTable + " SET "
                           + "idTradeMark = '" + sValue + "', "
                           + "sParam1 = NULL, "
                           + "sParam2 = NULL, "
                           + "sParam3 = NULL"
                           + " WHERE fPrice IS NULL")
        else:
            iNRows = int(fExecute("SELECT MAX(rowid) FROM " + sSessionTable)[0][0])
            res = fExecute("INSERT INTO " + sSessionTable + " SELECT "
                           + "idUser, "
                           + "idSession, "
                           + "dDate, "
                           + "idNetwork, "
                           + "idProductGroup, "
                           + "idProduct, "
                           + "'" + sValue + "', "
                           + "NULL, "
                           + "NULL, "
                           + "NULL, "
                           + "NULL "
                           + "FROM " + sSessionTable + " "
                           + "WHERE rowid = " + str(iNRows)
                           )
    elif iStatus == 5:
        res = fExecute("SELECT idUser FROM " + sSessionTable + " WHERE fPrice IS NULL")
        arr_sValue = sValue.split("..")
        arr_sValue.extend(["NULL", "NULL", "NULL"])
        if len(res) > 0:
            res = fExecute("UPDATE " + sSessionTable + " SET "
                           + "sParam1 = '" + arr_sValue[1] + "', "
                           + "sParam2 = '" + arr_sValue[2] + "', "
                           + "sParam3 = '" + arr_sValue[3] + "', "
                           + "fPrice = replace('" + arr_sValue[0] + "', ',', '.')"
                           + " WHERE fPrice IS NULL")
        else:
            iNRows = int(fExecute("SELECT MAX(rowid) FROM " + sSessionTable)[0][0])
            res = fExecute("INSERT INTO " + sSessionTable + " SELECT "
                           + "idUser, "
                           + "idSession, "
                           + "dDate, "
                           + "idNetwork, "
                           + "idProductGroup, "
                           + "idProduct, "
                           + "idTrademark, "
                           + "'" + arr_sValue[1] + "', "
                           + "'" + arr_sValue[2] + "', "
                           + "'" + arr_sValue[3] + "', "
                           + "replace('" + arr_sValue[0] + "', ',', '.')"
                           + "FROM " + sSessionTable + " "
                           + "WHERE rowid = " + str(iNRows)
                           )
    res = fSetSessionStatus(sSessionTable, iStatus+1 if iStatus < 5 else 4)


def fFillDictionnary(sSession, sValue):
    sSession = str(sSession)
    sValue = str(sValue)
    from dtm_functions import fGetSessionStatus
    from dtb_functions import fExecute, fGetSql
    iStatus = fGetSessionStatus(sSession)
    sTblName = {1: 'dicNetwork', 2: 'dicProductGroup', 3: 'dicProductType', 4: 'dicTrademark', 5: 'dicUnit'}[iStatus]
    res = fExecute("SELECT MAX(rowid) FROM " + sSession)
    iNRows = int(res[0][0]) if len(res) > 0 and res[0][0] is not None else 0
    sAdditionnal = ''
    if iNRows > 0:
        if iStatus == 3:
            res = fExecute("SELECT idProductGroup FROM " + sSession + " WHERE rowid = " + fGetSql(iNRows, 'INT'))
            sAdditionnal = fGetSql(res[0][0], 'INT') if len(res) > 0 and res[0][0] is not None else 'NULL'
            sAdditionnal = ", " + sAdditionnal
        elif iStatus == 4:
            res = fExecute("SELECT idProduct, idTrademark FROM " + sSession + " WHERE rowid = " + fGetSql(iNRows, 'INT'))
            sAdditionnal5 = ''
            sAdditionnal5 = fGetSql(res[0][0], 'INT') if len(res) > 0 and res[0][0] is not None else 'NULL'
            sAdditionnal5 += ", "
            sAdditionnal5 += fGetSql(res[0][1], 'INT') if len(res) > 0 and res[0][1] is not None else 'NULL'
            sAdditionnal5 += ", "
    if iStatus in range(1, 5):
        res = fExecute("INSERT INTO " + sTblName + " VALUES (" + fGetSql(sValue, 'TEXT') + sAdditionnal + ")")
        res = fExecute("SELECT MAX(rowid) FROM " + sTblName)
        iNRows = int(res[0][0]) if len(res) > 0 and res[0][0] is not None else 0
    else:
        iNRows = 0
    if iStatus == 4:    # for iStatus = 5's JOIN
        print "INSERT INTO dicUnit VALUES (" + sAdditionnal5 + ", NULL, NULL, NULL, NULL)"
        res = fExecute("INSERT INTO dicUnit VALUES (" + sAdditionnal5 + " NULL, NULL, NULL, NULL)")
    return iNRows