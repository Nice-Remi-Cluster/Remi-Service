Set-Location ..

Remove-Item -Path ".\data\db.sqlite3" -Recurse -Force
Remove-Item -Path ".\data\db.sqlite3-shm" -Recurse -Force
Remove-Item -Path ".\data\db.sqlite3-wal" -Recurse -Force

uv run aerich upgrade
