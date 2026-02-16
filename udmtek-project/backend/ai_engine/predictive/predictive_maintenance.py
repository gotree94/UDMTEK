"""
Predictive Maintenance AI Engine
Machine learning models for failure prediction and maintenance scheduling
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import numpy as np
import logging

logger = logging.getLogger(__name__)


class MaintenanceType(Enum):
    """Types of maintenance"""
    PREVENTIVE = "PREVENTIVE"
    CORRECTIVE = "CORRECTIVE"
    PREDICTIVE = "PREDICTIVE"
    CONDITION_BASED = "CONDITION_BASED"


class EquipmentHealth(Enum):
    """Equipment health status"""
    EXCELLENT = "EXCELLENT"    # 90-100%
    GOOD = "GOOD"              # 70-89%
    FAIR = "FAIR"              # 50-69%
    POOR = "POOR"              # 30-49%
    CRITICAL = "CRITICAL"      # 0-29%


@dataclass
class MaintenanceRecommendation:
    """Maintenance action recommendation"""
    equipment_id: str
    recommendation_id: str
    timestamp: datetime
    maintenance_type: MaintenanceType
    priority: int  # 1 (highest) to 5 (lowest)
    predicted_failure_date: Optional[datetime]
    remaining_useful_life: Optional[int]  # days
    confidence: float
    description: str
    recommended_actions: List[str]
    estimated_cost: Optional[float]
    estimated_downtime: Optional[int]  # minutes
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "equipment_id": self.equipment_id,
            "recommendation_id": self.recommendation_id,
            "timestamp": self.timestamp.isoformat(),
            "maintenance_type": self.maintenance_type.value,
            "priority": self.priority,
            "predicted_failure_date": self.predicted_failure_date.isoformat() if self.predicted_failure_date else None,
            "remaining_useful_life_days": self.remaining_useful_life,
            "confidence": self.confidence,
            "description": self.description,
            "recommended_actions": self.recommended_actions,
            "estimated_cost": self.estimated_cost,
            "estimated_downtime_minutes": self.estimated_downtime
        }


@dataclass
class EquipmentStatus:
    """Current equipment status"""
    equipment_id: str
    health_score: float  # 0-100
    health_status: EquipmentHealth
    operating_hours: float
    cycles_count: int
    last_maintenance: Optional[datetime]
    sensor_readings: Dict[str, float]
    anomaly_score: float
    degradation_rate: float  # per day


class PredictiveMaintenanceEngine:
    """
    AI-powered predictive maintenance engine
    Predicts equipment failures and recommends maintenance actions
    """
    
    def __init__(self):
        self.ml_models = {}
        self.equipment_database = {}
        self.failure_history = []
        self._initialize_models()
        logger.info("Predictive Maintenance Engine initialized")
    
    def _initialize_models(self):
        """Initialize ML models for different equipment types"""
        # TODO: Load trained models
        # For now, using rule-based approach
        
        self.degradation_models = {
            "motor": self._motor_degradation_model,
            "pump": self._pump_degradation_model,
            "valve": self._valve_degradation_model,
            "sensor": self._sensor_degradation_model,
            "bearing": self._bearing_degradation_model
        }
        
        logger.info(f"Loaded {len(self.degradation_models)} degradation models")
    
    def predict_maintenance(self, equipment_status: EquipmentStatus) -> List[MaintenanceRecommendation]:
        """
        Predict maintenance needs for equipment
        
        Args:
            equipment_status: Current status of equipment
            
        Returns:
            List of maintenance recommendations
        """
        logger.info(f"Analyzing equipment: {equipment_status.equipment_id}")
        
        recommendations = []
        
        # 1. Health-based recommendations
        if equipment_status.health_score < 50:
            rec = self._create_health_based_recommendation(equipment_status)
            recommendations.append(rec)
        
        # 2. Time-based recommendations
        time_rec = self._check_time_based_maintenance(equipment_status)
        if time_rec:
            recommendations.append(time_rec)
        
        # 3. Condition-based recommendations
        condition_recs = self._analyze_sensor_trends(equipment_status)
        recommendations.extend(condition_recs)
        
        # 4. Predict remaining useful life
        rul_rec = self._predict_remaining_useful_life(equipment_status)
        if rul_rec:
            recommendations.append(rul_rec)
        
        # 5. Anomaly-based recommendations
        if equipment_status.anomaly_score > 0.7:
            anomaly_rec = self._create_anomaly_recommendation(equipment_status)
            recommendations.append(anomaly_rec)
        
        # Sort by priority
        recommendations.sort(key=lambda x: x.priority)
        
        logger.info(f"Generated {len(recommendations)} maintenance recommendations")
        return recommendations
    
    def _create_health_based_recommendation(self, status: EquipmentStatus) -> MaintenanceRecommendation:
        """Create recommendation based on health score"""
        
        if status.health_score < 30:
            priority = 1
            maintenance_type = MaintenanceType.CORRECTIVE
            description = f"Critical health status ({status.health_score:.1f}%) - immediate attention required"
            actions = [
                "Perform emergency inspection",
                "Schedule immediate maintenance",
                "Prepare replacement parts"
            ]
        elif status.health_score < 50:
            priority = 2
            maintenance_type = MaintenanceType.PREDICTIVE
            description = f"Poor health status ({status.health_score:.1f}%) - maintenance recommended soon"
            actions = [
                "Schedule maintenance within 1 week",
                "Monitor closely",
                "Order replacement parts"
            ]
        else:
            priority = 3
            maintenance_type = MaintenanceType.CONDITION_BASED
            description = f"Fair health status ({status.health_score:.1f}%) - plan maintenance"
            actions = [
                "Schedule routine maintenance",
                "Continue monitoring"
            ]
        
        return MaintenanceRecommendation(
            equipment_id=status.equipment_id,
            recommendation_id=f"REC_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            maintenance_type=maintenance_type,
            priority=priority,
            predicted_failure_date=None,
            remaining_useful_life=None,
            confidence=0.85,
            description=description,
            recommended_actions=actions,
            estimated_cost=5000.0,
            estimated_downtime=120
        )
    
    def _check_time_based_maintenance(self, status: EquipmentStatus) -> Optional[MaintenanceRecommendation]:
        """Check if time-based maintenance is due"""
        
        if status.last_maintenance is None:
            return None
        
        days_since_maintenance = (datetime.now() - status.last_maintenance).days
        
        # Example: Maintenance every 180 days
        if days_since_maintenance > 180:
            return MaintenanceRecommendation(
                equipment_id=status.equipment_id,
                recommendation_id=f"REC_TIME_{datetime.now().timestamp()}",
                timestamp=datetime.now(),
                maintenance_type=MaintenanceType.PREVENTIVE,
                priority=3,
                predicted_failure_date=None,
                remaining_useful_life=None,
                confidence=1.0,
                description=f"Scheduled maintenance overdue by {days_since_maintenance - 180} days",
                recommended_actions=[
                    "Perform scheduled maintenance",
                    "Replace worn components",
                    "Lubrication service"
                ],
                estimated_cost=2000.0,
                estimated_downtime=60
            )
        
        return None
    
    def _analyze_sensor_trends(self, status: EquipmentStatus) -> List[MaintenanceRecommendation]:
        """Analyze sensor data trends for anomalies"""
        recommendations = []
        
        # Check vibration levels
        if "vibration" in status.sensor_readings:
            vibration = status.sensor_readings["vibration"]
            if vibration > 10.0:  # mm/s threshold
                rec = MaintenanceRecommendation(
                    equipment_id=status.equipment_id,
                    recommendation_id=f"REC_VIB_{datetime.now().timestamp()}",
                    timestamp=datetime.now(),
                    maintenance_type=MaintenanceType.CONDITION_BASED,
                    priority=2,
                    predicted_failure_date=datetime.now() + timedelta(days=14),
                    remaining_useful_life=14,
                    confidence=0.80,
                    description=f"Excessive vibration detected ({vibration:.2f} mm/s)",
                    recommended_actions=[
                        "Check bearing condition",
                        "Verify alignment",
                        "Balance rotating components",
                        "Inspect mounting"
                    ],
                    estimated_cost=3000.0,
                    estimated_downtime=180
                )
                recommendations.append(rec)
        
        # Check temperature
        if "temperature" in status.sensor_readings:
            temperature = status.sensor_readings["temperature"]
            if temperature > 80.0:  # °C threshold
                rec = MaintenanceRecommendation(
                    equipment_id=status.equipment_id,
                    recommendation_id=f"REC_TEMP_{datetime.now().timestamp()}",
                    timestamp=datetime.now(),
                    maintenance_type=MaintenanceType.CONDITION_BASED,
                    priority=2,
                    predicted_failure_date=datetime.now() + timedelta(days=7),
                    remaining_useful_life=7,
                    confidence=0.75,
                    description=f"Elevated temperature ({temperature:.1f}°C)",
                    recommended_actions=[
                        "Check cooling system",
                        "Verify lubrication",
                        "Clean heat exchanger",
                        "Check for overload"
                    ],
                    estimated_cost=1500.0,
                    estimated_downtime=90
                )
                recommendations.append(rec)
        
        # Check current draw (for motors)
        if "current" in status.sensor_readings:
            current = status.sensor_readings["current"]
            # Assuming rated current is known
            rated_current = 10.0  # A
            if current > rated_current * 1.2:
                rec = MaintenanceRecommendation(
                    equipment_id=status.equipment_id,
                    recommendation_id=f"REC_CURR_{datetime.now().timestamp()}",
                    timestamp=datetime.now(),
                    maintenance_type=MaintenanceType.CONDITION_BASED,
                    priority=1,
                    predicted_failure_date=datetime.now() + timedelta(days=3),
                    remaining_useful_life=3,
                    confidence=0.85,
                    description=f"Overcurrent condition ({current:.2f}A, rated {rated_current}A)",
                    recommended_actions=[
                        "Check for mechanical binding",
                        "Verify load conditions",
                        "Inspect motor windings",
                        "Check for phase imbalance"
                    ],
                    estimated_cost=4000.0,
                    estimated_downtime=240
                )
                recommendations.append(rec)
        
        return recommendations
    
    def _predict_remaining_useful_life(self, status: EquipmentStatus) -> Optional[MaintenanceRecommendation]:
        """Predict remaining useful life using degradation models"""
        
        # Determine equipment type from ID
        equipment_type = status.equipment_id.split("_")[0].lower()
        
        if equipment_type not in self.degradation_models:
            return None
        
        # Get degradation model
        model_func = self.degradation_models[equipment_type]
        
        # Predict RUL
        rul_days = model_func(status)
        
        if rul_days < 30:
            priority = 1
        elif rul_days < 60:
            priority = 2
        else:
            priority = 3
        
        failure_date = datetime.now() + timedelta(days=rul_days)
        
        return MaintenanceRecommendation(
            equipment_id=status.equipment_id,
            recommendation_id=f"REC_RUL_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            maintenance_type=MaintenanceType.PREDICTIVE,
            priority=priority,
            predicted_failure_date=failure_date,
            remaining_useful_life=rul_days,
            confidence=0.70,
            description=f"Predicted remaining useful life: {rul_days} days",
            recommended_actions=[
                f"Plan maintenance before {failure_date.strftime('%Y-%m-%d')}",
                "Order replacement parts",
                "Schedule maintenance window"
            ],
            estimated_cost=3500.0,
            estimated_downtime=150
        )
    
    def _create_anomaly_recommendation(self, status: EquipmentStatus) -> MaintenanceRecommendation:
        """Create recommendation based on anomaly detection"""
        
        return MaintenanceRecommendation(
            equipment_id=status.equipment_id,
            recommendation_id=f"REC_ANOM_{datetime.now().timestamp()}",
            timestamp=datetime.now(),
            maintenance_type=MaintenanceType.CONDITION_BASED,
            priority=2,
            predicted_failure_date=None,
            remaining_useful_life=None,
            confidence=status.anomaly_score,
            description=f"Abnormal behavior detected (anomaly score: {status.anomaly_score:.2f})",
            recommended_actions=[
                "Investigate unusual patterns",
                "Perform detailed inspection",
                "Review recent operational changes",
                "Monitor closely"
            ],
            estimated_cost=1000.0,
            estimated_downtime=30
        )
    
    # Degradation models for different equipment types
    
    def _motor_degradation_model(self, status: EquipmentStatus) -> int:
        """Predict motor remaining useful life"""
        
        # Factors affecting motor life
        base_life = 36500  # days (100 years new motor)
        
        # Reduce based on operating hours
        life_reduction = status.operating_hours / 100  # days
        
        # Reduce based on health score
        health_factor = status.health_score / 100
        
        # Reduce based on temperature
        temp = status.sensor_readings.get("temperature", 40)
        temp_factor = max(0, 1 - (temp - 40) / 100)  # Reduce life at high temp
        
        rul = int(base_life * health_factor * temp_factor - life_reduction)
        
        return max(1, rul)
    
    def _pump_degradation_model(self, status: EquipmentStatus) -> int:
        """Predict pump remaining useful life"""
        base_life = 18250  # days (50 years)
        
        health_factor = status.health_score / 100
        cycles_factor = max(0, 1 - status.cycles_count / 1000000)
        
        rul = int(base_life * health_factor * cycles_factor)
        
        return max(1, rul)
    
    def _valve_degradation_model(self, status: EquipmentStatus) -> int:
        """Predict valve remaining useful life"""
        base_life = 7300  # days (20 years)
        
        health_factor = status.health_score / 100
        cycles_factor = max(0, 1 - status.cycles_count / 100000)
        
        rul = int(base_life * health_factor * cycles_factor)
        
        return max(1, rul)
    
    def _sensor_degradation_model(self, status: EquipmentStatus) -> int:
        """Predict sensor remaining useful life"""
        base_life = 3650  # days (10 years)
        
        health_factor = status.health_score / 100
        
        rul = int(base_life * health_factor)
        
        return max(1, rul)
    
    def _bearing_degradation_model(self, status: EquipmentStatus) -> int:
        """Predict bearing remaining useful life"""
        base_life = 1825  # days (5 years)
        
        health_factor = status.health_score / 100
        
        # Vibration impact
        vibration = status.sensor_readings.get("vibration", 0)
        vib_factor = max(0, 1 - vibration / 50)
        
        rul = int(base_life * health_factor * vib_factor)
        
        return max(1, rul)
    
    def calculate_health_score(self, status: EquipmentStatus) -> float:
        """Calculate overall health score"""
        
        scores = []
        
        # Operating hours score (newer is better)
        if status.operating_hours < 1000:
            scores.append(100)
        elif status.operating_hours < 5000:
            scores.append(90)
        elif status.operating_hours < 10000:
            scores.append(70)
        else:
            scores.append(50)
        
        # Sensor-based scores
        if "vibration" in status.sensor_readings:
            vib = status.sensor_readings["vibration"]
            vib_score = max(0, 100 - vib * 5)
            scores.append(vib_score)
        
        if "temperature" in status.sensor_readings:
            temp = status.sensor_readings["temperature"]
            temp_score = max(0, 100 - (temp - 40) * 2)
            scores.append(temp_score)
        
        # Anomaly score impact
        anomaly_impact = (1 - status.anomaly_score) * 100
        scores.append(anomaly_impact)
        
        # Average all scores
        overall_score = np.mean(scores) if scores else 50.0
        
        return overall_score
    
    def optimize_maintenance_schedule(
        self, 
        recommendations: List[MaintenanceRecommendation],
        constraints: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """
        Optimize maintenance schedule considering constraints
        
        Args:
            recommendations: List of maintenance recommendations
            constraints: Budget, downtime limits, resource availability
            
        Returns:
            Optimized maintenance schedule
        """
        logger.info(f"Optimizing schedule for {len(recommendations)} recommendations")
        
        budget = constraints.get("budget", float('inf'))
        max_downtime = constraints.get("max_downtime_per_month", float('inf'))
        
        # Sort by priority and RUL
        sorted_recs = sorted(
            recommendations,
            key=lambda x: (x.priority, x.remaining_useful_life or 999)
        )
        
        schedule = []
        total_cost = 0
        total_downtime = 0
        current_date = datetime.now()
        
        for rec in sorted_recs:
            # Check budget constraint
            if total_cost + (rec.estimated_cost or 0) > budget:
                continue
            
            # Check downtime constraint
            if total_downtime + (rec.estimated_downtime or 0) > max_downtime:
                continue
            
            # Schedule the maintenance
            scheduled_date = current_date + timedelta(days=7)
            if rec.predicted_failure_date:
                # Schedule before predicted failure
                scheduled_date = rec.predicted_failure_date - timedelta(days=7)
            
            schedule.append({
                "equipment_id": rec.equipment_id,
                "scheduled_date": scheduled_date.isoformat(),
                "maintenance_type": rec.maintenance_type.value,
                "description": rec.description,
                "actions": rec.recommended_actions,
                "estimated_cost": rec.estimated_cost,
                "estimated_downtime": rec.estimated_downtime
            })
            
            total_cost += rec.estimated_cost or 0
            total_downtime += rec.estimated_downtime or 0
        
        logger.info(f"Optimized schedule: {len(schedule)} items, cost: ${total_cost}, downtime: {total_downtime}min")
        
        return schedule


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    engine = PredictiveMaintenanceEngine()
    
    # Create sample equipment status
    equipment = EquipmentStatus(
        equipment_id="MOTOR_001",
        health_score=65.0,
        health_status=EquipmentHealth.FAIR,
        operating_hours=8500.0,
        cycles_count=125000,
        last_maintenance=datetime.now() - timedelta(days=200),
        sensor_readings={
            "vibration": 8.5,
            "temperature": 72.0,
            "current": 11.5
        },
        anomaly_score=0.35,
        degradation_rate=0.05
    )
    
    # Predict maintenance
    recommendations = engine.predict_maintenance(equipment)
    
    print(f"\n=== Predictive Maintenance Analysis ===")
    print(f"Equipment: {equipment.equipment_id}")
    print(f"Health Score: {equipment.health_score:.1f}%")
    print(f"Operating Hours: {equipment.operating_hours:.0f}h")
    print(f"\nMaintenance Recommendations: {len(recommendations)}\n")
    
    for rec in recommendations:
        print(f"Priority {rec.priority}: {rec.description}")
        print(f"  Type: {rec.maintenance_type.value}")
        if rec.remaining_useful_life:
            print(f"  RUL: {rec.remaining_useful_life} days")
        print(f"  Confidence: {rec.confidence * 100:.0f}%")
        print(f"  Action: {rec.recommended_actions[0]}")
        print()
