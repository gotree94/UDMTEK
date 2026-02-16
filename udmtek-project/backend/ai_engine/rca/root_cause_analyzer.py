"""
Root Cause Analysis (RCA) AI Engine
Uses machine learning to identify and diagnose PLC faults automatically
"""

from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger(__name__)


class FaultSeverity(Enum):
    """Fault severity levels"""
    CRITICAL = "CRITICAL"
    HIGH = "HIGH"
    MEDIUM = "MEDIUM"
    LOW = "LOW"
    INFO = "INFO"


class FaultCategory(Enum):
    """Fault categories"""
    HARDWARE = "HARDWARE"
    SOFTWARE = "SOFTWARE"
    COMMUNICATION = "COMMUNICATION"
    CONFIGURATION = "CONFIGURATION"
    TIMING = "TIMING"
    SAFETY = "SAFETY"
    PROCESS = "PROCESS"


@dataclass
class Fault:
    """Represents a detected fault"""
    fault_id: str
    timestamp: datetime
    category: FaultCategory
    severity: FaultSeverity
    description: str
    affected_components: List[str]
    symptoms: List[str]
    root_cause: str
    recommended_actions: List[str]
    confidence: float  # 0.0 to 1.0
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "fault_id": self.fault_id,
            "timestamp": self.timestamp.isoformat(),
            "category": self.category.value,
            "severity": self.severity.value,
            "description": self.description,
            "affected_components": self.affected_components,
            "symptoms": self.symptoms,
            "root_cause": self.root_cause,
            "recommended_actions": self.recommended_actions,
            "confidence": self.confidence
        }


@dataclass
class DiagnosticData:
    """Input data for RCA analysis"""
    plc_signals: Dict[str, Any]      # Current PLC signal values
    historical_data: List[Dict]       # Historical signal data
    error_codes: List[str]            # PLC error codes
    alarm_history: List[Dict]         # Alarm log
    process_parameters: Dict[str, Any] # Process setpoints, etc.
    
    
