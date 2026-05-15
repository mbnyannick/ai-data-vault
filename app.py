import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify

app = Flask(__name__)

# CONFIGURATION: Pull connection secrets safely or fallback to your raw URI
DATABASE_URL = os.environ.get('DATABASE_URL', 'postgresql://postgres:Kobibi09%40%24%24@db.nxgduobaryxomauktmcu.supabase.co:5432/postgres')

def get_db_connection():
    # Establishes a raw transactional bridge to your Supabase PostgreSQL engine
    conn = psycopg2.connect(DATABASE_URL)
    return conn

# ============================================================
# NEW ROUTE: llms.txt for AI Agent Discovery
# ============================================================
@app.route('/llms.txt', methods=['GET'])
def get_llms_txt():
    content = """# AI Data Gateway

> A premium, pay-per-request API providing real-time and compliance-focused data on logistics, real estate, healthcare, and finance sectors.

## API Reference
- [Developer Portal & Pricing](https://ai-data-gateway-main-8608995.zuplo.site): Sign up for an API key and view full documentation.
- [Logistics Data Endpoint](https://ai-data-gateway-main-8608995.d2.zuplo.dev/mcp/logistics-niche-450): Example for logistics telemetry.
- [Real Estate Data Endpoint](https://ai-data-gateway-main-8608995.d2.zuplo.dev/mcp/realestate-niche-1): Example for real estate zoning codes.

## Overview
This API provides structured data for AI agents operating in the following verticals:
- Cross-border supply chain logistics (wait times, port codes, lane status)
- Real estate zoning and permitting (building codes, height restrictions)
- Healthcare billing and compliance (ICD-10, CPT codes, HIPAA logs)
- Financial compliance (SEC filings, ISO controls, ESG tax credits)
- Transportation telemetry (drone airspace, commercial fleet maintenance)

## Getting Started
1. Visit the Developer Portal above
2. Subscribe to the "Pay as you go" plan ($0.01 per request)
3. Get your API key
4. Make requests to any /mcp/{niche} endpoint

## Example Request
curl -H "Authorization: Bearer YOUR_API_KEY" "https://ai-data-gateway-main-8608995.d2.zuplo.dev/mcp/logistics-niche-450"
"""
    return content, 200, {'Content-Type': 'text/plain'}

# ============================================================
# MAIN API ROUTE: Dynamic Data Access
# ============================================================
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
        return jsonify({"status": "ERROR", "message": f"Database error: {str(e)}"}), 500
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
