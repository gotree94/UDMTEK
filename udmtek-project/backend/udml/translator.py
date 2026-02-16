"""
UDML (Unified Device Machine Language) Translator
Converts vendor-specific PLC instructions to unified intermediate representation
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from enum import Enum
import json
import logging

logger = logging.getLogger(__name__)


class UDMLOpcode(Enum):
    """Unified instruction opcodes"""
    # Data movement
    LOAD = "LOAD"           # Load value to accumulator
    STORE = "STORE"         # Store accumulator to memory
    MOVE = "MOVE"           # Move data between locations
    
    # Logic operations
    AND = "AND"
    OR = "OR"
    XOR = "XOR"
    NOT = "NOT"
    
    # Comparison
    EQ = "EQ"               # Equal
    NE = "NE"               # Not equal
    GT = "GT"               # Greater than
    LT = "LT"               # Less than
    GE = "GE"               # Greater or equal
    LE = "LE"               # Less or equal
    
    # Arithmetic
    ADD = "ADD"
    SUB = "SUB"
    MUL = "MUL"
    DIV = "DIV"
    MOD = "MOD"
    
    # Timer/Counter
    TON = "TON"             # Timer on-delay
    TOF = "TOF"             # Timer off-delay
    TP = "TP"               # Timer pulse
    CTU = "CTU"             # Count up
    CTD = "CTD"             # Count down
    CTUD = "CTUD"           # Count up/down
    
    # Control flow
    CALL = "CALL"           # Function call
    RET = "RET"             # Return
    JMP = "JMP"             # Jump
    JZ = "JZ"               # Jump if zero
    JNZ = "JNZ"             # Jump if not zero
    
    # Special
    NOP = "NOP"             # No operation
    SET = "SET"             # Set output
    RESET = "RESET"         # Reset output


@dataclass
class UDMLInstruction:
    """
    Unified instruction format
    All vendor-specific instructions are translated to this format
    """
    opcode: UDMLOpcode
    operands: List[str]
    source_vendor: str      # Original PLC vendor
    source_instruction: str # Original instruction mnemonic
    address: int
    metadata: Dict[str, Any]
    comment: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "opcode": self.opcode.value,
            "operands": self.operands,
            "source_vendor": self.source_vendor,
            "source_instruction": self.source_instruction,
            "address": self.address,
            "metadata": self.metadata,
            "comment": self.comment
        }


@dataclass
class UDMLProgram:
    """Complete UDML program representation"""
    program_name: str
    source_vendor: str
    instructions: List[UDMLInstruction]
    global_variables: Dict[str, Any]
    functions: List[Dict[str, Any]]
    metadata: Dict[str, Any]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "program_name": self.program_name,
            "source_vendor": self.source_vendor,
            "instruction_count": len(self.instructions),
            "instructions": [inst.to_dict() for inst in self.instructions],
            "global_variables": self.global_variables,
            "functions": self.functions,
            "metadata": self.metadata
        }


class UDMLTranslator:
    """
    Main translator class for converting vendor-specific code to UDML
    """
    
    # Instruction mapping tables for each vendor
    SIEMENS_MAPPING = {
        "A": UDMLOpcode.AND,
        "AN": UDMLOpcode.AND,  # AND NOT - handled with metadata
        "O": UDMLOpcode.OR,
        "ON": UDMLOpcode.OR,   # OR NOT
        "X": UDMLOpcode.XOR,
        "=": UDMLOpcode.STORE,
        "L": UDMLOpcode.LOAD,
        "T": UDMLOpcode.STORE,
        "S": UDMLOpcode.SET,
        "R": UDMLOpcode.RESET,
        "+I": UDMLOpcode.ADD,
        "-I": UDMLOpcode.SUB,
        "*I": UDMLOpcode.MUL,
        "/I": UDMLOpcode.DIV,
        "==I": UDMLOpcode.EQ,
        "<>I": UDMLOpcode.NE,
        ">I": UDMLOpcode.GT,
        "<I": UDMLOpcode.LT,
        "CALL": UDMLOpcode.CALL,
    }
    
    MITSUBISHI_MAPPING = {
        "LD": UDMLOpcode.LOAD,
        "LDI": UDMLOpcode.LOAD,
        "OUT": UDMLOpcode.STORE,
        "AND": UDMLOpcode.AND,
        "ANI": UDMLOpcode.AND,
        "OR": UDMLOpcode.OR,
        "ORI": UDMLOpcode.OR,
        "SET": UDMLOpcode.SET,
        "RST": UDMLOpcode.RESET,
        "MOV": UDMLOpcode.MOVE,
        "ADD": UDMLOpcode.ADD,
        "SUB": UDMLOpcode.SUB,
        "MUL": UDMLOpcode.MUL,
        "DIV": UDMLOpcode.DIV,
    }
    
    ROCKWELL_MAPPING = {
        "XIC": UDMLOpcode.LOAD,   # Examine if Closed
        "XIO": UDMLOpcode.LOAD,   # Examine if Open
        "OTE": UDMLOpcode.STORE,  # Output Energize
        "OTL": UDMLOpcode.SET,    # Output Latch
        "OTU": UDMLOpcode.RESET,  # Output Unlatch
        "TON": UDMLOpcode.TON,
        "TOF": UDMLOpcode.TOF,
        "CTU": UDMLOpcode.CTU,
        "CTD": UDMLOpcode.CTD,
        "ADD": UDMLOpcode.ADD,
        "SUB": UDMLOpcode.SUB,
        "MUL": UDMLOpcode.MUL,
        "DIV": UDMLOpcode.DIV,
        "EQU": UDMLOpcode.EQ,
        "NEQ": UDMLOpcode.NE,
        "GRT": UDMLOpcode.GT,
        "LES": UDMLOpcode.LT,
        "JSR": UDMLOpcode.CALL,
    }
    
    LS_MAPPING = {
        "LD": UDMLOpcode.LOAD,
        "OUT": UDMLOpcode.STORE,
        "AND": UDMLOpcode.AND,
        "OR": UDMLOpcode.OR,
        "SET": UDMLOpcode.SET,
        "RST": UDMLOpcode.RESET,
        "MOV": UDMLOpcode.MOVE,
        "ADD": UDMLOpcode.ADD,
        "SUB": UDMLOpcode.SUB,
    }
    
    OMRON_MAPPING = {
        "LD": UDMLOpcode.LOAD,
        "OUT": UDMLOpcode.STORE,
        "AND": UDMLOpcode.AND,
        "OR": UDMLOpcode.OR,
        "SET": UDMLOpcode.SET,
        "RSET": UDMLOpcode.RESET,
        "MOV": UDMLOpcode.MOVE,
        "ADD": UDMLOpcode.ADD,
        "SUB": UDMLOpcode.SUB,
    }
    
    def __init__(self):
        self.vendor_mappings = {
            "siemens": self.SIEMENS_MAPPING,
            "mitsubishi": self.MITSUBISHI_MAPPING,
            "rockwell": self.ROCKWELL_MAPPING,
            "ls": self.LS_MAPPING,
            "omron": self.OMRON_MAPPING,
        }
        logger.info("UDML Translator initialized")
    
    def translate(self, vendor: str, instructions: List[Any]) -> UDMLProgram:
        """
        Translate vendor-specific instructions to UDML
        
        Args:
            vendor: PLC vendor name (siemens, mitsubishi, rockwell, ls, omron)
            instructions: List of vendor-specific instruction objects
            
        Returns:
            UDMLProgram object
        """
        vendor_lower = vendor.lower()
        
        if vendor_lower not in self.vendor_mappings:
            raise ValueError(f"Unsupported vendor: {vendor}")
        
        logger.info(f"Translating {len(instructions)} instructions from {vendor}")
        
        mapping = self.vendor_mappings[vendor_lower]
        udml_instructions = []
        
        for inst in instructions:
            udml_inst = self._translate_instruction(vendor_lower, mapping, inst)
            if udml_inst:
                udml_instructions.append(udml_inst)
        
        program = UDMLProgram(
            program_name=f"{vendor}_program",
            source_vendor=vendor,
            instructions=udml_instructions,
            global_variables={},
            functions=[],
            metadata={
                "translation_date": "2024-01-01",
                "translator_version": "1.0.0"
            }
        )
        
        logger.info(f"Translation complete: {len(udml_instructions)} UDML instructions")
        return program
    
    def _translate_instruction(self, vendor: str, mapping: Dict, inst: Any) -> Optional[UDMLInstruction]:
        """Translate a single instruction"""
        
        # Extract instruction mnemonic (vendor-specific)
        mnemonic = inst.mnemonic if hasattr(inst, 'mnemonic') else str(inst)
        
        # Look up UDML opcode
        if mnemonic not in mapping:
            logger.warning(f"Unknown instruction for {vendor}: {mnemonic}")
            return UDMLInstruction(
                opcode=UDMLOpcode.NOP,
                operands=[],
                source_vendor=vendor,
                source_instruction=mnemonic,
                address=getattr(inst, 'address', 0),
                metadata={"warning": "unmapped_instruction"},
                comment=f"Unknown: {mnemonic}"
            )
        
        opcode = mapping[mnemonic]
        
        # Extract operands
        operands = []
        if hasattr(inst, 'operands'):
            operands = inst.operands
        
        # Handle special cases (e.g., AND NOT -> AND with negation flag)
        metadata = {}
        if mnemonic in ["AN", "ANI", "XIO"]:  # Negated instructions
            metadata["negated"] = True
        
        return UDMLInstruction(
            opcode=opcode,
            operands=operands,
            source_vendor=vendor,
            source_instruction=mnemonic,
            address=getattr(inst, 'address', 0),
            metadata=metadata,
            comment=getattr(inst, 'comment', None)
        )
    
    def optimize(self, program: UDMLProgram) -> UDMLProgram:
        """
        Optimize UDML program
        - Remove redundant operations
        - Combine adjacent instructions
        - Simplify logic expressions
        """
        logger.info("Optimizing UDML program")
        
        optimized_instructions = []
        i = 0
        
        while i < len(program.instructions):
            inst = program.instructions[i]
            
            # Example optimization: Remove NOP instructions
            if inst.opcode == UDMLOpcode.NOP:
                i += 1
                continue
            
            # Example: Combine LOAD + STORE -> MOVE
            if (i < len(program.instructions) - 1 and
                inst.opcode == UDMLOpcode.LOAD and
                program.instructions[i+1].opcode == UDMLOpcode.STORE):
                
                move_inst = UDMLInstruction(
                    opcode=UDMLOpcode.MOVE,
                    operands=[inst.operands[0], program.instructions[i+1].operands[0]],
                    source_vendor=inst.source_vendor,
                    source_instruction="OPTIMIZED",
                    address=inst.address,
                    metadata={"optimized": True},
                    comment="Combined LOAD+STORE"
                )
                optimized_instructions.append(move_inst)
                i += 2
                continue
            
            optimized_instructions.append(inst)
            i += 1
        
        program.instructions = optimized_instructions
        logger.info(f"Optimization complete: {len(optimized_instructions)} instructions")
        
        return program
    
    def export_json(self, program: UDMLProgram, filepath: str):
        """Export UDML program to JSON file"""
        with open(filepath, 'w') as f:
            json.dump(program.to_dict(), f, indent=2)
        logger.info(f"UDML program exported to {filepath}")
    
    def analyze_complexity(self, program: UDMLProgram) -> Dict[str, Any]:
        """Analyze program complexity metrics"""
        
        opcode_counts = {}
        for inst in program.instructions:
            opcode = inst.opcode.value
            opcode_counts[opcode] = opcode_counts.get(opcode, 0) + 1
        
        return {
            "total_instructions": len(program.instructions),
            "opcode_distribution": opcode_counts,
            "cyclomatic_complexity": self._calculate_cyclomatic_complexity(program),
            "max_nesting_depth": self._calculate_nesting_depth(program)
        }
    
    def _calculate_cyclomatic_complexity(self, program: UDMLProgram) -> int:
        """Calculate McCabe cyclomatic complexity"""
        # Simplified calculation
        decision_points = sum(
            1 for inst in program.instructions
            if inst.opcode in [UDMLOpcode.JZ, UDMLOpcode.JNZ, UDMLOpcode.CALL]
        )
        return decision_points + 1
    
    def _calculate_nesting_depth(self, program: UDMLProgram) -> int:
        """Calculate maximum nesting depth"""
        # Simplified calculation based on CALL depth
        max_depth = 0
        current_depth = 0
        
        for inst in program.instructions:
            if inst.opcode == UDMLOpcode.CALL:
                current_depth += 1
                max_depth = max(max_depth, current_depth)
            elif inst.opcode == UDMLOpcode.RET:
                current_depth = max(0, current_depth - 1)
        
        return max_depth


# Example usage
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    translator = UDMLTranslator()
    
    # Example: Translate Siemens instructions
    from parsers.siemens import PLCInstruction, InstructionType
    
    siemens_insts = [
        PLCInstruction(0, "A", ["I0.0"], InstructionType.LOGIC, b'\x00', "Input 1"),
        PLCInstruction(2, "AN", ["I0.1"], InstructionType.LOGIC, b'\x01', "Input 2 negated"),
        PLCInstruction(4, "=", ["Q0.0"], InstructionType.TRANSFER, b'\x02', "Output"),
    ]
    
    udml_program = translator.translate("siemens", siemens_insts)
    
    print(f"\nTranslation result:")
    print(f"  Source: {udml_program.source_vendor}")
    print(f"  Instructions: {len(udml_program.instructions)}")
    
    for inst in udml_program.instructions:
        print(f"    {inst.opcode.value}: {inst.operands} (from {inst.source_instruction})")
    
    # Analyze complexity
    complexity = translator.analyze_complexity(udml_program)
    print(f"\nComplexity analysis: {complexity}")