class RootCauseAnalyzer:
    """
    AI-powered Root Cause Analysis engine
    Analyzes PLC data to identify fault root causes automatically
    """
    
    def __init__(self):
        self.fault_database = self._initialize_fault_database()
        self.ml_model = None  # TODO: Load trained ML model
        logger.info("Root Cause Analyzer initialized")
    
    def _initialize_fault_database(self) -> Dict[str, Dict]:
        """Initialize knowledge base of known faults"""
        return {
            "SENSOR_FAILURE": {
                "category": FaultCategory.HARDWARE,
                "severity": FaultSeverity.HIGH,
                "symptoms": [
                    "Sensor value stuck at constant",
                    "Out-of-range readings",
                    "Signal noise increased"
                ],
                "root_causes": [
                    "Sensor mechanical failure",
                    "Wiring disconnection",
                    "Power supply issue",
                    "EMI interference"
                ],
                "diagnostic_pattern": {
                    "value_variance": lambda x: x < 0.01,
                    "out_of_range": lambda x: x < 0 or x > 100
                }
            },
            "COMMUNICATION_TIMEOUT": {
                "category": FaultCategory.COMMUNICATION,
                "severity": FaultSeverity.CRITICAL,
                "symptoms": [
                    "Fieldbus timeout errors",
                    "Data update stopped",
                    "Communication LED off"
                ],
                "root_causes": [
                    "Network cable disconnected",
                    "Device address conflict",
                    "Network overload",
                    "Device firmware issue"
                ],
                "diagnostic_pattern": {
                    "timeout_count": lambda x: x > 5,
                    "response_time": lambda x: x > 1000  # ms
                }
            },
            "LOGIC_ERROR": {
                "category": FaultCategory.SOFTWARE,
                "severity": FaultSeverity.MEDIUM,
                "symptoms": [
                    "Unexpected output state",
                    "Sequence out of order",
                    "Timer/counter malfunction"
                ],
                "root_causes": [
                    "Programming error",
                    "Race condition",
                    "Incorrect parameter",
                    "Logic conflict"
                ],
                "diagnostic_pattern": {
                    "state_mismatch": lambda x: True
                }
            },
            "MOTOR_OVERLOAD": {
                "category": FaultCategory.PROCESS,
                "severity": FaultSeverity.HIGH,
                "symptoms": [
                    "Current exceeds rated value",
                    "Temperature increase",
                    "Vibration abnormal"
                ],
                "root_causes": [
                    "Mechanical jam",
                    "Worn bearings",
                    "Overload condition",
                    "Phase loss"
                ],
                "diagnostic_pattern": {
                    "current_ratio": lambda x: x > 1.2,
                    "temperature": lambda x: x > 80
                }
            },
            "TIMING_VIOLATION": {
                "category": FaultCategory.TIMING,
                "severity": FaultSeverity.MEDIUM,
                "symptoms": [
                    "Scan time exceeded",
                    "Task overrun",
                    "Watchdog timeout"
                ],
                "root_causes": [
                    "CPU overload",
                    "Infinite loop",
                    "Blocking operation",
                    "Insufficient cycle time"
                ],
                "diagnostic_pattern": {
                    "scan_time": lambda x: x > 100,  # ms
                    "cpu_load": lambda x: x > 90  # %
                }
            },
            "SAFETY_VIOLATION": {
                "category": FaultCategory.SAFETY,
                "severity": FaultSeverity.CRITICAL,
                "symptoms": [
                    "Safety relay tripped",
                    "E-stop activated",
                    "Guard door open",
                    "Light curtain broken"
                ],
                "root_causes": [
                    "Safety device triggered",
                    "Safety logic error",
                    "Unauthorized access",
                    "Equipment malfunction"
                ],
                "diagnostic_pattern": {
                    "safety_status": lambda x: x == False
                }
            }
        }
    
    def analyze(self, data: DiagnosticData) -> List[Fault]:
        """
        Perform root cause analysis on diagnostic data
        
        Args:
            data: DiagnosticData containing PLC signals and history
            
        Returns:
            List of identified faults with root causes
        """
        logger.info("Starting root cause analysis")
        
        faults = []
        
        # 1. Pattern-based detection
        pattern_faults = self._pattern_based_detection(data)
        faults.extend(pattern_faults)
        
        # 2. Statistical anomaly detection
        anomaly_faults = self._anomaly_detection(data)
        faults.extend(anomaly_faults)
        
        # 3. Sequence analysis
        sequence_faults = self._sequence_analysis(data)
        faults.extend(sequence_faults)
        
        # 4. ML-based prediction (if model available)
        if self.ml_model:
            ml_faults = self._ml_prediction(data)
            faults.extend(ml_faults)
        
        # 5. Correlation analysis
        correlated_faults = self._correlation_analysis(faults, data)
        
        logger.info(f"Analysis complete: {len(correlated_faults)} faults detected")
        
        return correlated_faults
    
    def _pattern_based_detection(self, data: DiagnosticData) -> List[Fault]:
        """Detect faults using predefined patterns"""
        faults = []
        
        # Check for sensor failures
        for signal_name, signal_value in data.plc_signals.items():
            if "sensor" in signal_name.lower():
                # Check if value is stuck
                if self._is_value_stuck(signal_name, signal_value, data.historical_data):
                    fault = Fault(
                        fault_id=f"FAULT_{datetime.now().timestamp()}",
                        timestamp=datetime.now(),
                        category=FaultCategory.HARDWARE,
                        severity=FaultSeverity.HIGH,
                        description=f"Sensor {signal_name} failure detected",
                        affected_components=[signal_name],
                        symptoms=["Value stuck at constant", "No variation in readings"],
                        root_cause="Possible sensor mechanical failure or wiring issue",
                        recommended_actions=[
                            "Check sensor wiring connections",
                            "Verify sensor power supply",
                            "Replace sensor if faulty",
                            "Check for EMI interference"
                        ],
                        confidence=0.85
                    )
                    faults.append(fault)
        
        # Check error codes
        for error_code in data.error_codes:
            fault = self._interpret_error_code(error_code)
            if fault:
                faults.append(fault)
        
        return faults
    
    def _anomaly_detection(self, data: DiagnosticData) -> List[Fault]:
        """Detect anomalies using statistical methods"""
        faults = []
        
        # Example: Detect abnormal process parameters
        for param_name, param_value in data.process_parameters.items():
            # Calculate statistical deviation
            historical_values = [
                record.get(param_name, 0) 
                for record in data.historical_data
            ]
            
            if len(historical_values) > 10:
                mean = np.mean(historical_values)
                std = np.std(historical_values)
                
                # 3-sigma rule
                if abs(param_value - mean) > 3 * std:
                    fault = Fault(
                        fault_id=f"FAULT_{datetime.now().timestamp()}",
                        timestamp=datetime.now(),
                        category=FaultCategory.PROCESS,
                        severity=FaultSeverity.MEDIUM,
                        description=f"Abnormal value detected for {param_name}",
                        affected_components=[param_name],
                        symptoms=[f"Value {param_value} deviates from normal range"],
                        root_cause="Process parameter out of statistical control",
                        recommended_actions=[
                            "Investigate process conditions",
                            "Check control loop tuning",
                            "Verify setpoint accuracy"
                        ],
                        confidence=0.75
                    )
                    faults.append(fault)
        
        return faults
    
    def _sequence_analysis(self, data: DiagnosticData) -> List[Fault]:
        """Analyze sequence of events for logic errors"""
        faults = []
        
        # Example: Check alarm sequence
        if len(data.alarm_history) > 1:
            # Look for repeating alarm patterns
            alarm_codes = [alarm['code'] for alarm in data.alarm_history[-10:]]
            
            if len(set(alarm_codes)) == 1 and len(alarm_codes) > 3:
                fault = Fault(
                    fault_id=f"FAULT_{datetime.now().timestamp()}",
                    timestamp=datetime.now(),
                    category=FaultCategory.SOFTWARE,
                    severity=FaultSeverity.MEDIUM,
                    description="Repeating alarm pattern detected",
                    affected_components=["PLC_Logic"],
                    symptoms=[f"Alarm {alarm_codes[0]} repeating {len(alarm_codes)} times"],
                    root_cause="Possible logic error or unresolved condition",
                    recommended_actions=[
                        "Review PLC logic for alarm condition",
                        "Check if alarm reset is functioning",
                        "Verify alarm handling procedure"
                    ],
                    confidence=0.70
                )
                faults.append(fault)
        
        return faults
    
    def _ml_prediction(self, data: DiagnosticData) -> List[Fault]:
        """Use ML model for fault prediction"""
        # TODO: Implement ML-based prediction
        # This would use a trained model (e.g., Random Forest, Neural Network)
        # to predict faults based on feature vectors
        return []
    
    def _correlation_analysis(self, faults: List[Fault], data: DiagnosticData) -> List[Fault]:
        """
        Analyze correlations between faults to identify cascading failures
        and prioritize root causes
        """
        if len(faults) <= 1:
            return faults
        
        # Group related faults
        fault_groups = self._group_related_faults(faults)
        
        # For each group, identify the primary root cause
        primary_faults = []
        
        for group in fault_groups:
            # Sort by severity and confidence
            sorted_group = sorted(
                group,
                key=lambda f: (f.severity.value, f.confidence),
                reverse=True
            )
            
            primary_fault = sorted_group[0]
            
            # Add related faults as additional info
            if len(sorted_group) > 1:
                primary_fault.description += f" (with {len(sorted_group)-1} related faults)"
                primary_fault.symptoms.extend([
                    f"Related: {f.description}" for f in sorted_group[1:3]
                ])
            
            primary_faults.append(primary_fault)
        
        return primary_faults
    
    def _group_related_faults(self, faults: List[Fault]) -> List[List[Fault]]:
        """Group faults that are likely related"""
        groups = []
        assigned = set()
        
        for i, fault1 in enumerate(faults):
            if i in assigned:
                continue
            
            group = [fault1]
            assigned.add(i)
            
            for j, fault2 in enumerate(faults[i+1:], start=i+1):
                if j in assigned:
                    continue
                
                # Check if faults are related
                if self._are_faults_related(fault1, fault2):
                    group.append(fault2)
                    assigned.add(j)
            
            groups.append(group)
        
        return groups
    
    def _are_faults_related(self, fault1: Fault, fault2: Fault) -> bool:
        """Determine if two faults are related"""
        # Same category
        if fault1.category == fault2.category:
            return True
        
        # Overlapping components
        common_components = set(fault1.affected_components) & set(fault2.affected_components)
        if common_components:
            return True
        
        # Time proximity (within 5 minutes)
        time_diff = abs((fault1.timestamp - fault2.timestamp).total_seconds())
        if time_diff < 300:
            return True
        
        return False
    
    def _is_value_stuck(self, signal_name: str, current_value: Any, history: List[Dict]) -> bool:
        """Check if a signal value is stuck"""
        recent_values = [
            record.get(signal_name, None)
            for record in history[-10:]
            if signal_name in record
        ]
        
        if len(recent_values) < 5:
            return False
        
        # Check if all values are the same
        return len(set(recent_values)) == 1
    
    def _interpret_error_code(self, error_code: str) -> Optional[Fault]:
        """Interpret PLC error codes"""
        error_patterns = {
            "E001": ("Communication timeout", FaultCategory.COMMUNICATION, FaultSeverity.CRITICAL),
            "E002": ("Sensor fault", FaultCategory.HARDWARE, FaultSeverity.HIGH),
            "E003": ("Overload", FaultCategory.PROCESS, FaultSeverity.HIGH),
            "W001": ("Low battery", FaultCategory.HARDWARE, FaultSeverity.LOW),
        }
        
        if error_code in error_patterns:
            desc, category, severity = error_patterns[error_code]
            
            return Fault(
                fault_id=f"FAULT_{error_code}_{datetime.now().timestamp()}",
                timestamp=datetime.now(),
                category=category,
                severity=severity,
                description=f"Error code {error_code}: {desc}",
                affected_components=["PLC"],
                symptoms=[f"Error code {error_code} reported"],
                root_cause=desc,
                recommended_actions=["Refer to PLC manual", "Contact technical support"],
                confidence=0.90
            )
        
        return None
    
    def generate_report(self, faults: List[Fault]) -> Dict[str, Any]:
        """Generate comprehensive RCA report"""
        
        # Group by severity
        by_severity = {}
        for fault in faults:
            severity = fault.severity.value
            if severity not in by_severity:
                by_severity[severity] = []
            by_severity[severity].append(fault)
        
        # Generate summary
        report = {
            "timestamp": datetime.now().isoformat(),
            "total_faults": len(faults),
            "by_severity": {
                severity: len(fault_list)
                for severity, fault_list in by_severity.items()
            },
            "critical_faults": [
                f.to_dict() for f in faults
                if f.severity == FaultSeverity.CRITICAL
            ],
            "recommendations": self._generate_recommendations(faults),
            "faults": [f.to_dict() for f in faults]
        }
        
        return report
    
    def _generate_recommendations(self, faults: List[Fault]) -> List[str]:
        """Generate overall recommendations"""
        recommendations = []
        
        # Priority: Critical faults first
        critical = [f for f in faults if f.severity == FaultSeverity.CRITICAL]
        if critical:
            recommendations.append("IMMEDIATE ACTION REQUIRED: Critical faults detected")
            for fault in critical[:3]:
                recommendations.extend(fault.recommended_actions[:2])
        
        # Safety issues
        safety = [f for f in faults if f.category == FaultCategory.SAFETY]
        if safety:
            recommendations.append("Safety system review recommended")
        
        return recommendations


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    analyzer = RootCauseAnalyzer()
    
    # Create sample diagnostic data
    diagnostic_data = DiagnosticData(
        plc_signals={
            "temperature_sensor_1": 75.5,
            "pressure_sensor_1": 101.3,
            "motor_current": 12.5
        },
        historical_data=[
            {"temperature_sensor_1": 75.5, "pressure_sensor_1": 101.2},
            {"temperature_sensor_1": 75.5, "pressure_sensor_1": 101.3},
            {"temperature_sensor_1": 75.5, "pressure_sensor_1": 101.1},
        ],
        error_codes=["E002"],
        alarm_history=[
            {"code": "ALM001", "timestamp": datetime.now()}
        ],
        process_parameters={
            "setpoint_temperature": 75.0,
            "flow_rate": 150.0
        }
    )
    
    # Perform analysis
    faults = analyzer.analyze(diagnostic_data)
    
    print(f"\n=== Root Cause Analysis Results ===")
    print(f"Total faults detected: {len(faults)}\n")
    
    for fault in faults:
        print(f"Fault ID: {fault.fault_id}")
        print(f"  Severity: {fault.severity.value}")
        print(f"  Category: {fault.category.value}")
        print(f"  Description: {fault.description}")
        print(f"  Root Cause: {fault.root_cause}")
        print(f"  Confidence: {fault.confidence * 100:.1f}%")
        print(f"  Actions: {fault.recommended_actions[0]}")
        print()
    
    # Generate report
    report = analyzer.generate_report(faults)
    print(f"=== Summary ===")
    print(f"Critical faults: {report['by_severity'].get('CRITICAL', 0)}")
    print(f"High priority faults: {report['by_severity'].get('HIGH', 0)}")
