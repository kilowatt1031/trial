#!/bin/bash

# Streamlit管理スクリプト (Git Bash for Windows版)
APP_FILE="streamlit_app.py"
PID_FILE="streamlit.pid"
LOG_FILE="streamlit.log"

# プロセスが実行中か確認する関数 (Git Bash用)
is_process_running() {
    if [ -z "$1" ]; then
        return 1 # PIDがなければ偽
    fi
    # ps -p はGit Bashでも利用可能
    ps -p "$1" > /dev/null 2>&1
}

case "$1" in
    start)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if is_process_running "$PID"; then
                echo "Streamlit is already running (PID: $PID)"
                exit 1
            else
                # PIDファイルが残っているがプロセスは存在しない場合
                echo "Stale PID file found. Removing it."
                rm "$PID_FILE"
            fi
        fi
        
        echo "Starting Streamlit..."
        # バックグラウンドでStreamlitを起動 (nohupはGit Bash標準ではないため削除)
        # Git Bashウィンドウを閉じるとプロセスが終了する可能性があります
        uv run streamlit run "$APP_FILE" > "$LOG_FILE" 2>&1 &
        PID=$!
        echo $PID > "$PID_FILE"
        echo "Streamlit started with PID: $PID"
        echo "Access at: http://localhost:8501"
        echo "Log file: $LOG_FILE"
        echo ""
        echo "Next actions:"
        echo "   ./$(basename "$0") stop      - Stop Streamlit"
        echo "   ./$(basename "$0") restart   - Restart Streamlit"
        echo "   ./$(basename "$0") show-logs - Show recent logs"
        echo "   ./$(basename "$0") logs      - View live logs"
        echo "   ./$(basename "$0") status    - Check status"
        echo "   ./$(basename "$0") kill-all  - Force kill all Streamlit processes"
        ;;
    
    stop)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if is_process_running "$PID"; then
                echo "Stopping Streamlit (PID: $PID)..."
                # killはGit Bashではtaskkillを呼び出す
                kill "$PID"
                rm "$PID_FILE"
                echo "Streamlit stopped."
                echo ""
                echo "Next actions:"
                echo "   ./$(basename "$0") start     - Start Streamlit again"
                echo "   ./$(basename "$0") restart   - Quick restart"
            else
                echo "Streamlit process not found, but PID file exists. Cleaning up."
                rm "$PID_FILE"
            fi
        else
            echo "Streamlit is not running (PID file not found)."
        fi
        ;;
    
    restart)
        "$0" stop
        sleep 2
        "$0" start
        ;;
    
    status)
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if is_process_running "$PID"; then
                echo "Streamlit is running (PID: $PID)"
                echo "Access at: http://localhost:8501"
                echo ""
                echo "Available actions:"
                echo "   ./$(basename "$0") stop      - Stop Streamlit"
                echo "   ./$(basename "$0") restart   - Restart Streamlit"
                echo "   ./$(basename "$0") show-logs - Show recent logs"
            else
                echo "Streamlit is not running (stale PID file)."
                rm "$PID_FILE"
                echo ""
                echo "Available actions:"
                echo "   ./$(basename "$0") start     - Start Streamlit"
            fi
        else
            echo "Streamlit is not running."
            echo ""
            echo "Available actions:"
            echo "   ./$(basename "$0") start     - Start Streamlit"
        fi
        ;;
    
    logs)
        if [ -f "$LOG_FILE" ]; then
            echo "Showing live logs from '$LOG_FILE' (Press Ctrl+C to exit)..."
            echo "----------------------------------------"
            tail -f "$LOG_FILE"
        else
            echo "Log file '$LOG_FILE' not found."
        fi
        ;;
    
    show-logs)
        if [ -f "$LOG_FILE" ]; then
            echo "Recent Streamlit logs (last 20 lines from '$LOG_FILE'):"
            echo "----------------------------------------"
            tail -20 "$LOG_FILE"
            echo "----------------------------------------"
            echo ""
            echo "To view live logs, use: ./$(basename "$0") logs"
        else
            echo "Log file '$LOG_FILE' not found."
        fi
        ;;
    
    kill-all)
        echo "Attempting to kill all 'streamlit run' processes..."
        # pkillの代替: ps -WでWindowsプロセスを取得し、grepとawkでPIDを特定
        PIDS_TO_KILL=$(ps -W | grep "streamlit run" | grep -v "grep" | awk '{print $1}')
        
        if [ -z "$PIDS_TO_KILL" ]; then
            echo "No running 'streamlit run' processes found."
        else
            for PID in $PIDS_TO_KILL; do
                echo "Killing process $PID..."
                kill "$PID"
            done
            echo "All matching processes terminated."
        fi
        
        # PIDファイルも削除
        if [ -f "$PID_FILE" ]; then
            rm -f "$PID_FILE"
            echo "PID file removed."
        fi
        ;;
    
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|show-logs|kill-all}"
        echo ""
        echo "Commands:"
        echo "  start      - Start Streamlit in background"
        echo "  stop       - Stop Streamlit gracefully"
        echo "  restart    - Restart Streamlit"
        echo "  status     - Check Streamlit status"
        echo "  logs       - Show live logs (Ctrl+C to exit)"
        echo "  show-logs  - Show recent logs only"
        echo "  kill-all   - Force kill all Streamlit processes"
        exit 1
        ;;
esac