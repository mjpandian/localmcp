import sqlite3
from mcp.server.fastmcp import FastMCP

# Initialize FastMCP
mcp = FastMCP("localmcp-sqlite3")

def init_db():
    """Ensure the database and table exist before the server starts."""
    conn = sqlite3.connect("mcp_database.sqlite3")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS data_table (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@mcp.tool()
def add_data(query: str) -> bool:
    """Execute an INSERT query to add a record to the database."""
    try:
        conn = sqlite3.connect("mcp_database.sqlite3")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO data_table (data) VALUES (?)", (query,))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        return f"Error adding data: {str(e)}"

@mcp.tool()
def fetch_data(query: str) -> list:
    """Execute a SELECT query to return records. Pass 'all' or empty string to get everything."""
    conn = sqlite3.connect("mcp_database.sqlite3")
    cursor = conn.cursor()
    
    # If the user asks for 'all', just select everything
    if query.lower() == "all" or query.strip() == "":
        cursor.execute("SELECT data FROM data_table")
    else:
        cursor.execute("SELECT data FROM data_table WHERE data LIKE ?", ('%' + query + '%',))
    
    results = [row[0] for row in cursor.fetchall()]
    conn.close()
    return results

if __name__ == "__main__":
    init_db()
    # Explicitly run as an SSE server on port 8000
    mcp.run(transport="sse")