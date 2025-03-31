# test_imports.py
try:
    from ga1 import handlers as ga1_handlers
    print("GA1 imported successfully:", list(ga1_handlers.keys()))
except Exception as e:
    print("GA1 import failed:", str(e))

try:
    from ga2 import handlers as ga2_handlers
    print("GA2 imported successfully:", list(ga2_handlers.keys()))
except Exception as e:
    print("GA2 import failed:", str(e))

try:
    from ga3 import handlers as ga3_handlers
    print("GA3 imported successfully:", list(ga3_handlers.keys()))
except Exception as e:
    print("GA3 import failed:", str(e))

try:
    from ga4 import handlers as ga4_handlers
    print("GA4 imported successfully:", list(ga4_handlers.keys()))
except Exception as e:
    print("GA4 import failed:", str(e))

try:
    from ga5 import handlers as ga5_handlers
    print("GA5 imported successfully:", list(ga5_handlers.keys()))
except Exception as e:
    print("GA5 import failed:", str(e))