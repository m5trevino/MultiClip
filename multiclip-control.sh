#!/bin/bash

case "$1" in
    start)
        echo "Starting MultiClip service..."
        sudo systemctl start multiclip.service
        ;;
    stop)
        echo "Stopping MultiClip service..."
        sudo systemctl stop multiclip.service
        ;;
    restart)
        echo "Restarting MultiClip service..."
        sudo systemctl restart multiclip.service
        ;;
    status)
        echo "MultiClip service status:"
        sudo systemctl status multiclip.service
        ;;
    logs)
        echo "MultiClip service logs:"
        sudo journalctl -u multiclip.service -f
        ;;
    enable)
        echo "Enabling MultiClip service to start at boot..."
        sudo systemctl enable multiclip.service
        ;;
    disable)
        echo "Disabling MultiClip service from starting at boot..."
        sudo systemctl disable multiclip.service
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|enable|disable}"
        echo ""
        echo "Commands:"
        echo "  start   - Start the MultiClip service"
        echo "  stop    - Stop the MultiClip service"
        echo "  restart - Restart the MultiClip service"
        echo "  status  - Show service status"
        echo "  logs    - Show live service logs"
        echo "  enable  - Enable auto-start at boot"
        echo "  disable - Disable auto-start at boot"
        exit 1
        ;;
esac
