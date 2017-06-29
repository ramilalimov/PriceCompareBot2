def fsDataBase():
    return 'C:\Users\user\Desktop\Different things\Project_ComparePrices\dtb_pcb'

def fSelect(sTbl):
    import sqlite3
    conn=sqlite3.connect(fsDataBase())
    sQuery=conn.cursor()
    sQuery.execute('SELECT * FROM '+sTbl)
    res=sQuery.fetchall()
    conn.close()
    return res

def fExecute(sRequest):
    import sqlite3
    conn=sqlite3.connect(fsDataBase())
    sQuery=conn.cursor()
    sQuery.execute(sRequest)
    res=sQuery.fetchall()
    conn.commit()
    conn.close()
    return res

def fDropTable(sTbl):
    import sqlite3
    conn=sqlite3.connect(fsDataBase())
    sQuery=conn.cursor()
    sQuery.execute('DROP TABLE IF EXISTS '+sTbl)
    res=sQuery.fetchall()
    conn.commit()
    conn.close()
    return res

def fGetTableInfo(sTbl):
    import sqlite3
    conn=sqlite3.connect(fsDataBase())
    sQuery=conn.cursor()
    sQuery.execute('PRAGMA table_info('+sTbl+')')
    res=sQuery.fetchall()
    conn.close()
    return res


def fGetSql(sString, sType):
    if sString is None:
        sAnswer = 'NULL'
    else:
        sString = str(sString)
        if sType.upper() == 'TEXT':
            sAnswer = "'" + sString + "'"
        else:
            sAnswer = sString
    return sAnswer