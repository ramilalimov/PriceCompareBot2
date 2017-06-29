def fGetDialogStatus(idUser):
    idUser = int(idUser)
    from dtb_functions import fExecute
    res = fExecute("SELECT iStatus FROM tblDialogStatus WHERE idUser = " + str(idUser))
    return int(res[0][0]) if len(res) > 0 and res[0][0] is not None else None


def fSetDialogStatus(idUser, iStatus):
    idUser = int(idUser)
    from dtb_functions import fExecute, fGetSql
    if len(fExecute("SELECT iStatus FROM tblDialogStatus WHERE idUser = " + fGetSql(idUser, 'INT'))) > 0:
        res = fExecute("UPDATE tblDialogStatus SET iStatus = " + fGetSql(iStatus, 'INT') + " WHERE idUser = " + fGetSql(idUser, 'INT'))
    else:
        res = fExecute("INSERT INTO tblDialogStatus VALUES (" + fGetSql(idUser, 'INT') + ", " + fGetSql(iStatus, 'INT') + ")")
    return

