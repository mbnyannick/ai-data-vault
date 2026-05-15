import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify

app = Flask(__name__)

# CONFIGURATION: Pull connection secrets safely or fallback to your raw URI
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:Kobibi09@$$@db.nxgduobaryxomauktmcu.supabase.co:5432/postgres')

def get_db_connection():
    # Establishes a raw transactional bridge to your Supabase PostgreSQL engine
    conn = psycopg2.connect(DATABASE_URL)
    return conn

@app.route('/mcp/<niche_id>', methods=['GET'])
def get_vault_data(niche_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)
        
        # Pull exactly one target row matching the bot query variable instantly
        cur.execute("SELECT niche, telemetry_data, mcp_context FROM niches WHERE id = %s;", (niche_id,))
        tool_data = cur.fetchone()
        
        cur.close()
        
        if tool_data:
            # Wrap the payload inside a clean enterprise machine success dictionary
            response = {"status": "SUCCESS"}
            response.update(tool_data)
            return jsonify(response), 200
        else:
            return jsonify({
                "status": "ERROR", 
                "message": f"Niche identifier '{niche_id}' not found in the 400,000 active master registry."
            }), 404
            
    except Exception as e:
        return jsonify({"status": "ERROR", "message": "Database query connection timeout exception."}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
