#!/bin/bash

# MultiClip Service Control Script
SERVICE_NAME="multiclip.service"

case "$1" in
    start)
        echo "Starting MultiClip service..."
        sudo systemctl start $SERVICE_NAME
        ;;
    stop)
        echo "Stopping MultiClip service..."
        sudo systemctl stop $SERVICE_NAME
        ;;
    restart)
        echo "Restarting MultiClip service..."
        sudo systemctl restart $SERVICE_NAME
        ;;
    status)
        echo "MultiClip service status:"
        sudo systemctl status $SERVICE_NAME --no-pager
        ;;
    logs)
        echo "MultiClip service logs:"
        sudo journalctl -u $SERVICE_NAME --no-pager -n 50
        ;;
    enable)
        echo "Enabling MultiClip service at startup..."
        sudo systemctl enable $SERVICE_NAME
        ;;
    disable)
        echo "Disabling MultiClip service at startup..."
        sudo systemctl disable $SERVICE_NAME
        ;;
    test)
        echo "Testing MultiClip manually (Ctrl+C to stop)..."
        cd /home/flintx/multiclip
        poetry run python multiclip.py
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|enable|disable|test}"
        echo ""
        echo "Commands:"
        echo "  start    - Start the MultiClip service"
        echo "  stop     - Stop the MultiClip service"
        echo "  restart  - Restart the MultiClip service"
        echo "  status   - Show service status"
        echo "  logs     - Show recent service logs"
        echo "  enable   - Enable service at startup"
        echo "  disable  - Disable service at startup"
        echo "  test     - Run MultiClip manually for testing"
        exit 1
        ;;
esac
