SUPPORTED_DIALECTS = (
    'mysql',
    'postgresql',
    'sqlite'
)

SUPPORTED_DB_DRIVERS = {
    'mysql': (
        'mysqlconnector',
        'pymysql',
        # not tested properly
        'pyodbc',
    ),
    'postgresql': (
        'psycopg2',
        'pg8000',
        'pygresql',
    )
}
