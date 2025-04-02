#!/bin/bash
set -e

# 記錄上次向量庫更新的檔案（如果需要持久化，可考慮掛載資料卷）
LAST_UPDATE_FILE="/app/last_update_vector.txt"
CURRENT_DATE=$(date +"%Y-%m-%d")

# 讀取上次更新日期
if [ -f "$LAST_UPDATE_FILE" ]; then
    LAST_UPDATE_DATE=$(cat "$LAST_UPDATE_FILE")
else
    LAST_UPDATE_DATE="1970-01-01"
fi

# 檢查今天是否已執行過更新，若否則立即執行更新任務
if [ "$LAST_UPDATE_DATE" != "$CURRENT_DATE" ]; then
    echo "檢測到今日未執行向量庫更新，立即執行 update_vector_store.py..."
    python -m src.update_vector_store
    echo "$CURRENT_DATE" > "$LAST_UPDATE_FILE"
else
    echo "今日的向量庫更新任務已執行。"
fi

# 最後啟動 cron，保持容器內定時任務（如果容器持續運行的話）
echo "啟動 cron 服務..."
cron -f
