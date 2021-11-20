import sqlite3

DATABASE = "fxman.db"


class Database:

    def __init__(self):
        self.db_connection = sqlite3.connect(DATABASE)
        cursor = self.db_connection.cursor()
        cursor.execute("pragma journal_mode = WAL")
        cursor.execute("pragma synchronous = normal ")
        cursor.execute("pragma temp_store = memory ")
        cursor.execute("pragma mmap_size = 50000000")
        self.create_tables()

    def get_db_conn(self):
        return self.db_connection

    def create_tables(self):
        tables = [
            # """DROP TABLE IF EXISTS accounts""",
            # """DROP TABLE IF EXISTS deals""",
            # """DROP INDEX IF EXISTS idx_deal_ticket_number""",
            # """DROP TABLE IF EXISTS positions""",
            # """DROP INDEX IF EXISTS idx_position_ticket_number""",
            # """DROP TABLE IF EXISTS statistic""",
            # """DROP TABLE IF EXISTS status""",
            # """DROP TABLE IF EXISTS sentiments""",
            # """DROP TABLE IF EXISTS signals""",
            # """DROP TABLE IF EXISTS tas""",
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
            """CREATE TABLE IF NOT EXISTS statistic(
                    number INTEGER NOT NULL,                  
                    date TEXT NOT NULL,
                    profit REAL NOT NULL DEFAULT 0.0,
                    balance REAL NOT NULL DEFAULT 0.0,
                    percent REAL NOT NULL DEFAULT 0.0,
                    growth REAL NOT NULL DEFAULT 0.0,
                    UNIQUE(number, date)
                )            
            """,
            """CREATE TABLE IF NOT EXISTS status(
                    number TEXT NOT NULL PRIMARY KEY,  
                    online INTEGER NOT NULL DEFAULT 0,                    
                    error INTEGER NOT NULL DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )            
            """,
            """CREATE TABLE IF NOT EXISTS sentiments(
                    site TEXT NOT NULL,
                    symbol TEXT NOT NULL,  
                    sentiment INTEGER NOT NULL DEFAULT 0,
                    contrarian INTEGER NOT NULL DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    date TEXT NOT NULL DEFAULT '',
                    UNIQUE(site, symbol, date)
                )            
            """,
            """CREATE INDEX IF NOT EXISTS idx_sentiment ON sentiments(site, symbol, date)""",
            """CREATE TABLE IF NOT EXISTS tas(
                    symbol TEXT NOT NULL,  
                    interval TEXT NOT NULL,
                    ma INTEGER NOT NULL DEFAULT 0,
                    os INTEGER NOT NULL DEFAULT 0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    UNIQUE(symbol, interval)
                )            
            """,
            """CREATE INDEX IF NOT EXISTS idx_tas_interval_symbol ON tas(symbol, interval)""",
            """CREATE TABLE IF NOT EXISTS signals(
                    number TEXT NOT NULL,
                    symbol TEXT NOT NULL,  
                    type INTEGER NOT NULL DEFAULT 0,
                    risk INTEGER NOT NULL DEFAULT 0,
                    open_price REAL NOT NULL DEFAULT 0.0,
                    current_price REAL NOT NULL DEFAULT 0.0,
                    max_price REAL NOT NULL DEFAULT 0.0,
                    min_price REAL NOT NULL DEFAULT 0.0,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                    datehour TEXT NOT NULL DEFAULT '',
                    UNIQUE(number, symbol, type, datehour)
                )            
            """,
            """CREATE INDEX IF NOT EXISTS idx_signals_symbol ON signals(symbol)""",
            """CREATE TRIGGER IF NOT EXISTS update_max_price
               AFTER UPDATE ON signals
               WHEN new.current_price > old.max_price
                BEGIN
                   UPDATE signals SET max_price = current_price WHERE symbol = new.symbol;
                END;
            """,
            """CREATE TRIGGER IF NOT EXISTS update_min_price
               AFTER UPDATE ON signals
               WHEN new.current_price < old.min_price
                BEGIN
                   UPDATE signals SET min_price = current_price WHERE symbol = new.symbol;
                END;
            """
        ]
        db_conn = self.get_db_conn()
        cursor = db_conn.cursor()
        for table in tables:
            cursor.execute(table)
        db_conn.commit()
        print("Tables created!")
