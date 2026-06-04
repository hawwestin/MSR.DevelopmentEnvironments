If ansible keep stuck on tasks and next execution cannot even start. We may need to clean old sessions
```bash
pkill -f ansible || true
pkill -f ssh || true
```