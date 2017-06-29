# файл dtm_functions - функции, работающие с потоками данных

# таблица с текущими сессиями
from dtb_functions import fExecute, fSelect
# Исходные таблицы
fExecute("CREATE TABLE dicProductGroup (sName TEXT)")
fExecute("CREATE TABLE dicNetwork (sName TEXT)")
fExecute("CREATE TABLE dicProductType (sName TEXT, idProductGroup INTEGER)")
fExecute("CREATE TABLE dicTrademark (sName TEXT)")
fExecute("CREATE TABLE dicUnit (idProduct INTEGER, idTrademark INTEGER, sParamAmount TEXT, sParam1 TEXT, sParam2 TEXT, sParam3 TEXT)")
fExecute("CREATE TABLE tblOptionsParam (sPAram TEXT, sValue TEXT)")
#наполнение:
fExecute("INSERT INTO tblOptionsPAram VALUES ('idUpdate', '0')")

# текущие сессии
fExecute("CREATE TABLE tblCurrentInsertSessions (idUser INT, sCurrentSessionTable TEXT)")

# Таблица со статусами сессий:
#
#   0 меню сессии
#   1 запрос: меню сети
#   2 запрос: меню секции
#   3 запрос: меню типа продукта
#   4 запрос: меню брэнда
#   5 запрос: комплектация и запись
fExecute('CREATE TABLE tblInsertSessionsStatus (sSessionTable TEXT, iStatus INT)')

#меню состояния диалога:
fExecute("CREATE TABLE tblDialogStatus (idUser int, iStatus int)")