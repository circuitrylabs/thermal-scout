#!/usr/bin/env python
"""
Run the Thermal Scout API server

Created with ❤️ by Claude and Tyler
"""

import uvicorn

if __name__ == "__main__":
    print("🔥 Starting Thermal Scout API...")
    print("📍 API will be available at: http://localhost:8080")
    print("📚 Interactive docs at: http://localhost:8080/docs")
    print("🔍 ReDoc at: http://localhost:8080/redoc")

    uvicorn.run(
        "thermal_scout.api.main:app",
        host="0.0.0.0",
        port=8080,
        reload=True,
        log_level="info"
    )
