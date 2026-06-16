---
name: ssl-fix
description: Mandatory SSL patch required before any FinanceDataReader call in this macOS environment
metadata:
  type: feedback
---

This environment's Python cannot locate system certificates for SSL verification. Any `fdr.DataReader()` call will fail with an SSL error unless the following patch is applied FIRST:

```python
import ssl, certifi, functools
ssl._create_default_https_context = functools.partial(ssl.create_default_context, cafile=certifi.where())
```

**Why:** macOS system Python SSL certificate store is not accessible; certifi provides the fallback CA bundle.

**How to apply:** Always place these 3 lines before `import FinanceDataReader as fdr` in every Python script run via Bash in this project. Without them, all FDR HTTP requests fail silently or raise SSLError.
