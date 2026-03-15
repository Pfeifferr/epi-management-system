import pymysql

# 1. Faz o disfarce PRIMEIRO
pymysql.install_as_MySQLdb()

# 2. AGORA importa o disfarce para mudar a versão
import MySQLdb # type: ignore
MySQLdb.version_info = (2, 2, 1, 'final', 0)