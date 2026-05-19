import os
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify

app = Flask(__name__)

# Use Supabase pooler port 6543 to avoid connection limit exhaustion
DATABASE_URL = os.environ.get(
    'DATABASE_URL',
    'postgresql://postgres:Kobibi09%40%24%24@db.nxgduobaryxomauktmcu.supabase.co:6543/postgres'
)

def get_db_connection():
    conn = psycopg2.connect(DATABASE_URL)
    return conn


# ============================================================
# DISCOVERY: llms.txt for AI Agent Discovery (no auth required)
# ============================================================
@app.route('/llms.txt', methods=['GET'])
def get_llms_txt():
    content = """# AI Data Gateway
> A premium, pay-per-request API providing real-time and compliance-focused data on logistics, real estate, healthcare, and finance sectors.

## API Reference
- [Developer Portal & Pricing](https://aiapi-main-b378d28.zuplo.site): Sign up for an API key and view full documentation.
- [Logistics Data Example](https://aiapi-main-b378d28.zuplo.app/mcp/logistics-niche-1): Example for logistics telemetry.
- [Healthcare Data Example](https://aiapi-main-b378d28.zuplo.app/mcp/healthcare-niche-1): Example for healthcare compliance data.

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
4. Make requests to any /mcp/{niche_id} endpoint

## Example Request
curl -H "Authorization: Bearer YOUR_API_KEY" "https://aiapi-main-b378d28.zuplo.app/mcp/logistics-niche-1"
"""
    return content, 200, {'Content-Type': 'text/plain'}


# ============================================================
# MAIN API ROUTE: Dynamic Niche Data Lookup
# ============================================================
@app.route('/mcp/<niche_id>', methods=['GET'])
def get_vault_data(niche_id):
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor(cursor_factory=RealDictCursor)

        cur.execute(
            "SELECT niche, telemetry_data, mcp_context FROM niches WHERE id = %s;",
            (niche_id,)
        )
        tool_data = cur.fetchone()
        cur.close()

        if tool_data:
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


# ============================================================
# HEALTH CHECK: for uptime monitoring (no auth required)
# ============================================================
@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
