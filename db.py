import sqlite3

DATABASE_NAME = "fxman.db"


def get_db():
    conn = sqlite3.connect(DATABASE_NAME)
    return conn


def create_tables():
    tables = [
        # """DROP TABLE IF EXISTS accounts""",
        # """DROP TABLE IF EXISTS deals""",
        # """DROP INDEX IF EXISTS idx_deal_ticket_number""",
        # """DROP TABLE IF EXISTS positions""",
        # """DROP INDEX IF EXISTS idx_position_ticket_number""",
        """CREATE TABLE IF NOT EXISTS accounts(
                number INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                broker TEXT NOT NULL,
                server TEXT NOT NULL,
                deposit REAL NOT NULL DEFAULT 0.0,
                credit REAL NOT NULL DEFAULT 0.0,
                withdraw REAL NOT NULL DEFAULT 0.0,
                balance REAL NOT NULL DEFAULT 0.0,
                equity REAL NOT NULL DEFAULT 0.0,
                margin REAL NOT NULL DEFAULT 0.0,
                deals INTEGER NOT NULL DEFAULT 0,
                netvolume REAL NOT NULL DEFAULT 0.0,
                netprofit REAL NOT NULL DEFAULT 0.0,
                positions INTEGER NOT NULL DEFAULT 0,
                floatvolume REAL NOT NULL DEFAULT 0.0,
                floatprofit REAL NOT NULL DEFAULT 0.0,
                depositload REAL NOT NULL DEFAULT 0.0,
                drawdown REAL NOT NULL DEFAULT 0.0,
                lastupdate TEXT NOT NULL 
            )
        """,
        """CREATE TABLE IF NOT EXISTS deals(
                ticket INTEGER NOT NULL ,  
                number INTEGER NOT NULL,
                time TEXT NOT NULL,
                symbol TEXT NOT NULL, 
                type INTEGER NOT NULL,                       
                volume REAL NOT NULL DEFAULT 0.0,
                price REAL NOT NULL DEFAULT 0.0,
                sl REAL NOT NULL DEFAULT 0.0,
                tp REAL NOT NULL DEFAULT 0.0,
                commission REAL NOT NULL DEFAULT 0.0,
                swap REAL NOT NULL DEFAULT 0.0,
                profit REAL NOT NULL DEFAULT 0.0,
                magic INTEGER NOT NULL DEFAULT 0,
                comment TEXT,
                UNIQUE(ticket, number) 
            )
        """,
        """CREATE INDEX IF NOT EXISTS idx_deal_ticket_number ON deals(ticket, number)""",
        """CREATE TABLE IF NOT EXISTS positions(
                ticket INTEGER NOT NULL ,  
                number INTEGER NOT NULL,
                time TEXT NOT NULL,
                symbol TEXT NOT NULL, 
                type INTEGER NOT NULL,                       
                volume REAL NOT NULL DEFAULT 0.0,
                price REAL NOT NULL DEFAULT 0.0,
                sl REAL NOT NULL DEFAULT 0.0,
                tp REAL NOT NULL DEFAULT 0.0,
                commission REAL NOT NULL DEFAULT 0.0,
                swap REAL NOT NULL DEFAULT 0.0,
                profit REAL NOT NULL DEFAULT 0.0,
                magic INTEGER NOT NULL DEFAULT 0,
                comment TEXT,
                UNIQUE(ticket, number) 
            )
        """,
        """CREATE INDEX IF NOT EXISTS idx_position_ticket_number ON positions(ticket, number)""",
        """CREATE TABLE IF NOT EXISTS sentiments(
                symbol TEXT NOT NULL  PRIMARY KEY,  
                value INTEGER NOT NULL DEFAULT 0
            )
        """,
    ]
    db = get_db()
    cursor = db.cursor()
    for table in tables:
        cursor.execute(table)
