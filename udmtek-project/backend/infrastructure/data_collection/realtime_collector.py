"""
Real-time Data Collection Module
Collects data from PLCs and sensors in real-time
"""

import asyncio
import logging
from typing import Dict, Any, Callable
from datetime import datetime

logger = logging.getLogger(__name__)


class RealtimeCollector:
    """
    Real-time data collector for PLC and sensor data
    """
    
    def __init__(self):
        self.is_running = False
        self.data_handlers = []
        self.collection_interval = 1.0  # seconds
        logger.info("Real-time Collector initialized")
    
    def register_handler(self, handler: Callable):
        """Register a data handler callback"""
        self.data_handlers.append(handler)
        logger.info(f"Registered data handler: {handler.__name__}")
    
    async def start(self):
        """Start real-time data collection"""
        self.is_running = True
        logger.info("🚀 Starting real-time data collection...")
        
        try:
            while self.is_running:
                # Collect data
                data = await self._collect_data()
                
                # Notify all handlers
                for handler in self.data_handlers:
                    try:
                        await handler(data)
                    except Exception as e:
                        logger.error(f"Error in handler {handler.__name__}: {str(e)}")
                
                # Wait before next collection
                await asyncio.sleep(self.collection_interval)
                
        except Exception as e:
            logger.error(f"Error in data collection: {str(e)}")
        finally:
            logger.info("Real-time data collection stopped")
    
    async def stop(self):
        """Stop real-time data collection"""
        self.is_running = False
        logger.info("Stopping real-time data collection...")
    
    async def _collect_data(self) -> Dict[str, Any]:
        """
        Collect data from all connected sources
        
        Returns:
            Dictionary containing collected data
        """
        # TODO: Implement actual data collection from PLCs
        # This is a placeholder that simulates data
        
        import random
        
        data = {
            "timestamp": datetime.now().isoformat(),
            "plc_data": {
                "PLC_001": {
                    "status": "running",
                    "cpu_load": random.uniform(30, 80),
                    "scan_time": random.uniform(5, 15),
                    "signals": {
                        "temperature_1": random.uniform(60, 80),
                        "pressure_1": random.uniform(95, 105),
                        "motor_speed": random.uniform(1400, 1600),
                    }
                },
                "PLC_002": {
                    "status": "running",
                    "cpu_load": random.uniform(40, 90),
                    "scan_time": random.uniform(4, 12),
                    "signals": {
                        "temperature_2": random.uniform(55, 75),
                        "flow_rate": random.uniform(140, 160),
                    }
                }
            },
            "alarms": []
        }
        
        # Simulate occasional alarm
        if random.random() < 0.1:
            data["alarms"].append({
                "severity": "WARNING",
                "message": "Temperature approaching upper limit",
                "source": "PLC_001",
                "timestamp": datetime.now().isoformat()
            })
        
        return data


# Global instance
collector = RealtimeCollector()


# Example usage
if __name__ == "__main__":
    async def print_handler(data: Dict[str, Any]):
        """Example data handler"""
        print(f"Received data at {data['timestamp']}")
        print(f"PLC count: {len(data['plc_data'])}")
    
    collector.register_handler(print_handler)
    
    try:
        await collector.start()
    except KeyboardInterrupt:
        await collector.stop()
